# Technical Notes

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30.

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`KLV_DE_S`**, **annual** grid — for the standardized composite German *kapitalbildende
Lebensversicherung* defined in `product-spec.md` (same directory). **This is not any single insurer's
product.** [S#] / [R#] tags refer to the source list in `sources.md` (numbering carried from
`_research/kapitallebensversicherung.md`; frozen); [REG-R#] tags refer to the cross-product library
`references/regulatory-and-actuarial-references.md` (its own frozen R1–R56 numbering). **[std]** marks
a standardization introduced for the reference implementation; [unverified] marks a claim no search
result corroborated. Parameter values are identical to those in `product-spec.md`. delib was
drafted with all HTTP egress blocked and no document retrieved; the citations have since been
re-verified against the primary documents, and **forty-five of the forty-seven entries in
`sources.md` now record a document that was opened and read**, the two exceptions being [S8] (404)
and [R24] (429). Treat a claim as sound where its entry says `Retrieved: yes`, and as a pointer
rather than a certificate — an instrument named, not one anybody checked — where it does not.
Cells names, model-point columns and CSV headers are English `lower_snake_case`; German terms of art
keep their German form in prose.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — *Beiträge* in;
  *Todesfallleistungen*, *Erlebensfallleistungen* and *Rückkaufswerte* out; insurer expenses and
  commission — for a single-policy model point on an expected basis, with the three state variables that
  make the product what it is: the guaranteed *Deckungskapital*, the accumulated *Überschussguthaben*
  and the accrued *Schlussüberschussanteil*.
- **Out of scope, and said so.** No discounting. **No *Deckungsrückstellung***: the model projects the
  contract's *Deckungskapital* — the amount that should be held — not the balance-sheet quantity of
  § 341f HGB [REG-R54]. No *Zinszusatzreserve* [REG-R17], no RfB stock [REG-R10] [REG-R19], no MindZV
  allocation [R6] [REG-R18], no P&L, no Solvency II technical provision, risk margin, SCR or MCR
  [REG-R1] [REG-R2] [REG-R6]. No *Beteiligung an den Bewertungsreserven* in the base run — the parameter
  exists and is zero [R1] [R8]. No tax: delib publishes gross benefits and the tax rules enter only as
  design constraints. No premium-default path, §§ 37 and 38 VVG never having been researched (gap 20);
  no § 222 or § 314 VAG write-down [REG-R12]; no *Zusatzversicherungen*, *Kapitalwahlrecht*, *Dynamik*
  or *Beleihung*.
- **Projection frequency.** **Monthly grid, over an annual product.** Every contractual mechanic on
  this contract is annual and stays annual: the surplus is declared once a year and allocated at the
  *Bilanzstichtag* [S9], the *Rückkaufswert* is struck at the end of the current *Versicherungsperiode*
  [R2], the *beitragsfreie Versicherungssumme* is tabulated *für jedes Versicherungsjahr* [R3], the
  *Deckungskapital* rolls forward by Fackler from one anniversary to the next at an annual
  *Rechnungszins*, and the *Ablauf* falls on an anniversary [S7]. What the finer grid resolves is
  everything that is **not** contractually annual — the *Beitrag* the contract bills in instalments,
  the insurer's running expense, and the decrements, which now fall in the month they happen.
- **Two clocks, and which quantity runs on which.** Cells that state an **annual account** take a
  0-based policy year `k`: the whole pricing block, all three reserves, the § 169 value, the paid-up
  purchase, every part of the *Überschussbeteiligung*, the *Stornoabzug* band and the expense
  inflation. Cells that state a **month** take `t`: the in force, the claims, the premium instalments
  and every `result_cf()` column. The decrement rates take `t` and return the **year's annual** rate;
  `mort_rate_mth(t)` and `lapse_rate_mth(t)` are what the recursion applies, each
  `1 − (1 − r)^(1/12)` **[std]**, so twelve of each compound back to the year's rate exactly.
- **What `t` counts, and it is 0-based.** `t` is the **policy month index**, measured from **issue**:
  month `t` runs from time `t` to time `t + 1`. `duration(t) = t // 12` is the completed policy years
  at the start of month `t` — the **bridge between the two clocks** — and is what every duration-keyed
  schedule is indexed on: the *Stornoabzug*, the lapse table, the § 169 Abs. 3 five-year spreading, the
  *beitragsfreie Versicherungssumme*. `age(t) = issue_age + duration(t)` steps on the **anniversary**
  and not monthly, and `is_anniv(t) = (t % 12 == 11)` marks the month the annual machinery acts in. The
  **contractual** policy year is the 1-based label `policy_year(t) = duration(t) + 1`, and it is
  **derived, never indexed by**: it is the key into the tables whose own column is called
  `policy_year`.
- **Where the frame starts, and `proj_len()`.** `proj_len_y() = policy_term` is the number of policy
  years and what every annual construction is written against; `proj_len() = 12 · proj_len_y()` is the
  frame's **exclusive** end. The frame runs `t = t_start() … proj_len() − 1` contiguously with
  `t_start() = 12 · duration_init` — `duration_init` being an elapsed count of policy **years**, so the
  conversion is a multiplication — and `k_start() = duration_init` is its annual counterpart. Hence
  `result_cf().index[-1] == proj_len() − 1`, `len(result_cf()) == proj_len() − t_start()`,
  `result_cf().index[0] == t_start()` and `pols_if(t_start()) == pols_if_init()` on every model point.
  This is lifelib's own `for t in range(proj_len())`. The *Ablauf* falls at the end of the last month;
  **there is no `t = proj_len()` row.** `result_cf_annual()` sums the frame into policy years and is
  the view the worked example below is stated on.
- **Timing conventions [std].** A *Beitrag* **instalment** on the *Zahlweise*'s own cycle at the
  **beginning** of the month — one month in twelve for an annual payer, every month for a monthly one;
  acquisition expense and initial commission in month `t_start()` at issue, as single amounts and not
  twelfths; **one twelfth** of the maintenance expense and the renewal commission on the instalment, at
  the beginning of the month on the in-force; the guaranteed *Deckungskapital* rolling forward over the
  **policy year** at the *Rechnungszins*; the surplus declared and credited **at the anniversary** on
  that year's closing reserve; death and maturity claims at the **end of the month**; surrender at the
  end of the month, **after** the mortality decrement.
- **What a mid-year exit is paid [std].** A death or surrender in a **non-anniversary** month is paid
  the balances **standing at the end of that month** — which are the ones struck at the **last**
  anniversary, the year's declaration not having happened yet. So `av_sur_close_pp`,
  `bonus_si_close_pp`, `term_bonus_close_pp` and `res_guar_close_pp` return the year's own closing
  figure in an anniversary month and the previous one otherwise. On a *gezillmert* contract the
  guaranteed leg of a surrender is therefore **exactly zero through the whole first policy year**,
  which is the consumer fact this product is best known for and one the annual grid could not express:
  it had to pay a month-0 surrender the value the coming anniversary would close at, a forward-looking
  payment at a date it is not yet due. The documented alternative — a *pro rata temporis* accrual of
  the year's declared surplus — is a **variant and not the base**: no retrieved German wording
  describes one, and it would put an unsourced accrual rule inside the benefit. It reconciles at the
  anniversary just as exactly, so only the sources decide between them.
- **What the § 169 value does *not* resolve.** § 169 Abs. 3 VVG strikes the *Rückkaufswert* "zum
  Schluss der laufenden Versicherungsperiode" and § 12 VVG makes that period follow the *Zahlweise*, so
  on a monthly-paying contract the statute would strike it monthly. **The model does not, and says so
  rather than interpolating**: a monthly § 169 value needs a monthly *Deckungskapital*, and the tariff
  defines the *Rechnungsgrundlagen der Prämienkalkulation* on an annual *Rechnungszins* and an annual
  first-order table. The value standing between two anniversaries is the one struck at the last.
- **The Bilanzstichtag becomes the policy anniversary [std].** The sources put the allocation at the
  *Bilanzstichtag*, 31 December [S9]; on a policy-year grid that falls inside a policy year for every
  contract not written on 1 January, so the model allocates at the **policy-year end**. The effect is a
  timing shift of up to one year in the surplus credit, stated rather than hidden. The monthly grid
  does not narrow it: it is a mismatch between two annual clocks, not a resolution limit.
- **Age basis.** Age last birthday at issue, stepping at the policy anniversary **[std]** — no located
  German endowment wording states one (`product-spec.md`, footnote 6). The age steps at `t = 12, 24,
  …`, and the monthly grid does not make it finer.
- **Unisex pricing is a hard constraint.** `sex` is carried and drives the **decrement** lookup but
  **must not enter the premium**: § 20 Abs. 2 Satz 1 AGG was repealed and new business has been unisex
  since 21 December 2012 [REG-R34]. The pricing basis is a fixed portfolio blend; letting `sex` leak
  into `prem_gross_pp` reproduces a tariff unlawful in Germany since 2012 (pitfall 17).
- **No account value in the unit-linked sense.** The house vocabulary's `prem_to_av_pp` has **no
  counterpart here** and is not published: a *Beitrag* funds the *Deckungskapital* through the tariff,
  not a policyholder account, and the only true account is the *Überschussguthaben*, which receives
  surplus and never premium. `withdrawals` is likewise absent — a classic German endowment has no
  partial-withdrawal right in any located wording.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  claims, expenses and commission −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to euro
  cents and `pols_if` to six decimals **[std]**.

---

## Model point attributes

Every column of `model_point_table.csv` is published as a cells of the same name.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Row key; `Projection`'s only parameter | all |
| `policy_id` | str | Human-readable identifier | all |
| `sex` | enum {M, F} | Decrement lookup only; **never** a pricing input [REG-R34] | 7 (F) |
| `smoker` | enum {N, S} | Feeds `rating_factor`; no published scale [R14] | 14 (S) |
| `issue_year` | int | Cohort identity: fixes the DeckRV ceilings [REG-R15] and the tax cohort [R10] | 10 (2012) |
| `issue_age` | int | Age last birthday at issue | all |
| `duration_init` | int | Completed policy **years** at the valuation date; 0 = new business. An **elapsed count**, so already 0-based: it *is* `k_start()`, and `t_start() = 12 ×` it | 10 (14) |
| `pols_if_init` | float | Policies represented at `t_start()` | all |
| `policy_term` | int | *Versicherungsdauer*, in years; equals `proj_len_y()`, and `proj_len() = 12 ×` it | all |
| `prem_term` | int | *Beitragszahlungsdauer* ≤ `policy_term`; **1 = *Einmalbeitrag*** | 2 (1), 3 (15) |
| `sum_assured` | EUR | Guaranteed *Erlebensfallleistung* (*Versicherungssumme*) | all |
| `death_ratio` | float | *Todesfallleistung* ÷ *Erlebensfallleistung*; 1.00 = the endowment proper | 14 (0.60) |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | Payment frequency | 4–7 |
| `unterjaehrig_form` | enum {echt, unecht} | Whether the sub-annual premium is a genuine sub-annual *Versicherungsperiode* (**no** loading) or an instalment of an annual one (loaded) [R28] | 4 / 5 |
| `rechnungszins` | rate | The contract's own guaranteed technical rate, fixed at conclusion [REG-R14] | 10 (1.75%) |
| `zillmer_on` | 0/1 | Whether the *Deckungskapital* is *gezillmert*. **[std]** — § 4 DeckRV sets a ceiling, not a mandate [R7], and no retrieved carrier wording is un-zillmered | 13 (0) |
| `cost_id` | str | Key into `cost_table.csv`: the tariff loadings and the expense basis | all |
| `surplus_use` | enum {ansammlung, bonus, beitragsverrechnung} | *Überschussverwendung* [R28] | 8, 9 |
| `scenario_id` | str | Key into `surplus_rate_table.csv`: the declared-rate path | 3 (low), 14 (nil) |
| `rating_factor` | float | *Risikozuschlag* multiplier on the risk premium; 1.00 at standard rates [R5] | 14 (1.50) |
| `av_sur_pp_init` | EUR | *Überschussguthaben* carried at the valuation date | 10 |
| `bonus_si_init` | EUR | Bonus sum insured already bought (*Bonussystem*, in force) | — |
| `bfz_year` | int | **Contractual, 1-based policy year** at whose end *Beitragsfreistellung* is elected; 0 = never; ≤ `duration_init` = already paid-up. Not a frame index: the election falls at the end of the 0-based policy year `bfz_year − 1` — month `12(bfz_year − 1) + 11` — so the contract is paid-up from policy year `bfz_year` onwards. The column stays 1-based because 0 has to remain free to mean "never" | 11 (10), 12 (3) |

`sum_assured` and `death_ratio` are the two halves of the *gemischte Versicherung*, and the
*Mindesttodesfallschutz* [R12] [REG-R45] requires the death sum to be at least 50 % of the
*Beitragssumme* — a **model-point design constraint**, checked when the table is built, not a model
formula. `rechnungszins` is a contract term, not a market rate: fixed at conclusion and carried for the
whole term [REG-R14], which is why the in-force point carries 1,75 % and new business 1,00 %.

**The fourteen model points.** Point 1 is the worked example's anchor; the other thirteen each exercise
something it does not. Every one satisfies the *Mindesttodesfallschutz* [R12] [REG-R45] and carries a
`rechnungszins` at or below its cohort's ceiling [REG-R15].

| # | What it adds | Key columns |
|---|---|---|
| 1 | **Anchor.** New-business *gemischte Versicherung*, level annual premium over the full term | M 37, term 25, `prem_term` 25, SI 50,000, ratio 1.00, annual, 1.00%, zillmered, `ansammlung`, `base` |
| 2 | *Einmalbeitrag* — the other premium form; the 25 ‰ *Zillmersatz* then buys almost nothing | as 1 with `prem_term` = **1** |
| 3 | *Abgekürzte Beitragszahlungsdauer*: premiums stop at 15, cover runs to 25; on the `low` scenario | as 1 with `prem_term` = **15**, `scenario_id` = `low` |
| 4 | Monthly, ***unecht*** — the 5 % *Ratenzahlungszuschlag* applies | `prem_freq` monthly, `unterjaehrig_form` **unecht** |
| 5 | Monthly, ***echt*** — a genuine monthly *Versicherungsperiode*, so **no** loading [R28] | `prem_freq` monthly, `unterjaehrig_form` **echt** |
| 6 | Half-yearly (2 % loading) | `prem_freq` half_yearly, unecht |
| 7 | Quarterly (3 % loading), female — the unisex-pricing pair with 1 | `prem_freq` quarterly, `sex` **F** |
| 8 | ***Bonussystem*** — pairs with 1 for the [R28] maturity/death asymmetry | `surplus_use` **bonus** |
| 9 | ***Beitragsverrechnung*** — the surplus reduces the *Zahlbeitrag* instead of a benefit | `surplus_use` **beitragsverrechnung** |
| 10 | **In force**, a 2012 cohort on a 1,75 % guarantee, opening at `t_start()` = 14 with an *Überschussguthaben* | issue 2012, M 40, term 30, `duration_init` 14, `rechnungszins` **1.75%**, `av_sur_pp_init` 6,000 |
| 11 | ***Beitragsfreistellung*** succeeding: premiums cease at the end of policy year 10 (`k` = 9, month 119), the contract stays in force | as 1 with `bfz_year` = **10** |
| 12 | **Boundary.** *Beitragsfreistellung* **failing** the *Mindestversicherungsleistung*, so the election becomes a surrender at the end of policy year 3 — `k` = 2, and the whole cohort leaves in **month 35** [R3] | M 45, term 20, SI **6,000**, `bfz_year` = **3** |
| 13 | **Non-*gezillmert*** — the § 169 floor is then slack and the three reserves coincide. **[std]**: all four retrieved wordings that state a method apply § 4 DeckRV *Zillmerung* [S7] [S9] [S18], so this point exercises the ceiling being a maximum rather than a market option anyone was observed taking | as 1 with `zillmer_on` = **0** |
| 14 | **Boundary.** Unequal sums, old entry, a *Risikozuschlag*, and zero declared surplus | M 55 smoker, term 12, SI 30,000, ratio **0.60**, `rating_factor` **1.50**, `scenario_id` **nil** |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | Policies in force at the **start** of **month** `t`; `pols_if(t_start()) = pols_if_init()`. `pols_if_at(t, timing)` gives `"BEF_DECR"` / `"AFT_MORT"` / `"AFT_LAPSE"` | monthly decrements |
| `res_pp(k)` | Guaranteed *Deckungskapital* per policy at the **start** of **policy year** `k`, on the first-order basis. `res_pp_at(k, timing)` gives `"BEF_PREM"` / `"AFT_PREM"` / `"AFT_INT"` | annual, prospective, with a roll-forward check |
| `av_sur_pp(k)`, `bonus_si_pp(k)` | *Überschussguthaben* per policy at the start of **policy year** `k`, nil unless `surplus_use = ansammlung`, with `av_sur_pp_at(k, timing)` and `av_sur_at(k, timing)` per the house convention for a *verzinsliche Ansammlung* side account — library-wide `av_pp` is the **principal** balance, which in this product is the reserve `res_pp` and not an account; and the bonus sum insured bought out of surplus, nil unless `surplus_use = bonus` | annual recursion |
| `term_bonus_pp(k)` | Accrued *Schlussüberschussanteil* at the start of **policy year** `k`, payable at the *Ablauf* and on death, not on surrender in the base run | annual accrual |
| `*_close_pp(t)` | The four balances above — and the § 169 value — **standing at the end of month `t`**: the year's own closing figure in an anniversary month, and the one struck at the last anniversary otherwise. What a mid-year exit is actually paid | derived, monthly |
| `is_paid_up(k)` | Whether the contract is *beitragsfrei* at the start of **policy year** `k`; true from `k = bfz_year` onwards, the election falling at the end of policy year `bfz_year − 1` | set once, at the `bfz_year` election |
| `bfz_si_pp` | *Beitragsfreie Versicherungssumme* bought at the *Beitragsfreistellung*, or 0 where the *Mindestversicherungsleistung* test fails and the election became a surrender | once per model point |

There is **no** unit fund, **no** policyholder account fed by premium and **no** partial-withdrawal
ledger. The *Überschussguthaben* is a genuine account fed by declared surplus alone, and § 341f HGB
confirms the separation from the other direction: the *Deckungsrückstellung* is formed **excluding
*verzinslich angesammelte Überschussanteile*** [REG-R54].

---

## Assumption inputs

**The external CSVs.** Every input is a plain UTF-8 CSV in the model folder's **parent**, read once per
model by a reader cells in `Data` — the `annuallife/TradLife_A` layout, not `basiclife/BasicTerm_S`'s
embedded IOSpec. Every file but `model_point_table.csv` carries a final **`provenance`** column, one tag
per row: delib's second ruling, machine-checked.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the 22 further attributes of the table above (exempt from `provenance`) |
| `mort_table.csv` | `sex`, `age` | `mort_rate_1st`, `provenance` |
| `lapse_table.csv` | `policy_year` (**1-based label**, read as `policy_year(t) = t + 1`) | `lapse_rate`, `storno_rate`, `provenance` |
| `surplus_rate_table.csv` | `scenario_id`, `policy_year` (**1-based label**, read as `t + 1`) | `decl_rate`, `term_rate`, `ans_rate`, `provenance` |
| `cost_table.csv` | `cost_id` | `alpha_rate`, `beta_rate`, `gamma_rate`, `acq_expense`, `maint_expense`, `expense_infl`, `claim_expense`, `comm_init_rate`, `comm_renew_rate`, `provenance` |
| `freq_loading_table.csv` | `prem_freq` | `instalments`, `prem_freq_load`, `provenance` |
| `deckrv_table.csv` | `issue_year` | `hoechstrechnungszins`, `hoechstzillmersatz`, `provenance` |

`cost_table.csv` deliberately carries the **first-order tariff loadings and the second-order expense
assumptions on the same row**, because the difference between them *is* the *Kostenüberschuss*, and
`deckrv_table.csv` carries both DeckRV ceilings — § 2's *Höchstrechnungszins* and § 4's
*Höchstzillmersatz* — keyed by `issue_year`, both being cohort facts that travel with the contract
[REG-R14] [REG-R15] [REG-R16]. The scalars that are not tables — `mort_be_factor`, `suicide_share`,
`bfz_min_si`, `term_surr_share`, `bwr_rate` and the two behaviour-module switches — are `Projection`
References, and their values and tags are in this section.

Three classes. Class (a) is contractual or statutory and is cited; class (b) is the insurer's current
discretionary declaration, revisable annually and capable of being zero [S3] [S9]; class (c) is the
modeller's view of experience. The split is the German ***Rechnungsgrundlagen erster und zweiter
Ordnung*** distinction wearing different clothes [REG-R47]: (a) is the first-order basis, which fixes
the *Bruttobeitrag* and the guaranteed benefits — the numbers the contract states — while (c) is the
second-order basis, which drives the projection, and (b) is the output of the insurer's policy for
distributing the wedge between them.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| *Rechnungszins* `rechnungszins` | Model-point column; 1.00% for new business from 1 January 2025, the cohort's rate otherwise | [R7] [R15] [REG-R14] [REG-R15] |
| *Höchstrechnungszins* ceiling by cohort | 3.50% to 06/1994; 4.00% to 06/2000; 3.25% to 2003; 2.75% to 2006; 2.25% to 2011; 1.75% to 2014; 1.25% to 2016; 0.90% to 2021; 0.25% to 2024; **1.00% from 2025** | [REG-R15]; the split-year convention **[std]** (1) |
| *Höchstzillmersatz* ceiling by cohort | **40 ‰** of the *Beitragssumme* to 2014, **25 ‰** from 1 January 2015; the rate used at conclusion applies for the whole term | [R7] [S15] [REG-R16] [REG-R20] |
| *Zillmersatz* `alpha_rate` | 25 ‰ of the *Beitragssumme*, at the ceiling | ceiling [R7] [REG-R16]; the level **[std]**, `product-spec.md` (15) |
| Premium form and frequency | Level *Bruttobeitrag* over the *Beitragszahlungsdauer*, in advance, ceasing on death [S7], on *Beitragsfreistellung* [R3] and at the end of the *Beitragszahlungsdauer*; *Ratenzahlungszuschlag* 2% half-yearly, 3% quarterly, 5% monthly, applied **only** to `unterjaehrig_form = unecht` | [S3] [S7] [R3] [R28] [R28-family]; single loading values **[std]** |
| The two benefits | *Erlebensfallleistung* `sum_assured` at the *Ablauf* if the insured is then alive; *Todesfallleistung* `sum_assured × death_ratio` on death before it — each plus the accumulated surplus and the accrued *Schlussüberschussanteil* | [S7] [S11] [R1] [R18-family] |
| *Rückkaufswert* | The *Deckungskapital* on the *Rechnungsgrundlagen der Prämienkalkulation*, at the **end of the current *Versicherungsperiode***, floored on *Kündigung* by the five-year-spread *Mindestrückkaufswert*, less a *vereinbart*, *beziffert* and *angemessen* *Stornoabzug*, plus the *Überschussguthaben* | [R2] [R22] [R24] [REG-R28]; even-spread reading **[std]** (2) |
| *Beitragsfreistellung* | At the end of the current *Versicherungsperiode*, **if** the *Mindestversicherungsleistung* is reached; otherwise the insurer pays the § 169 value and the election **becomes a surrender**. The paid-up sum is computed on the § 169 value | [R3] [REG-R28] |
| *Selbsttötung* | Within three years of conclusion the insurer is *leistungsfrei* but **must pay the *Rückkaufswert* including *Überschussanteile*** — a benefit **substitution**, not a forfeiture | [R4] [REG-R26] |
| Surplus allocation base and timing | A percentage of the *Deckungskapital* — "in Prozent des maßgeblichen Deckungskapitals" [S7], the reserve "um ein Jahr mit dem Rechnungszins abgezinst" [S18], booked into the *Deckungskapital* at each *Bilanztermin*, 31 December [S9]. **Entitlement timing varies across carriers**: none at [S9], a one-year *Wartezeit* at [S18], three years at [S7] tariff group A and [S3]; the model takes the shortest, which is **[std]** | [S7] [S18] [S9] [S3] [R1] |
| *Beteiligung an den Bewertungsreserven* | Half of the amount determined on termination, but only to the extent it exceeds the *Sicherungsbedarf*. **Zero in the base run** | [R1] [R8] [REG-R9] [REG-R24]; zero **[std]** |

1. The published history splits 1994 and 2000 mid-year [REG-R15] and a year-keyed table cannot, so both
   split years take the **higher** of the two rates — 4,00 % — making `check_rechnungszins_cap()`
   permissive rather than strict in exactly the two years where the model cannot know which half of the
   year a contract was written in. Years after 2026 carry 1,00 %, held flat **[std]** [R15].
2. § 169 Abs. 3 VVG's "gleichmäßige Verteilung … auf die ersten fünf Vertragsjahre" [R2] is implemented
   as a **straight-line** amortisation of `alpha_cost` in five equal instalments; the alternative
   reading — a five-year *Zillmerung* — gives a slightly lower floor at durations 1 to 4 and the same
   value from duration 5, and is pitfall 5.

### (b) Insurer-discretionary current elements (snapshot; revisable annually, and may be zero)

| Input | Base value | Basis |
|---|---|---|
| Declared *laufende Verzinsung* `decl_rate` | **2.70% p.a., level**, whence the derived `zins_ueberschuss_rate = max(0, decl_rate − rechnungszins)` = 1.70% on the anchor cell — **never an input and never added on top of the guarantee** (pitfall 1) | Allianz's **2025** declaration for "die klassischen Lebens- und Rentenversicherungen", i.e. a combined book, reported by the trade press [R26] — **the three Allianz pages state no declared rate at all** [S11], and no carrier in this corpus publishes one for an endowment book; the retrieved named-carrier band is 2.25%–2.80% [R26]; level-forever **[std]** (3); derivation [REG-R53] |
| *Schlussüberschussanteilsatz* `term_rate` | **0.40% p.a.** of the *Deckungskapital*, accrued and paid at the *Ablauf* and on death | **[std]** (4) — **no rate of any kind was established** (gap 1) |
| *Ansammlungszinssatz* `ans_rate` | **2.70% p.a.**, equal to the declared rate | mechanism [R28]; the § 28 RechVersV disclosure names the rate as a published quantity [REG-R54]; the level **[std]** (5) |
| Scenarios `low` / `nil` | `low`: `decl_rate` 1.20%, `term_rate` 0.10%, `ans_rate` 1.20%. `nil`: all three **0.00%** | `nil` rests on the sourced statement that the surplus "may also be zero euros" [S9]; both scenarios **[std]** |
| *Stornoabzug* `storno_rate` | 10% of the guaranteed value in years 1–5, 7.5% in 6–10, 5% in 11–15, 2.5% from 16 | **three carrier schedules on three bases**: 0–20% of the *Deckungskapital*, decaying to nil over the last ten years, sub judice [S3] [R22] [R30]; 50 € + 0,15% of premiums × years remaining [S9]; 100 € + 0,2% of (sum insured − reserve) [S18]; schedule **[std]** |
| *Bewertungsreserven* rate `bwr_rate` | **0.00%** | [R1] [R8] [REG-R9]; zero **[std]** |

3. Level for the whole projection is a modelling choice, not a forecast: the corpus supports a
   **direction** — about one in three insurers raised the rate for 2026, Allianz did not, the caution
   attributed to remaining *stille Lasten* [R25] [R26] — and no path, so two alternative paths ship as
   scenarios and the sensitivity is exercisable rather than argued.
4. **Nothing in the corpus fixes a terminal-bonus level, for any insurer, in any year** (gap 1). 0.40 %
   p.a. on the *Deckungskapital* makes the terminal share a visible but clearly secondary part of the
   maturity benefit; paying it at the *Ablauf* and on death and **not** on surrender is the choice that
   does not invent an entitlement the sources do not describe (`product-spec.md`, footnote 12).
5. Setting `ans_rate = decl_rate` is a market convention rather than a sourced fact, and it matters for
   one reason: because `ans_rate > rechnungszins`, **the *verzinsliche Ansammlung* out-accumulates the
   *Bonussystem* at maturity while the *Bonussystem* pays more on an early death** — exactly the
   asymmetry [R28] records (pitfall 15). Setting `ans_rate = rechnungszins` would destroy it.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German insurer publishes a mortality basis, an expense
loading, a commission scale or a lapse rate for this product, and the DAV tables are not public.

**Mortality — two bases, one table.** The first-order basis is `mort_table.csv`, a **[std] Makeham-form
proxy**, sex-specific, ages 0 to 120:

```
mort_rate_1st(M, x) = 0.00022 + B · 1.10^x          with B fixed by the anchor below
mort_rate_1st(F, x) = 0.00016 + B · 1.10^(x − 3)     a three-year setback on the same curve
```

**The anchor is `mort_rate_1st(M, 37) = 0.001200` exactly**, which fixes `B` and makes the worked
example reproduce; the `Data` docstring states it.

**The table is read twice, for two different purposes, and they must not be confused.** The
*tariff* rate `mort_rate_at_age(x)` — what prices and what reserves — is a **fixed unisex blend**
of the two rows, `½ · q₁(M, x) + ½ · q₁(F, x)` **[std]**, because German new business has been
unisex since 21 December 2012 [REG-R34] and a tariff that priced on `sex` would be unlawful; the
blend itself is a portfolio mix no insurer publishes. The *decrement* is the policy's own
sex-specific row, `mort_rate_base(t)`, and the best-estimate basis is that scaled:
`mort_rate(t) = mort_rate_base(t) × mort_be_factor` with **`mort_be_factor = 0.75` [std]**, so the
first-order table carries a 33 % safety loading. That wedge is the ***Sicherheitszuschlag*** and its
systematic release **is** the *Risikoüberschuss* [REG-R47] — the model does not compute the surplus
from it, but the two must not be confused, and using one basis where the other belongs is pitfall 14.

The table this proxy stands in for is **DAV 2008 T**, the market-standard first-order basis for German
death-benefit business, derived from insurers' own policy data over the observation years **2001 to
2004** — the derivation paper was read for this pass and says so; 2006–2008, recorded here before,
is when the DAV working group did the work — pooled from Gen Re, Münchener Rück, Swiss Re and the
Verband öffentlicher Versicherer across 47 undertakings and more than 100 million *Bestandsjahre*, the
cleansed insured data covering **60 % of the German market in the *Kapitallebensversicherung*
segment** [R14]. It is a single **Schlusstafel** built from data from the sixth policy year onwards to
strip out selection, and there is **no separate endowment table**: about 91 % of the observations
behind it are endowment data, and endowment mortality from the sixth year is 101 % of the all-tariff
level [R14]. **It is
the property of the Deutsche Aktuarvereinigung, is not public and is not redistributed here** [R14]
[REG-R47] [REG-R48]. A replacement must preserve four things: an **insured-lives**, not population,
level, materially lighter than Destatis at the working ages [REG-R52]; **sex-specific** base tables,
the raw material even though a tariff may not price on sex [REG-R34]; **no projected improvement**,
because for a death cover improvement favours the insurer [REG-R48]; and an explicit
*Sicherheitszuschlag* directed *upward* for the death leg. **The proxy carries no selection factors**,
which DAV 2008 T is understood to have [REG-R48], so a book of newly underwritten lives shows more
early deaths here than a real one — stated rather than corrected by a second unsourced factor. And
the *Richtlinie* states the suitability limit in terms — "Die Sterbetafel DAV 2008 T ist grundsätzlich
auch für die Beitragskalkulation von Lebensversicherungen mit Todesfallcharakter, **ausgenommen Tarife
ohne Gesundheitsprüfung**, geeignet" [R14] — so the whole basis presupposes the underwriting the
composite specifies.

**One table for two legs — a compromise.** The death leg wants a prudent basis with mortality *higher*
than expected and the survival leg one *lower*, so the direction of prudence forks and a single
first-order table cannot be prudent for both [REG-R47] [REG-R48]. German practice resolves this in the
tariff rather than the table and the model follows: one first-order table for both legs, the compromise
named here and asserted as pitfall 13 rather than papered over.

**Lapse [std].** The decrement is **surrender only**. `lapse_table.csv`:

| Policy year (`t + 1`) | 1–2 | 3–8 | 9–11 | 12 | 13+ | final year |
|---|---|---|---|---|---|---|
| `lapse_rate` | 5.0% | 3.5% | 2.0% | 6.0% | 2.5% | **0** |

The file's key column is the **contractual, 1-based** `policy_year`, so the row for policy year 12 is
read at `t` = 11.

The **shape** is the one thing the evidence supports: the half-income tax rule needs twelve years and
age 60 or 62 [R10] [REG-R45], so surrenders are suppressed approaching duration 12 and spike at it,
exactly as the eight-year threshold drives French *assurance vie* [REG-R45]. **The levels are not
sourced.** The only German lapse datum is a market aggregate: "Die Stornoquote (Anzahl) stieg im Jahr
2023 leicht auf **2,56 %** (Vorjahr: 2,51 %)" [R20] — one **count** measure over all life business,
neither endowment-specific nor split by duration, so it cannot be a surrender decrement (pitfall 10).
The 2,72 % for 2024 and the second 1,2 % measure recorded here before this pass are not in the
retrieved GDV publication and are withdrawn. What the supervisor adds is directional rather than
numerical: some products show "sehr hohen Stornoquoten ... speziell in den ersten Jahren nach
Vertragsabschluss", which is the shape of the first two rows above [R18]. In the **final
policy year the rate is zero**: the end of year `t = n − 1` is the *Ablauf*, so the survivors leave as
a maturity. Unlike frlib's term product this is not a bookkeeping split — a final-year surrender would pay
the § 169 value while a maturity pays the sum insured plus surplus — so it decides a real payment, and
is stated as an assumption and asserted as pitfall 18.

**Expenses, commission and the tariff loadings, side by side.** `cost_table.csv` carries both, on one
row per `cost_id`, because the difference between them **is** the *Kostenüberschuss*:

| Input | Basis `std_2026` | Class | Tag |
|---|---|---|---|
| `alpha_rate` | 25 ‰ of the *Beitragssumme*, zillmered | first order | ceiling [R7] [REG-R16]; level **[std]** |
| `beta_rate` | 3.0% of the *Bruttobeitrag*, over the *Beitragszahlungsdauer* | first order | form [R28]; level **[std]** |
| `gamma_rate` | 1.5 ‰ of the *Versicherungssumme* p.a., over the *Versicherungsdauer* | first order | form **not established**, gap 17; **[std]** |
| `acq_expense` | 300 EUR per policy at issue | second order | **[std]** |
| `comm_init_rate` | 2.5% of the *Beitragssumme* at conclusion | second order | set at the 25 ‰ *zillmering* ceiling [R7], which is **not** a commission cap — "Eine Deckelung der Provisionen ist gesetzlich nicht vorgesehen" [R29]; **no carrier commission rate is established**, so **[std]** with no observation behind it |
| `comm_renew_rate` | 1.5% of the *Bruttobeitrag* from year 2 (*Bestandsprovision*) | second order | mechanism [R29]; level **[std]** |
| `maint_expense` | 45 EUR per in-force policy p.a. | second order | **[std]** |
| `expense_infl` | 1.8% p.a. | second order | **[std]** |
| `claim_expense` | 120 EUR per death, maturity or surrender claim | second order | **[std]** |

**No charge level of any kind was established for any German carrier** (gap 7). The levels are
placeholders sized so the first-year acquisition outgo — 300 EUR plus 2,5 % of the *Beitragssumme* —
modestly exceeds what the *Zillmerung* recovers, so the anchor carries the new-business strain a real
German endowment carries. **The *Effektivkosten* they produce is a validation target, not an input**:
reproducing one needs the PRIIPs Annex VI algorithm and a holding period, neither of which delib
implements [R9] [R19] [REG-R31] [REG-R32].

**Suicide share `suicide_share` = 0.02 [std].** § 161 VVG substitutes the *Rückkaufswert* for the sum
insured on the suicide sub-cause of death in the first three policy years [R4] [REG-R26]. No source
gives a suicide share of deaths at any age, so 2 % is a placeholder standing for "about one death in
fifty in the window is an excluded suicide". Setting it to zero is a defensible variant; **paying nil
instead of the *Rückkaufswert* is not** (pitfall 7). The *Bewertungsreserven* share is zero for the
reason in `product-spec.md`, footnote 13, and there is no dynamic lapse formula in the base run — the
optional modules are under *Policyholder behaviour modelling*.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | **month** index, **0-based** from issue, `t = t_start … 12n − 1` |
| `k` | `duration(t)` | completed policy **years** at the start of month `t`, `= t // 12`; the argument of every annual cells |
| `y(t)` | `policy_year(t)` | contractual, **1-based** policy year label, `= k + 1`; the key into the `policy_year` column of the input tables |
| (anniv) | `is_anniv(t)` | whether month `t` is the last of a policy year, `t % 12 == 11` |
| `n`, `m` | `policy_term`, `prem_term` | *Versicherungsdauer*; *Beitragszahlungsdauer*. `n` is also `proj_len_y()`, and `proj_len() = 12n` is the frame's exclusive end |
| `x(k)` | `age_y(k)`, `age(t)` | attained age at the start of policy year `k` = `issue_age + k`; `age(t) = age_y(duration(t))` |
| `SE`, `SD` | `sum_assured`, `sum_death` | guaranteed survival sum; guaranteed death sum `= SE × death_ratio` |
| `i₁`, `v₁` | `rechnungszins` | first-order interest rate; `v₁ = 1/(1 + i₁)` |
| `q₁(x)` | `mort_rate_at_age(x)` | first-order **tariff** mortality at attained age `x`: the unisex blend, which prices and reserves |
| `q(t)` | `mort_rate(t)` | best-estimate **annual** mortality of month `t`'s policy year, `= mort_rate_base(t) × mort_be_factor` |
| `qᵐ(t)` | `mort_rate_mth(t)` | the monthly rate applied, `= 1 − (1 − q(t))^(1/12)` **[std]** |
| (table) | `mort_rate_base(t)` | this policy's own **sex-specific** first-order annual rate |
| `w(t)`, `σ(k)` | `lapse_rate(t)`, `storno_rate(k)` | **annual** surrender rate of the policy year; *Stornoabzug* rate at duration `k` |
| `wᵐ(t)` | `lapse_rate_mth(t)` | the monthly rate applied, `= 1 − (1 − w(t))^(1/12)` **[std]** |
| `l(t)` | `pols_if(t)` | policies in force at the **start** of month `t` |
| `α`, `β`, `γ`, `φ` | `alpha_rate`, `beta_rate`, `gamma_rate`, `prem_freq_load` | *Zillmersatz*; premium loading; sum-insured loading; *Ratenzahlungszuschlag*, 1.000 where `unterjaehrig_form = echt` |
| `B`, `BS`, `A` | `prem_gross_pp`, `beitragssumme`, `alpha_cost` | annual *Bruttobeitrag* before `φ`; *Beitragssumme* `= B × m`; zillmered acquisition cost `= zillmer_on × α × BS` |
| `P^n`, `P^Z` | `prem_net_level_pp`, `prem_zill_pp` | net level premium; Zillmer premium |
| `V(k)`, `V^n`, `V^Z`, `V^min` | `res_pp(k)`, `res_net_pp`, `res_zill_pp`, `res_min_pp` | *Deckungskapital* at the start of **policy year** `k`, and its three constructions |
| `G(k)` | `res_guar_pp(k)` | the § 169 guaranteed value at the **end** of policy year `k` |
| (closing) | `res_guar_close_pp(t)` | the same value **standing at the end of month `t`** — the one struck at the last anniversary |
| `RK(t)` | `surr_value_pp(t)` | *Rückkaufswert* actually payable on a surrender at the end of **month** `t` |
| `U(k)`, `Z(k)`, `S(k)` | `av_sur_pp(k)`, `bonus_si_pp(k)`, `term_bonus_pp(k)` | *Überschussguthaben*; bonus sum insured; accrued *Schlussüberschussanteil* |
| (closing) | `av_sur_close_pp(t)`, `bonus_si_close_pp(t)`, `term_bonus_close_pp(t)` | the same three standing at the end of month `t` |
| `d(k)`, `z(k)`, `a(k)`, `s(k)` | `decl_rate`, `zins_ueberschuss_rate`, `ans_rate`, `term_rate` | declared rate; interest-surplus rate; *Ansammlungszinssatz*; terminal rate |
| `C(k)` | `surplus_credit_pp(k)` | surplus allocated to the contract for policy year `k` |
| `r` | `instalments()` | premium instalments a policy year: 1 / 2 / 4 / 12, with `prem_cycle() = 12/r` and `prem_due(t)` |

`q₁`, `q`, `w`, `σ`, `d`, `z`, `a`, `s` are dimensionless annual rates; `SE`, `SD`, `B`, `V`, `U`,
`Z`, `S` are EUR per policy; every cash-flow component is EUR per policy year.

### The first-order basis and the pricing equivalence

First-order survival from issue and the two annuities-due, computed by summation on the model point's
own `sex` and `rechnungszins`:

```
tpx_1st(k)        = Π_{j=0}^{k-1} ( 1 − q₁(x_0 + j) ),  tpx_1st(0) = 1
pv_death_1st      = SD · Σ_{k=0}^{n-1} v₁^(k+1) · tpx_1st(k) · q₁(x_0 + k)
pv_maturity_1st   = SE · v₁^n · tpx_1st(n)
pv_benefit_1st    = pv_death_1st + pv_maturity_1st
ann_due_prem_1st  = Σ_{k=0}^{m-1} v₁^k · tpx_1st(k)
ann_due_term_1st  = Σ_{k=0}^{n-1} v₁^k · tpx_1st(k)
```

The *Bruttobeitrag* is struck by equivalence, which is linear in `B` because `BS = B · m`:

```
B · ann_due_prem_1st = pv_benefit_1st + α · B · m
                       + β · B · ann_due_prem_1st + γ · SE · ann_due_term_1st

⇒  prem_gross_pp = ( pv_benefit_1st + γ · SE · ann_due_term_1st ) / ( (1 − β) · ann_due_prem_1st − α · m )
```

`check_equivalence()` asserts that identity closes. **Note that the acquisition cost `α · BS` is in
the premium whether or not the contract is zillmered**: *Zillmerung* decides where the cost sits in the
**reserve**, not whether it is charged (`zillmer_on` enters `alpha_cost`, not the pricing equation).
That is why `zillmer_on` moves the reserve profile and the surrender values without moving
`prem_gross_pp` at all. The risk element carries the *Risikozuschlag*: `rating_factor` multiplies `q₁` in the
**death** leg of `pv_death_1st` only, never the survival leg, never the benefit, and never a
best-estimate rate (pitfall 12).

Then the two reserving premiums, and the zillmered cost:

```
beitragssumme     = prem_gross_pp · m
alpha_cost        = zillmer_on · alpha_rate · beitragssumme
prem_net_level_pp = pv_benefit_1st / ann_due_prem_1st
prem_zill_pp      = prem_net_level_pp + alpha_cost / ann_due_prem_1st
```

**Single premium.** `prem_term = 1` gives `ann_due_prem_1st = 1` and `BS = B`, so the 25 ‰
*Zillmersatz* buys almost nothing and the § 169 floor is slack from the first anniversary. That is
the correct answer, not a degenerate case.

### The Deckungskapital

Prospectively, at the start of year `t` (duration `k = t`), on the first-order basis, over the
remaining term and the remaining premium period:

```
pv_benefit_fut(t)    = SD · Σ_{j=0}^{n-k-1} v₁^(j+1) · jp(x(t)) · q₁(x(t)+j)  +  SE · v₁^(n-k) · (n-k)p(x(t))
ann_due_prem_fut(t)  = Σ_{j=0}^{max(0, m-k)-1} v₁^j · jp(x(t))

res_net_pp(t)   = pv_benefit_fut(t) − prem_net_level_pp · ann_due_prem_fut(t)
res_zill_pp(t)  = res_net_pp(t) − alpha_cost · ann_due_prem_fut(t) / ann_due_prem_1st
res_min_pp(t)   = res_net_pp(t) − alpha_cost · max(0, 1 − t / 5)
res_pp(t)       = res_zill_pp(t)                       while premium-paying
                = bfz_si_pp · pu_single_prem(t)        once paid-up
```

Three facts about those three lines. **`res_zill_pp(0) = −alpha_cost`** exactly: the *gezillmerte
Deckungskapital* is **negative at issue**, which is the arithmetic of [R28] and the reason § 169
Abs. 3 needs a floor at all. **How long it stays negative is a parameter question, not a structural
one**, and on the shipped basis the answer is under a year: 25 ‰ of a twenty-five-year
*Beitragssumme* is 0,625 of one annual premium, so the first Zillmer premium more than repays it and
the reserve is positive from the first anniversary (−1 252,53 € opening, +570,75 € closing, on the
anchor cell). Under the pre-2015 40 ‰ ceiling [R7] [REG-R16], or on a long term with a short
*Beitragszahlungsdauer*, it is negative for longer. **`res_min_pp` is that floor**, on the
straight-line reading of the five-year spreading. And **the floor normally binds**:
`ann_due_prem_fut(t)/ann_due_prem_1st` falls roughly linearly over `m` years while `max(0, 1 − k/5)`
reaches zero after five, so `res_min_pp(t) ≥ res_zill_pp(t)` at every duration on a long *gezillmert*
contract, with equality only at durations 0 and `m`. **A model publishing only the Zillmer reserve as
the surrender value understates it at essentially every duration; one publishing only the floor loses
the quantity the *Deckungsrückstellung* and the paid-up sum are built on** (pitfall 4). With
`zillmer_on = 0` all three coincide and the floor is slack — a useful invariance test.

### Rückkaufswert, Beitragsfreistellung and the paid-up sum

`G(t)` is struck at the **end** of policy year `t` — on the reserve at the start of year `t + 1` —
because that is what "zum Schluss der laufenden Versicherungsperiode" requires [R2]:

```
res_guar_pp(t)     = max( res_zill_pp(t+1), res_min_pp(t+1), 0 )
surr_value_pp(t)   = res_guar_pp(t) · (1 − storno_rate(t)) + av_sur_pp_at(t, "AFT_CREDIT")
                     + term_surr_share · term_bonus_pp(t+1)
pu_single_prem(t)  = SD/SE · Σ_{j} v₁^(j+1) · jp(x(t)) · q₁(x(t)+j)  +  v₁^(n-k) · (n-k)p(x(t))
bfz_si_pp          = res_guar_pp(e) / pu_single_prem(e + 1),   e = bfz_year − 1
```

`e = bfz_year − 1` is the **0-based index of the election year**: `bfz_year` is the contractual,
1-based policy year at whose end the election falls, so that end is the end of period `e` and the
start of period `e + 1 = bfz_year`.

`pu_single_prem(t)` is the first-order single premium for **one unit** of paid-up endowment over the
remaining term, so `bfz_si_pp` is the *beitragsfreie Versicherungssumme* the § 169 value will buy —
exactly what § 165 prescribes, "auf der Grundlage des Rückkaufswertes nach § 169 Abs. 3 bis 5" [R3].
Three rules ride on those four lines:

- **The *Stornoabzug* bites on the guaranteed value only**, not on the *Überschussguthaben*: Debeka's
  published deduction is a percentage of the *Deckungskapital* [S3] [R30] (pitfall 6).
- **`term_surr_share = 0` in the base run [std]** — the accrued *Schlussüberschussanteil* is paid at the
  *Ablauf* and on death, not on surrender (`product-spec.md`, footnote 12); the parameter is exposed.
- **The *Mindestversicherungsleistung* test**: if `bfz_si_pp < bfz_min_si` (**2,500 EUR [std]**) the
  election is **not** a *Beitragsfreistellung* — § 165 VVG obliges the insurer to pay the § 169 value
  instead, so the model converts the point to a **surrender at the end of year `e = bfz_year − 1`**
  and the projection terminates there [R3] (pitfall 8). Model point 12 exercises that branch.

Where the election succeeds the contract stays in force with `bfz_si_pp` in place of `SE`, no further
premium and a reserve `bfz_si_pp · pu_single_prem(t)`. Because the § 169 floor generally exceeds the
Zillmer reserve, the paid-up sum bought is worth more than the Zillmer reserve released; that
difference is `bfz_uplift_pp`, which enters the roll-forward identity so `check_res_roll_fwd()` still
closes in the election year.

### The Überschussbeteiligung

Declared annually, as a percentage of the *Deckungskapital*, allocated at the period end [S7] [S18]
[S9]:

```
zins_ueberschuss_rate(t) = max( 0, decl_rate(t) − rechnungszins )
surplus_base_pp(t)       = max( res_pp_at(t, "AFT_INT"), 0 )
surplus_credit_pp(t)     = zins_ueberschuss_rate(t) · surplus_base_pp(t)
term_bonus_pp(t+1)       = term_bonus_pp(t) + term_rate(t) · surplus_base_pp(t)
```

`res_pp_at(t, "AFT_INT")` is the closing guaranteed reserve of policy year `t`, before this year's
surplus is applied. That is a **[std]** reading of a base the wordings state three ways: Gothaer's
"maßgebliches Deckungskapital" is undefined in the wording [S7]; VPV takes the reserve "um ein Jahr mit
dem Rechnungszins abgezinst", i.e. an opening rather than a closing balance [S18]; and die Bayerische
accrues monthly on "das am Anfang des Monats vorhandene DECKUNGSKAPITAL (inklusive eines ggf. fälligen
Beitrags, abzüglich der zum Monatsbeginn fälligen Kosten)" [S9]. On a one-year grid the closing
balance is the natural annual analogue of a monthly accrual over the year, and the difference against
VPV's opening balance is one year's interest on the base. **The `max(0, ·)`
on the base is load-bearing**: the *gezillmerte Deckungskapital* is negative in the early years, and a
positive rate on a negative base would credit a negative surplus (pitfall 3). It follows that a
*gezillmert* contract earns **no** interest surplus in its first years even though § 153 entitlement
runs from inception where the wording grants it from inception [S9] — economically right, because
there is no fund to earn on, and worth saying
because it looks like a bug. **The `max(0, ·)` on the rate** is the other half: in the `nil` scenario the
declared rate is below the guarantee, which the reserve roll-forward still meets in full, so the surplus
is zero and not negative (pitfall 1).

Then the three *Überschussverwendung* systems:

```
ansammlung:           av_sur_pp(k+1)    = av_sur_pp(k) · (1 + ans_rate(k)) + surplus_credit_pp(k)
bonus:                bonus_si_pp(k+1)  = bonus_si_pp(k) + surplus_credit_pp(k) / pu_single_prem(k+1)
beitragsverrechnung:  prem_offset_pp(k) = min( prem_charged_pp(k), surplus_credit_pp(k-1) )   for k > k_start
                                        = 0                                                  at k = k_start
```

All three are **policy-year** ledgers, and the monthly grid does not subdivide any of them: the
declaration is an annual act.

Under `ansammlung` the surplus compounds at `ans_rate` and raises the maturity benefit; under `bonus`
it buys paid-up insurance at first-order rates, raising the **death** benefit immediately by the full
bonus sum but accumulating only at `rechnungszins`; under `beitragsverrechnung` it reduces the
*Zahlbeitrag* and neither balance grows. Because `ans_rate > rechnungszins` the first gives a higher
maturity benefit and the second a higher death benefit — **exactly the asymmetry [R28] states**, and
the test that distinguishes them (pitfall 15).

### Premium, decrements, benefits and cash flows

The annual amounts, with `k = duration(t)`:

```
prem_charged_pp(k) = prem_gross_pp · prem_freq_load        if k < prem_term and not is_paid_up(k)
                   = 0                                      otherwise
prem_paid_pp(k)    = prem_charged_pp(k) − prem_offset_pp(k)
```

and what is actually collected in a month, on the *Zahlweise*'s own cycle with `r = instalments`:

```
prem_due(t)             = 1{ t mod (12/r) = 0 }
prem_charged_inst_pp(t) = prem_charged_pp(k)/r · prem_due(t)
prem_inst_pp(t)         = prem_paid_pp(k)/r    · prem_due(t)
premiums(t)             = prem_inst_pp(t) · pols_if(t)

pols_death(t)      = pols_if(t) · mort_rate_mth(t)
pols_lapse(t)      = pols_if(t) · (1 − mort_rate_mth(t)) · lapse_rate_mth(t)
pols_maturity(t)   = pols_if(t) · (1 − mort_rate_mth(t))    at t = 12n − 1, else 0
pols_if(t+1)       = pols_if(t) − pols_death(t) − pols_lapse(t)

benefit_full_pp(t)     = sum_death + av_sur_close_pp(t) + bonus_si_close_pp(t)
                         + term_bonus_close_pp(t)
benefit_death_pp(t)    = (1 − suicide_share) · benefit_full_pp(t) + suicide_share · surr_value_pp(t)
                                                            for duration(t) < 3 (months 0–35),
                                                            else benefit_full_pp(t)
benefit_maturity_pp(N) = sum_assured + av_sur_close_pp(N) + bonus_si_close_pp(N)
                         + term_bonus_close_pp(N) + bwr_rate · res_guar_close_pp(N),   N = 12n − 1
surr_value_pp(t)       = res_guar_close_pp(t) · (1 − storno_rate(k)) + av_sur_close_pp(t)
                         + term_surr_share · term_bonus_close_pp(t)

claims(t, "DEATH")    = pols_death(t)    · benefit_death_pp(t)
claims(t, "MATURITY") = pols_maturity(t) · benefit_maturity_pp(t)
claims(t, "LAPSE")    = pols_lapse(t)    · surr_value_pp(t)

expenses(t)    = acq_expense · 1{t = t_start and duration_init = 0}
                 + maint_expense/12 · inflation_factor(k) · pols_if(t)
                 + claim_expense · ( pols_death(t) + pols_lapse(t) + pols_maturity(t) )
commissions(t) = comm_init_rate · beitragssumme · 1{t = t_start and duration_init = 0}
                 + comm_renew_rate · prem_charged_inst_pp(t) · pols_if(t)   for k > k_start
net_cf(t)      = premiums(t) − claims(t,"DEATH") − claims(t,"MATURITY") − claims(t,"LAPSE")
                 − expenses(t) − commissions(t) liability_cf(t)= − net_cf(t)
```

Three orientations worth naming. **`sum_death` is `sum_assured × death_ratio` and the surplus is added
to it whole** — the *Überschussguthaben*, the bonus sum and the accrued terminal bonus are payable on
death as well as at maturity [S11] [S16], so the two benefits differ only in their guaranteed leg.
**The renewal commission is charged on the instalment of `prem_charged_pp`, not of `prem_paid_pp`**:
under *Beitragsverrechnung* the intermediary is paid on the tariff premium, the surplus offset being a
policyholder rebate. And **every ``*_close_pp`` is the balance standing at the end of the month of
exit**, which is the year's own closing figure in an anniversary month and the previous anniversary's
in the other eleven — the rule stated under *Model scope and conventions*.

`result_cf()` is a `DataFrame` indexed by the **month** `t` (`df.index.name == "t"`), contiguous from
`t_start()` to `proj_len() − 1`, with columns **in this order**:

```
pols_if, premiums, claims_death, claims_maturity, claims_lapse, expenses, commissions, net_cf
```

A ninth column, `liability_cf`, is appended after `net_cf`: the library's conventions suite reads it
from the frame to assert `net_cf(t) == −liability_cf(t)`, so a published `liability_cf` cells with no
column would fail there. Every column but `pols_if` is a euro flow and the **six flow columns named
above** sum to `net_cf` exactly, which is what `check_net_cf()` asserts. Note the deliberate difference from frlib, where commission sits **inside**
`expenses` and is published beside it too: here `expenses` **excludes** commission, so summing the
columns gives `net_cf` rather than a double count. `result_cf_annual()` sums that frame into policy
years, indexed by the 1-based `policy_year`, with `pols_if` the count at the **start** of the year: a
regrouping of the same numbers and never a second projection, and the view the worked example below is
stated on. `result_surplus()` is a third frame reporting the surplus machinery — `decl_rate`,
`zins_ueberschuss_rate`, `surplus_base_pp`, `surplus_credit_pp`, `res_pp`, `av_sur_pp`,
`term_bonus_pp`, and `surr_value_pp` at that year's **anniversary** — which are state, not cash flow,
and are therefore kept out of `result_cf()`. It is **annual**, and deliberately so: what it publishes
moves once a year, and repeating each value twelve times would invite a reader to think a
*Deckungskapital* accrues through the year. What a mid-year surrender is paid is in `result_cf()`, and
is smaller.

### Published identities

Ten `check_*()` cells, each taking no argument, returning a `bool` and carrying a per-argument
residual at `check_*_resid`. **The residual's argument says which clock the identity lives on**: the
three that state an annual identity — the Fackler roll-forward, the surplus ledgers and the § 169
floor — take a policy year `k`; the other seven take a month `t`. The conventions suite calls every one
on every model point.

| Identity | What it asserts |
|---|---|
| `check_net_cf()` | **delib's first ruling.** `net_cf(t)` equals `premiums − claims_death − claims_maturity − claims_lapse − expenses − commissions`, rebuilt from `result_cf()`'s own published columns |
| `check_pols_roll_fwd()` | `pols_if(t+1) == pols_if(t) − pols_death(t) − pols_lapse(t)` in every **month**, and at `t = 12n − 1` the survivors of that month's mortality are exactly `pols_maturity(12n − 1)` |
| `check_decrement_closure()` | `Σ_t ( pols_death + pols_lapse + pols_maturity ) == pols_if_init()` |
| `check_res_roll_fwd()` | The Fackler recursion on the guaranteed *Deckungskapital*, per **policy year**: `( res_pp(k) + prem_zill_charged(k) ) · (1 + i₁) + bfz_uplift_pp(k) == f · q₁(x(k)) · sum_death + (1 − q₁(x(k))) · res_pp(k+1)`, where `q₁` is the unisex tariff rate and the *Risikozuschlag* `f` loads the death term only. This is the strongest single check in the model: it proves the premium, the first-order mortality, the interest and the prospective formula are mutually consistent |
| `check_surplus_roll_fwd()` | The active surplus vehicle's ledger closes, per **policy year**: `av_sur_pp(k+1) == av_sur_pp(k)·(1 + a(k)) + C(k)` under `ansammlung`, the bonus-purchase identity under `bonus`, and `prem_offset_pp(k) == min(prem_charged_pp(k), C(k−1))` under `beitragsverrechnung`, with `C(k−1)` read as zero at `k = k_start` |
| `check_surr_floor()` | § 169 Abs. 3, per **policy year**: `res_guar_pp(k) ≥ res_zill_pp(k+1)`, `≥ res_min_pp(k+1)` and `≥ 0`, and the *Rückkaufswert* at that year's anniversary `surr_value_pp(12k + 11) ≥ 0` |
| `check_surr_nonneg()` | The *Rückkaufswert* is non-negative in **every month**. Added with the monthly grid, which quotes one in the eleven months of each policy year the annual grid never priced — months paid on the **last** anniversary's § 169 value, which is a different and smaller number |
| `check_equivalence()` | The first-order pricing equivalence closes: `B·(1 − β)·ann_due_prem_1st − α·BS == pv_benefit_1st + γ·SE·ann_due_term_1st` |
| `check_rechnungszins_cap()`, `check_zillmer_cap()` | The two DeckRV cohort ceilings: `rechnungszins ≤ hoechstrechnungszins(issue_year)` under § 2 [REG-R14] [REG-R15], and `alpha_rate ≤ hoechstzillmersatz(issue_year)` with `alpha_cost ≤ hoechstzillmersatz · beitragssumme` under § 4 [R7] [REG-R16] |

The last two are parameter invariants rather than roll-forward identities, and they live here rather
than in a build script because a German model point's cohort **is** an assumption: a 4,00 % guarantee
on a 2026 issue year is not a stress, it is a data error.

### Processing order

Two loops, one inside the other. The **annual** one runs over `k = k_start() … n − 1` and is exactly
the order the annual-step model ran in; the **monthly** one runs over the twelve months of each policy
year and is what the frame publishes.

**The annual layer**, for policy year `k`:

1. **Open the year.** `x(k) = issue_age + k`; carry in `res_pp(k)`, `av_sur_pp(k)`, `bonus_si_pp(k)`,
   `term_bonus_pp(k)`, `is_paid_up(k)`.
2. **Decide whether a premium is due**: `k < prem_term` **and** not `is_paid_up(k)` — the `m` annual
   premiums fall in `k = 0 … m − 1`. Apply `φ` only where `unterjaehrig_form = unecht`.
3. **Apply the *Beitragsverrechnung* offset**, where elected: last year's declared surplus reduces this
   year's *Zahlbeitrag*, floored at zero. That fixes the year's annual `prem_paid_pp(k)`.
4. **Roll the guaranteed *Deckungskapital* forward** one year on the first-order basis — interest at
   `rechnungszins`, mortality release at the unisex tariff rate `mort_rate_at_age(x(k))` — to
   `res_pp_at(k, "AFT_INT")`, the closing guaranteed reserve. This is the **allocation-date**
   *Deckungskapital*.
5. **Declare and credit the surplus at the anniversary**: `z(k) = max(0, d(k) − i₁)`, base
   `max(res_pp_at(k, "AFT_INT"), 0)`, credit `C(k)`, and accrue `term_rate(k)` on the same base.
6. **Apply the surplus** per `surplus_use` — accumulate it, buy bonus sum insured, or carry it forward
   as next year's premium offset.
7. **The *Beitragsfreistellung* election**, where `k = bfz_year − 1`: strike `res_guar_pp(k)`, buy
   `bfz_si_pp`, and test it against `bfz_min_si` — **below the minimum the election becomes a
   surrender**, and it falls in that policy year's **last month**.
8. **Strike the § 169 value** `res_guar_pp(k)` at the year's end, and roll forward `res_pp(k+1)`,
   `av_sur_pp(k+1)`, `bonus_si_pp(k+1)`, `term_bonus_pp(k+1)`, `is_paid_up(k+1)`.

**The monthly layer**, for `t = t_start() … 12n − 1` with `k = duration(t)`:

1. **Open the month.** Carry in `pols_if(t)`; read the year's annual rates `q(t)` and `w(t)` and the
   monthly rates derived from them, `qᵐ(t)` and `wᵐ(t)`.
2. **Collect the premium instalment in advance**, where `prem_due(t)`:
   `premiums(t) = prem_inst_pp(t) × pols_if(t)`. A life that dies or surrenders later in the month
   **has already paid** that instalment; do not net it again (pitfall 11).
3. **Charge beginning-of-month expenses and commission** on the in-force: one twelfth of the
   maintenance expense, and the renewal commission on the instalment charged. The acquisition expense
   and the initial commission fall in month `t_start()`, and only for a new-business point — as single
   amounts, not twelfths.
4. **End of month, deaths** at the **best-estimate monthly** `qᵐ(t)`: the benefit is the guaranteed
   death sum plus the three surplus balances **standing at the end of that month**, with the § 161
   substitution of the *Rückkaufswert* on the suicide share for `duration(t) < 3` — the first
   thirty-six months.
5. **End of month, maturity or surrender.** At `t = 12n − 1` the survivors of that month's mortality
   mature and take the *Erlebensfallleistung*; the projection stops. Otherwise `wᵐ(t)` applies to the
   survivors of mortality and pays `surr_value_pp(t)`, on the § 169 value standing at the **last**
   anniversary.
6. **Roll forward** `pols_if(t+1)`.

The two layers meet at the anniversary, month `12k + 11`: the annual layer's step 5 credit and step 8
value are the balances the monthly layer's steps 4 and 5 pay in that month and in no other.

The annual layer's step order is the one thing a reader should check first. The surplus is declared on
the reserve **after** the year's interest, so a policy dying **at the anniversary** closing policy year
`k` receives that year's declared surplus — which follows the sources, the allocation being made at the
*Bilanzstichtag* to the contracts then in force [S9], and is the generous reading. A policy dying in
any of that year's other eleven months does **not**, and that is the conversion's own decision, stated
under *Model scope and conventions*: the declaration has not happened yet, so the balances standing are
the last anniversary's.

### Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each one is
a test in `tests/test_kapitallebensversicherung_de.py`.

1. **Adding the declared rate on top of the guarantee.** The ***laufende Verzinsung*** **is** the
   *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung* [REG-R53], so a declared 2,70 %
   on a 1,00 % guarantee is a **1,70 pp** surplus credit and not 2,70 pp on top of 1,00 pp. Assert
   `zins_ueberschuss_rate(k) == max(0, decl_rate(k) − rechnungszins)` in every policy year, and that on the
   `nil` scenario it is exactly 0 while the reserve still rolls forward at the full `rechnungszins`.
2. **Applying the surplus rate to the sum insured or to the premium.** The base is the
   ***Deckungskapital* at the allocation date** [S3]. Assert
   `surplus_credit_pp(k) == zins_ueberschuss_rate(k) · max(res_pp_at(k, "AFT_INT"), 0)` and that
   `surplus_credit_pp` is invariant to `sum_assured` **once the reserve is held fixed** — the quickest
   way to catch a `× sum_assured` where a `× res_pp` belongs.
3. **Crediting surplus on an un-floored negative reserve.** The *gezillmerte Deckungskapital* is
   negative at issue [R28]. Assert `surplus_base_pp(k) ≥ 0` in every policy year and that
   `surplus_credit_pp(k) == 0` wherever `res_pp_at(k, "AFT_INT") < 0`. **On the shipped 25 ‰ basis
   that set is empty**, because the base is the *closing* reserve and it is positive from policy year
   1 — so the assertion holds vacuously on every shipped model point, and it is stated here as what
   it is: a guard against a parameter this run does not use (the pre-2015 40 ‰ ceiling, or a long
   term with a short *Beitragszahlungsdauer*), not a behaviour the base run exhibits. The test should
   therefore also assert the guard directly, by evaluating the credit against a negative base.
   **Entitlement from inception [S9] does not mean a positive credit from inception.**
4. **Implementing one reserve where the product has three.** `res_zill_pp` is what the insurer
   reserves, `res_min_pp` is the § 169 Abs. 3 floor and **normally binds**, and `res_guar_pp` is their
   maximum and what the customer gets. Assert `res_guar_pp(k) ≥ res_zill_pp(k+1)` and `≥ res_min_pp(k+1)`
   in every policy year, that the floor is **strictly** binding at some duration on the anchor cell, and
   that on model point 13 (`zillmer_on = 0`) all three coincide.
5. **Conflating the § 169 five-year spreading with the § 4 DeckRV 25 ‰ cap.** § 169 Abs. 3 VVG fixes
   **how** the acquisition cost is spread for the surrender floor — a floor on the **value** — while
   § 4 DeckRV fixes **how much** may be zillmered at all — a cap on the **charge** [R2] [R7] [REG-R16]
   [REG-R28] (gap 5). Assert `check_zillmer_cap()` against the cohort ceiling **and**
   `check_surr_floor()` against the five-year schedule, separately.
6. **Deducting the *Stornoabzug* from the *Überschussguthaben*.** Debeka's published deduction is a
   percentage of the *Deckungskapital* [S3] [R30]. Assert
   `surr_value_pp(t) − av_sur_close_pp(t) == res_guar_close_pp(t) · (1 − storno_rate(duration(t)))` in
   **every month** of the base run, so the accumulated surplus passes through undeducted — and note
   that the deduction band is a **policy-year** band and steps on the anniversary while the value it
   bites on is the one standing at the end of the month.
7. **Paying nil on a suicide inside the three-year window.** § 161 VVG makes the insurer
   *leistungsfrei* **and** obliges it to pay the *Rückkaufswert* including *Überschussanteile* under
   § 169 [R4] [REG-R26]: the German rule is a **benefit substitution**, not a forfeiture, unlike art.
   L. 132-7 of the French code. Assert
   `benefit_death_pp(t) == 0.98 · benefit_full_pp(t) + 0.02 · surr_value_pp(t)` for `duration(t) < 3`
   — policy years 1 to 3, the first **thirty-six months**, the window being measured in whole years so
   that its boundary falls on an anniversary — and `== benefit_full_pp(t)` from month 36, and that
   `benefit_death_pp(0) > 0` even where `surr_value_pp(0)` is nil, which on a *gezillmert* contract it
   is through the whole first policy year.
8. **Offering *Beitragsfreistellung* without the *Mindestversicherungsleistung* test.** § 165 VVG makes
   the election a **surrender** where the minimum is not reached [R3]. Assert that model point 11
   (`bfz_year = 10`) continues in force to `proj_len() − 1` with `prem_paid_pp(k) == 0` from `k = 10`
   — the election falls at the end of policy year 10, `k` = 9, month 119 — and that model point 12
   (`bfz_year = 3`, small sum) instead **terminates in month 35** with a `claims_lapse` payment and
   nothing thereafter. That month, and not the first month of the election year, is where
   `lapse_rate_mth` places the statutory 1.0: the election falls at the end of a *Versicherungsperiode*
   and spreading an annual 1.0 geometrically would empty the cohort eleven months early.
9. **Removing the paid-up policy from `pols_if`.** *Beitragsfreistellung* keeps the contract alive with
   a reduced sum insured [R3] [S7]; only a *Kündigung* removes it. Assert `pols_if(t)` is unaffected by
   `bfz_year` on model point 11 relative to the anchor, while `prem_paid_pp` and
   `benefit_maturity_pp` both fall.
10. **Calibrating the surrender decrement to GDV's headline *Stornoquote*.** The GDV publishes one
    figure, "Die Stornoquote (Anzahl) stieg im Jahr 2023 leicht auf 2,56 % (Vorjahr: 2,51 %)" [R20]:
    a **count** measure over all German life business, not a surrender rate, not endowment-specific
    and not split by duration. It is the wrong quantity in three ways at once, and duration is the one
    that bites hardest — BaFin's finding is that lapse is concentrated "speziell in den ersten Jahren
    nach Vertragsabschluss" [R18], which no single annual average can express. Assert that
    `lapse_rate` comes from `lapse_table.csv`, that it is the **annual** rate of the policy year and is
    flat across its twelve months, that twelve of `lapse_rate_mth` compound back to it exactly, and
    that its provenance column says [std], not [R20].
11. **Double-counting the premium-cessation rule.** Premiums are in advance and decrements are at the
    period end, so a decedent has already paid the year's premium. The rule behind this is contract
    termination, not a special clause: in the ordinary endowment the death payment ends the contract
    ("Mit der Auszahlung endet der Vertrag") and no further premium can fall due [S7] § 3 I (5). The
    express stipulation "Bei Tod der versicherten Person vor dem Ablauftermin werden keine Beiträge
    mehr fällig" belongs to the *Termfixversicherung* [S7] § 3 II, where the benefit is payable at the
    fixed date irrespective of survival and the contract does **not** end on death — the one variant
    where premium cessation has to be said. Assert
    `premiums(t) == prem_inst_pp(t) · pols_if(t)` with **no** `(1 − qᵐ)` factor. The finer grid narrows
    the error — 0,15 € in month 0 against 1,80 € in the first policy year on the annual grid — without
    removing the trap: there are now twelve times as many chances to apply it.
12. **Letting the *Risikozuschlag* reach the wrong quantity.** `rating_factor` scales the first-order
    mortality in the **death** leg of the pricing only [R5]. Assert that `benefit_death_pp` is invariant
    to `rating_factor`, that `mort_rate(t)` (the best estimate) is invariant to it, and that
    `prem_gross_pp` rises with it.
13. **Using one mortality table as if it were prudent for both legs.** The direction of prudence forks:
    a death benefit wants mortality assumed **higher** than expected, a survival benefit **lower**
    [REG-R47] [REG-R48]. The model uses one first-order table for both and says so; assert that the
    single table is in fact used for both legs, so the compromise stays visible.
14. **Crossing the first- and second-order bases.** `mort_rate_at_age` prices and reserves, on the
    unisex blend; `mort_rate_base` is this policy's own sex-specific table rate and `mort_rate`
    projects. Assert `mort_rate(t) == mort_rate_base(t) · mort_be_factor` with
    `mort_be_factor = 0.75`, that `res_pp` is invariant to `mort_be_factor`, and that `pols_death`
    moves with it. A model that reserves on the best estimate has thrown away the *Sicherheitszuschlag*
    that is the source of the *Risikoüberschuss* [REG-R47].
15. **Expecting the two surplus systems to give the same benefits.** "Compared with the *Bonussystem*,
    the *verzinsliche Ansammlung* leads to a higher payment at maturity, while the *Bonussystem*
    produces higher death benefits" [R28]. Assert exactly that between model point 1 (`ansammlung`) and
    model point 8 (`bonus`). It holds because `ans_rate > rechnungszins`, and a model that sets them
    equal fails it — correctly.
16. **Treating the *Zahlbeitrag* as guaranteed.** Under *Beitragsverrechnung* the policyholder pays the
    *Bruttobeitrag* less a **discretionary** surplus offset, withdrawable without invoking § 163 VVG at
    all [REG-R27] [REG-R53]. Assert on model point 9 that `prem_paid_pp(t) < prem_charged_pp(t)` while
    surplus is being declared, that `prem_charged_pp(t)` is unchanged from the anchor, and that on the
    `nil` scenario the offset is zero and the two coincide.
17. **Letting `sex` into the premium.** Unisex since 21 December 2012 [REG-R34]. Assert that
    `prem_gross_pp` is identical for two otherwise-identical model points differing only in `sex`
    (points 1 and 7 both price at 2 004,0420 €), while `mort_rate` differs. This is why the pricing
    reads `mort_rate_at_age`, the fixed unisex portfolio blend — itself **[std]** — and not
    `mort_rate_base`, which is the policy's own row; reading one where the other belongs is silent,
    and it moved the anchor's premium by 9,15 € when it was first written that way.
18. **Running past the *Ablauf*, or letting a final-year surrender collide with the maturity.**
    `proj_len() = 12 · policy_term` is the frame's **exclusive** end, so the last row is
    `t = proj_len() − 1` and there is no `t = proj_len()` row. `lapse_rate` is 0 through the whole last
    **policy year** **[std]**,
    so the survivors of that last month's mortality all leave as a maturity — and unlike a term product
    the two exits do **not** pay the same thing, a surrender paying the § 169 value and a maturity the
    sum insured plus surplus, so this is a real payment decision. Assert
    `lapse_rate(t) == 0` through months `12(n − 1) … 12n − 1`,
    `pols_maturity(12n − 1) == pols_if(12n − 1) · (1 − mort_rate_mth(12n − 1))`, and closure to 1e-12.

---

## Policyholder behaviour modelling

All formulas are **[std]**; no German calibration evidence exists for any of them.

- **Base surrender.** The duration table above: shape driven by the tax thresholds — twelve years and
  age 60 or 62 [R10] [REG-R45] — levels unsourced. The anchor cell's *Ablauf* at attained age 62 makes
  the two thresholds coincide, which is why a German buyer is sold that term and why the surrender rate
  collapses in the run-up to it.
- **The *Beitragsfreistellung* election is deterministic** — a model-point column, not a decrement.
  The corpus establishes the right in full [R3] and gives **no take-up rate at all**, and the one
  aggregate that would bear on it mixes the paid-up route in with surrenders and cannot be split [R20].
  Modelling it as a scheduled election keeps the unsourced number out of the base run; what that costs
  is stated — a real book converts a material, duration-dependent share to *beitragsfrei*, and this
  model shows that path only where a model point elects it.
- **Two dynamic modules, both [std] and both off in the base run.** *Premium-shock lapse* is inert on
  the base contract, whose *Bruttobeitrag* is level, but live under *Beitragsverrechnung*, where a fall
  in the declared rate raises the *Zahlbeitrag*: `M_shock(k) = 1 + β_shock · max(0,
  prem_paid_pp(k)/prem_paid_pp(k−1) − 1 − g0)` on the **annual** *Zahlbeitrag* of consecutive policy
  years, `g0 = 0.05`, `β_shock = 1.5`, base run `β_shock = 0`.
  *Rate-gap lapse* keys on the gap between the declared rate and what is available elsewhere:
  `lapse_add(k) = a · max(0, ref_rate − decl_rate(k) − tol)`, `a = 3.0`, `tol = 0.5 pp`, `ref_rate` a
  model Reference, base run `a = 0`. Both compare **annual** declarations, which is what they are
  about; neither becomes a monthly comparison. **No German calibration of any of these numbers exists in the
  corpus**, which is why both ship off. **Selective lapsation is not modelled** either: surrenders on
  an endowment are wealth- and tax-driven rather than health-driven.
- **What the model deliberately does not do.** No premium-default path (§§ 37/38 VVG unresearched, gap
  20); no *Widerruf* decrement (§ 152 VVG unresearched); no dynamic *Beitragsverrechnung* take-up; and
  no management action on the declared rate — the rate is a scenario, and the RfB and its
  *Schlussüberschussanteilfonds* [REG-R54] that would smooth it are outside this model.

---

## Worked example

**Configuration.** Model point 1, the anchor cell of `model_point_table.csv`: `policy_id`
`DE-KLV-0001`; `sex` **M**; `smoker` **N**; `issue_year` **2026**; `issue_age` **37**;
`duration_init` **0**, so `t_start() = 0` and the projection opens at issue; `pols_if_init` **1.0**;
`policy_term` **25**, so `proj_len_y() = 25` and `proj_len() = 300`, the frame is `t` = 0 … 299
**months** and the annual table below — the monthly frame summed into policy years — is the
**entire** projection, with the
*Ablauf* at attained age **62** — the age the half-income tax rule requires for a contract concluded
after 31 December 2011 [R10] [REG-R45]; `prem_term` **25**, the full term, so the contract is
premium-paying to the *Ablauf*; `sum_assured` **50,000.00 EUR**; `death_ratio` **1.00**, so the
guaranteed death sum equals the guaranteed survival sum and the contract is the *gemischte Versicherung
auf den Todes- und Erlebensfall* proper; `prem_freq` **annual** and `unterjaehrig_form` **unecht**, so
`prem_freq_load = 1.000` and the *Ratenzahlungszuschlag* is inert; `rechnungszins` **1.00%**, the
*Höchstrechnungszins* for new business written from 1 January 2025 [R7] [REG-R15]; `zillmer_on` **1**;
`cost_id` **`std_2026`**; `surplus_use` **`ansammlung`**; `scenario_id` **`base`**; `rating_factor`
**1.00**; `av_sur_pp_init` **0.00**; `bonus_si_init` **0.00**; `bfz_year` **0**, so no
*Beitragsfreistellung* is elected. The *Bruttobeitrag* is **not** a model point column: it is derived
by the equivalence principle above and reported in the table, because **no German endowment premium
rate table is public, for any carrier** (gap 16).

**Assumptions, each tagged.** *First order.* Interest `i₁ = 1.00%` [R7] [R15] [REG-R14] [REG-R15].
Mortality `mort_rate_1st(M, x) = 0.00022 + B · 1.10^x`, `B` fixed by the anchor
`mort_rate_1st(M, 37) = 0.001200` exactly **[std]**, standing in for **DAV 2008 T**, which is not
public and is not shipped [R14] [REG-R47] [REG-R48]; the tariff prices and reserves on the **unisex
blend** `mort_rate_at_age(37) = ½ · 0.001200 + ½ · 0.000896288505 = 0.001048144253` **[std]**
[REG-R34], and the anchor cell's own decrement is `mort_rate(0) = 0.001200 × 0.75 = 0.000900`. *Zillmersatz* `alpha_rate = 25 ‰` of the
*Beitragssumme* — the § 4 DeckRV ceiling [R7] [REG-R16], the level **[std]**. Premium loading
`beta_rate = 3.0%` of the *Bruttobeitrag* over the *Beitragszahlungsdauer* — the form is the one the
corpus establishes [R28], the level **[std]**. Sum loading `gamma_rate = 1.5 ‰` of the
*Versicherungssumme* p.a. over the *Versicherungsdauer* — **the form itself is not established** (gap
17) and both form and level are **[std]**. *Ratenzahlungszuschlag* `prem_freq_load = 1.000` on the
annual mode [R28].

*Insurer-discretionary.* Declared *laufende Verzinsung* `decl_rate = 2.70%` p.a. level — Allianz's
**2025** declaration for its combined classic life-and-annuity book as reported by the trade press
[R26], the nearest thing in the corpus to a manufacturer figure touching an endowment book, the
level-forever assumption **[std]**; hence `zins_ueberschuss_rate = max(0, 2.70% − 1.00%) = 1.70%`, **derived and
never added on top of the guarantee** [REG-R53]. *Schlussüberschussanteilsatz* `term_rate = 0.40%` p.a.
of the *Deckungskapital*, accrued and paid at the *Ablauf* and on death, **not** on surrender
(`term_surr_share = 0`) — **[std]**, no rate of any kind having been established (gap 1).
*Ansammlungszinssatz* `ans_rate = 2.70%`, equal to the declared rate — **[std]**. *Stornoabzug*
`storno_rate` 10% of the guaranteed value in policy years 1–5, 7.5% in 6–10, 5% in 11–15 and 2.5% from
16 — **[std]**, against three observed carrier schedules on three incompatible bases: 0–20 % of the
*Deckungskapital*, decaying to nil over the last ten years, at Debeka and under collective action
after a BGH remittal [S3] [R22] [R30]; 50 € + 0,15 % of premiums paid times the years remaining at die
Bayerische [S9]; and 100 € + 0,2 % of the gap between sum insured and *Rückkaufswert* at VPV [S18]. *Bewertungsreserven* `bwr_rate = 0.00%` —
**[std]** [R1] [R8] [REG-R9].

*Second order.* Mortality `mort_rate(t) = mort_rate_base(t) × 0.75` on this policy's own
sex-specific row, `mort_be_factor = 0.75` **[std]**
— a 33 % first-order safety loading, whose systematic release is the *Risikoüberschuss* [REG-R47].
Surrender `lapse_rate` 5.0% in policy years 1–2, 3.5% in 3–8, 2.0% in 9–11, **6.0% in policy year 12**
— the twelve-year tax threshold [R10] [REG-R45] — 2.5% from policy year 13, and **0 through the whole
of policy year 25**, the *Ablauf* year — all **[std]** and all **annual**, no endowment-specific or
duration-specific German lapse rate having been established (gap 10); the schedule is keyed by the
1-based `policy_year(t) = duration(t) + 1`, and each annual rate is spread to the month at
`1 − (1 − w)^(1/12)` **[std]**.
Suicide share `suicide_share = 0.02` for policy years 1 to 3, with the
*Rückkaufswert* substituted for the sum insured on that share [R4] [REG-R26] — the **first
thirty-six months** on the monthly frame, the window being measured in whole years so that its
boundary falls on an anniversary — the share **[std]**.
Expenses **[std]** throughout: `acq_expense = 300.00 EUR` at issue, `comm_init_rate = 2.5%` of the
*Beitragssumme* at issue — set at the 25 ‰ *zillmering* ceiling [R7], which does not cap commission
[R29], and with **no carrier commission rate established anywhere in the corpus** — `maint_expense = 45.00 EUR` per in-force policy p.a. inflating at `expense_infl = 1.8%` p.a.,
`comm_renew_rate = 1.5%` of the *Bruttobeitrag* from year 2, and `claim_expense = 120.00 EUR` per
death, maturity or surrender claim. No behaviour modules: `β_shock = 0`, `a = 0`.

All amounts in euros; `pols_if` to six decimals, cash flows and balances to the cent. Totals are summed
**at full precision and then rounded**, not summed from the rounded cells.

**The derived tariff.** The equivalence gives a *Bruttobeitrag* of **2 004,04 €** a year, a
*Beitragssumme* of **50 101,05 €**, `alpha_cost` **1 252,53 €**, `prem_net_level_pp`
**1 811,15 €** and `prem_zill_pp` **1 868,92 €**, on `pv_death_1st` = 3 611,698493 €,
`pv_maturity_1st` = 35 655,282574 € and `ann_due_prem_1st` = `ann_due_term_1st` = 21,680698 —
the two annuities coinciding because the *Beitragszahlungsdauer* is the whole
*Versicherungsdauer*.

### The projection, policy year by policy year

Transcribed from `KLV_DE_S.Projection[1].result_cf_annual()`, the monthly frame summed into policy
years. `pols_if` is the count at the **start** of the policy year — the number the annual-step model
carried on the same row, unchanged by the conversion; every other column is that year's euro flow.
`expenses` **excludes** commission, so the six flow columns sum to `net_cf` exactly. The table is the
whole contract, policy years 1 to 25.

| policy year | age | pols_if | premiums | claims_death | claims_maturity | claims_lapse | expenses | commissions | net_cf |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 37 | 1.000000 | 2,004.04 | 43.08 | 0.00 | 2.88 | 350.04 | 1,252.53 | 355.51 |
| 2 | 38 | 0.949145 | 1,902.13 | 44.26 | 0.00 | 40.88 | 48.26 | 28.53 | 1,740.20 |
| 3 | 39 | 0.900810 | 1,805.26 | 45.90 | 0.00 | 86.60 | 45.20 | 27.08 | 1,600.47 |
| 4 | 40 | 0.868365 | 1,740.24 | 49.00 | 0.00 | 142.18 | 44.30 | 26.10 | 1,478.66 |
| 5 | 41 | 0.837014 | 1,677.41 | 51.41 | 0.00 | 195.02 | 43.41 | 25.16 | 1,362.41 |
| 6 | 42 | 0.806716 | 1,616.69 | 54.04 | 0.00 | 251.21 | 42.54 | 24.25 | 1,244.66 |
| 7 | 43 | 0.777431 | 1,558.00 | 56.89 | 0.00 | 293.79 | 41.68 | 23.37 | 1,142.27 |
| 8 | 44 | 0.749121 | 1,501.27 | 60.00 | 0.00 | 334.28 | 40.84 | 22.52 | 1,043.63 |
| 9 | 45 | 0.721747 | 1,446.41 | 63.83 | 0.00 | 213.02 | 38.97 | 21.70 | 1,108.90 |
| 10 | 46 | 0.706081 | 1,415.02 | 68.58 | 0.00 | 237.51 | 38.78 | 21.23 | 1,048.91 |
| 11 | 47 | 0.690646 | 1,384.08 | 73.79 | 0.00 | 268.03 | 38.60 | 20.76 | 982.91 |
| 12 | 48 | 0.675431 | 1,353.59 | 78.01 | 0.00 | 876.44 | 40.95 | 20.30 | 337.88 |
| 13 | 49 | 0.633469 | 1,269.50 | 82.09 | 0.00 | 378.76 | 36.95 | 19.04 | 752.66 |
| 14 | 50 | 0.616105 | 1,234.70 | 88.23 | 0.00 | 404.57 | 36.56 | 18.52 | 686.82 |
| 15 | 51 | 0.599079 | 1,200.58 | 94.94 | 0.00 | 429.56 | 36.17 | 18.01 | 621.91 |
| 16 | 52 | 0.582376 | 1,167.11 | 102.28 | 0.00 | 464.10 | 35.77 | 17.51 | 547.45 |
| 17 | 53 | 0.565979 | 1,134.25 | 110.30 | 0.00 | 487.85 | 35.37 | 17.01 | 483.71 |
| 18 | 54 | 0.549875 | 1,101.97 | 119.08 | 0.00 | 510.74 | 34.97 | 16.53 | 420.66 |
| 19 | 55 | 0.534048 | 1,070.25 | 128.67 | 0.00 | 532.76 | 34.56 | 16.05 | 358.22 |
| 20 | 56 | 0.518483 | 1,039.06 | 139.15 | 0.00 | 553.89 | 34.14 | 15.59 | 296.29 |
| 21 | 57 | 0.503165 | 1,008.36 | 150.61 | 0.00 | 574.14 | 33.71 | 15.13 | 234.78 |
| 22 | 58 | 0.488079 | 978.13 | 163.12 | 0.00 | 593.48 | 33.28 | 14.67 | 173.58 |
| 23 | 59 | 0.473210 | 948.33 | 176.78 | 0.00 | 611.91 | 32.84 | 14.22 | 112.58 |
| 24 | 60 | 0.458543 | 918.94 | 191.69 | 0.00 | 629.39 | 32.39 | 13.78 | 51.69 |
| 25 | 61 | 0.444064 | 889.92 | 210.36 | 28,750.90 | 0.00 | 83.85 | 13.35 | -28,168.54 |
| **Total** | | **16.648981** | **33,365.26** | **2,446.09** | **28,750.90** | **9,112.99** | **1,314.12** | **1,722.94** | **-9,981.79** |

**The Total row is summed at full precision and then rounded, not summed from the rounded cells
above it**, and on this cell the two differ. Adding the printed column gives 33,365.24 for
`premiums` against 33,365.26, 1,314.13 for `expenses` against 1,314.12 and −9,981.78 for `net_cf`
against −9,981.79 — the accumulation of twenty-five roundings of at most half a cent each.
`pols_if` behaves the same way: 16.648981 at full precision against 16.648982 from the printed
column. The other columns agree to the cent. Where a reader needs the totals to reconcile with
the printed cells rather than with the model, it is the printed cells that are the approximation.

### The first policy year, month by month

The view the annual grid could not show, from `result_cf()`. Month 0 collects the whole year's
*Beitrag* — this cell is an annual payer — and bears the acquisition expense and the initial
commission; the other eleven collect nothing, carry a death claim and a twelfth of the maintenance
expense, and **pay a surrender nothing guaranteed**: the § 169 value standing before the first
anniversary is the one struck at issue, which on a *gezillmert* contract is zero. Only month 11
carries a surrender claim at all.

| t | pols_if | premiums | claims_death | claims_lapse | expenses | commissions | net_cf |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000000 | 2,004.04 | 3.68 | 0.00 | 304.27 | 1,252.53 | 443.57 |
| 1 | 0.995660 | 0.00 | 3.66 | 0.00 | 4.25 | 0.00 | -7.91 |
| 2 | 0.991339 | 0.00 | 3.64 | 0.00 | 4.23 | 0.00 | -7.88 |
| 3 | 0.987036 | 0.00 | 3.63 | 0.00 | 4.22 | 0.00 | -7.84 |
| 4 | 0.982753 | 0.00 | 3.61 | 0.00 | 4.20 | 0.00 | -7.81 |
| 5 | 0.978487 | 0.00 | 3.60 | 0.00 | 4.18 | 0.00 | -7.78 |
| 6 | 0.974241 | 0.00 | 3.58 | 0.00 | 4.16 | 0.00 | -7.74 |
| 7 | 0.970012 | 0.00 | 3.57 | 0.00 | 4.14 | 0.00 | -7.71 |
| 8 | 0.965803 | 0.00 | 3.55 | 0.00 | 4.12 | 0.00 | -7.68 |
| 9 | 0.961611 | 0.00 | 3.54 | 0.00 | 4.11 | 0.00 | -7.64 |
| 10 | 0.957438 | 0.00 | 3.52 | 0.00 | 4.09 | 0.00 | -7.61 |
| 11 | 0.953282 | 0.00 | 3.51 | 2.88 | 4.07 | 0.00 | -10.46 |
| **Year 1** | 1.000000 | **2,004.04** | **43.08** | **2.88** | **350.04** | **1,252.53** | **355.51** |

The shape is worth naming. The first policy year very nearly washes — **+355,51 €** — the *Beitrag*
of 2 004,04 € almost exactly meeting the initial commission of 1 252,53 € plus the 300 €
acquisition expense, so **the new-business strain of a *gezillmert* German endowment is in the
reserve and not in the cash flow**: the *Deckungskapital* opens at −1 252,53 €. The margin then
runs near a thousand euros a year and decays with the cohort, dipping visibly in policy year 12 —
337,88 € against 982,91 € — where the surrender rate spikes to 6,0 % at the twelve-year tax
threshold. The last year is a single outflow of **−28 168,54 €**.

### The state behind it

The same projection's *Deckungskapital*, its surplus and what a surrender would pay, at ten
durations, from `result_surplus()`. `res_pp(t)` is the guaranteed reserve at the **start** of
year `t`; `surplus_base_pp(t)` is the same reserve at the **end** of that year, which is the
*Deckungskapital* at the allocation date; `surr_value_pp(t)` is what a surrender at the end of
year `t` receives.

| t | res_pp | surplus_base_pp | surplus_credit_pp | av_sur_pp | term_bonus_pp | surr_value_pp |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | -1,252.53 | 570.75 | 9.70 | 0.00 | 0.00 | 708.73 |
| 1 | 570.75 | 2,410.10 | 40.97 | 9.70 | 2.28 | 2,590.38 |
| 2 | 2,410.10 | 4,265.63 | 72.52 | 50.94 | 11.92 | 4,518.89 |
| 4 | 6,137.47 | 8,025.74 | 136.44 | 232.53 | 53.54 | 8,521.62 |
| 9 | 15,747.00 | 17,720.63 | 301.25 | 1,321.31 | 290.92 | 18,779.50 |
| 11 | 19,712.27 | 21,722.40 | 369.28 | 2,038.12 | 440.65 | 23,755.21 |
| 14 | 25,800.39 | 27,869.68 | 473.78 | 3,450.48 | 725.75 | 31,007.41 |
| 19 | 36,372.42 | 38,561.55 | 655.55 | 6,811.60 | 1,367.70 | 45,521.12 |
| 23 | 45,313.89 | 47,636.03 | 809.81 | 10,540.47 | 2,038.44 | 58,136.33 |
| 24 | 47,636.03 | 50,000.00 | 850.00 | 11,634.87 | 2,228.98 | 61,549.01 |

Two rows carry the product. At `t` = 0 the reserve is **−1 252,53 €** — exactly `−alpha_cost`,
the whole *Zillmerung* unrecovered — while the *closing* reserve the surplus is declared on is
already **570,75 €**, so the credit is a small positive 9,70 € rather than the negative amount
an un-floored base would have produced from the opening figure. At `t` = 24 the closing reserve
is **50 000,00 €** exactly: the last year's *Deckungskapital* **is** the *Erlebensfallleistung*.

### Three independent checks, and a closure identity

Each rebuilds a cell of the tables above a **different way**, in arithmetic a reader can follow
on a calculator. None of them re-runs the model's own path to the number.

**1. The *Bruttobeitrag*, from the equivalence.** The premium is not an input; it is the
solution of `B (1 − β) ä_m − α B m = pv_benefit_1st + γ SE ä_n`. Numerator:
`pv_benefit_1st` = 3 611,698493 + 35 655,282574 = **39 266,981067**, plus
`γ SE ä_n` = 0,0015 × 50 000 × 21,680698 = **1 626,052368**, giving **40 893,033435**.
Denominator: 0,97 × 21,680698 = 21,030277, less 0,025 × 25 = 0,625, giving **20,405277**.
Then 40 893,033435 ÷ 20,405277 = **2 004,0420 €**, the table's *Bruttobeitrag*. The two
reserving premiums follow without touching the projection: `prem_net_level_pp` =
39 266,981067 ÷ 21,680698 = 1 811,1493 €, and `prem_zill_pp` = 1 811,1493 + 1 252,5263 ÷
21,680698 = 1 811,1493 + 57,7715 = **1 868,9208 €**.

**2. The reserve at the first anniversary, by Fackler.** The state table gives
`res_pp(1)` = 570,75 € *prospectively*, as a present value of what remains. Rebuild it
*retrospectively*, forwards from the opening reserve. The unisex first-order rate at age 37 is
½ × 0,001200000000 + ½ × 0,000896288505 = **0,001048144253**. Then
(−1 252,5263 + 1 868,9208) × 1,01 = 616,3945 × 1,01 = **622,5584**; deduct the year's death
outgo 0,001048144253 × 50 000 = **52,4072**; divide the remaining 570,1512 by the survivors
1 − 0,001048144253 = 0,998951856, and the answer is **570,7495 €**. The two agree to eight
figures, which is what `check_res_roll_fwd()` asserts in every policy year — and it is the strongest
statement in the model, because it holds only if the premium, the first-order mortality, the
*Rechnungszins* and the prospective formula are mutually consistent.

**3. The surplus credited in policy year 2 (`k` = 1), and the *Überschussguthaben* it builds.** The declared
rate is 2,70 % and the guarantee 1,00 %, so `zins_ueberschuss_rate` = **1,70 pp** — derived by
subtraction, never added on top. The base is that year's *closing* reserve, 2 410,101960 €, so
the credit is 0,017 × 2 410,101960 = **40,9717 €**, the state table's figure. It then compounds:
`av_sur_pp(2)` = 9,702741 × 1,027 + 40,971733 = 9,964715 + 40,971733 = **50,9364 €**, and the
terminal share accrues on the same base, `term_bonus_pp(2)` = 2,282998 + 0,004 × 2 410,101960 =
2,282998 + 9,640408 = **11,9234 €**. Both match the table to the cent.

**4. The policy-year-12 surrender payment, from its three parts.** Policy year 12 is `k` = 11,
months 132 to 143, and `claims_lapse` over it is 876,44 € — the one year where the § 169 floor, the
*Stornoabzug* and the surrender spike all bite at once. Count: the 0,675431 in force at the start
of the year decrement month by month at the 6,0 % annual spike spread to
`1 − 0,94^(1/12)`, giving **0,04047664** surrenders over the twelve months, against 0,04043417 on
the annual grid — the difference being the monthly interleaving of the two decrements. Amount, at
the **anniversary**: the § 169 value at the end of that year is the **floor**, `res_min_pp(12)` =
22 413,4564 €, which exceeds the Zillmer reserve `res_zill_pp(12)` = 21 722,3990 € by **691,06 €**
— the floor is binding, and this is what a model publishing only the Zillmer reserve would lose.
Apply the 5 % *Stornoabzug* to that and nothing else: 22 413,4564 × 0,95 = 21 292,7836 €, then add
the *Überschussguthaben* **undeducted**, 2 462,4255 €, for a *Rückkaufswert* of **23 755,2091 €**.
The eleven other months are paid the value struck at the **previous** anniversary, 21 467,9479 €,
which is why the year's claim is 876,44 € and not 960,52 €.

**The closure identities.** Over the whole projection the cohort accounts for itself exactly:
deaths **0,04355790**, surrenders **0,51566656** and maturities **0,44077554** sum to
**1,000000000000** — `check_decrement_closure()`. The maturing cohort is the annual-step model's
own figure to the last digit, lapse being zero through the whole final policy year under either
grid; the split between the first two moved by 0,00054, which is what interleaving the two
decrements monthly genuinely changes. And the cash flow statement closes row by row; summed over
policy year 12, 1 353,591433 − 78,012539 − 0 − 876,440599 − 40,954555 − 20,303871 =
**337,879869 €** — `check_net_cf()`, this library's first ruling, asserted in every month from
`result_cf()`'s own published columns rather than from the cells behind them.

### The variant: the *Einmalbeitrag*

Model point 2 is the anchor cell with `prem_term` changed from 25 to 1 and nothing else, so it
isolates the second premium form. The single premium is **43 273,05 €**; the *Beitragssumme* is
that same amount, so the 25 ‰ *Zillmersatz* buys only 1 081,83 € of zillmered cost against
1 252,53 € on the level-premium form, and `ann_due_prem_1st` collapses to exactly 1.

| policy year | pols_if | premiums | claims_death | claims_maturity | claims_lapse | expenses | commissions | net_cf |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000000 | 43,273.05 | 43.19 | 0.00 | 147.82 | 350.04 | 1,081.83 | 41,650.17 |
| 2 | 0.949145 | 0.00 | 45.68 | 0.00 | 1,728.58 | 48.26 | 0.00 | -1,822.52 |
| 3 | 0.900810 | 0.00 | 48.10 | 0.00 | 1,181.37 | 45.20 | 0.00 | -1,274.68 |
| 24 | 0.458543 | 0.00 | 236.84 | 0.00 | 813.28 | 32.39 | 0.00 | -1,082.51 |
| 25 | 0.444064 | 0.00 | 260.17 | 35,570.54 | 0.00 | 83.85 | 0.00 | -35,914.55 |
| **Total** | **16.648981** | **43,273.05** | **2,894.48** | **35,570.54** | **22,825.77** | **1,314.12** | **1,081.83** | **-20,413.68** |

Four consequences are visible in five rows. **The § 169 floor is slack from the first
anniversary** — `res_zill_pp(1)` = 39 648,80 € against `res_min_pp(1)` = 38 783,34 €, the reverse
of the level-premium ordering, a single premium leaving almost nothing to amortise. **The
surrender outflow is far larger throughout**, 22 825,77 € in total against 9 112,99 €, every
surrendering policy carrying a reserve built in the first year. **The monthly grid bites hardest
exactly here**: policy year 1's surrender claim falls from 1 816,26 € on the annual grid to
147,82 €, because the eleven months before the first anniversary are paid the § 169 value struck
at issue, which is zero — an *Einmalbeitrag* contract surrendered in its first months gets its
*Überschussguthaben* and nothing else, which is what the statute says and what the annual grid
could not express. And **the maturity benefit is much higher**, 80 699,89 € against 65 227,99 €.
The two forms' `net_cf` totals are *not* comparable: the equivalence holds in present value on
tariff survivorship, not in undiscounted totals over a lapsing cohort.

### The variant: the three *Überschussverwendung* systems

Model points 8 and 9 differ from the anchor in `surplus_use` alone. The same surplus is
credited in all three; what differs is where it lands.

| model point | `surplus_use` | maturity benefit per policy | death benefit per policy, month 59 | premiums collected | `net_cf` total |
|---|---|---:|---:|---:|---:|
| 1 | `ansammlung` | 65,227.99 | 50,460.89 | 33,365.26 | -9,981.79 |
| 8 | `bonus` | 63,562.77 | 50,532.10 | 33,365.26 | -8,089.89 |
| 9 | `beitragsverrechnung` | 52,428.98 | 50,085.64 | 28,016.10 | -8,318.08 |

The death benefit is read at **month 59**, the anniversary closing policy year 5 — the instant the
annual grid priced, and unchanged by the conversion. A death earlier in that policy year is paid
the balances standing at the previous anniversary and is strictly smaller on all three systems;
the asymmetry between them survives that, which is what makes it a property of the product rather
than of the grid.

That is exactly the asymmetry the sources describe, and it is arithmetic rather than
coincidence: the *verzinsliche Ansammlung* accumulates at `ans_rate` = 2,70 % and the
*Bonussystem* at `rechnungszins` = 1,00 %, so the first wins at the *Ablauf* by 1 665,22 €;
but the *Bonussystem* buys **paid-up insurance**, whose whole face amount is payable on death
at once, so the second wins on an early death by 71,21 €. A model that set the two rates equal
would lose the distinction, correctly. *Beitragsverrechnung* moves the surplus out of the
benefit stream entirely: premiums collected fall by 5 349,16 € and the maturity benefit falls to
the guaranteed sum plus the accrued terminal share alone.

### What the conversion to a monthly step changed in these notes

The model was moved from an annual grid to a monthly one after these notes were written, and the
sentences that stopped being true were restated rather than left standing.

1. **The frame.** `t` counts policy months, `proj_len() = 12 · policy_term`, and the worked example
   is now **two tables** — the whole run summed into policy years by `result_cf_annual()`, which is
   the view every figure quoted here is stated on, and the twelve months of policy year 1 beside it.
2. **Two clocks.** Annual cells take a policy year `k` and monthly cells a month `t`; the decrement
   rates take `t` and return the **year's annual** rate, with `mort_rate_mth` and `lapse_rate_mth`
   the monthly rates actually applied, each `1 − (1 − r)^(1/12)` **[std]**.
3. **Nothing annual moved.** The equivalence, all three reserves, the § 169 value, the paid-up
   purchase and every part of the *Überschussbeteiligung* are **bit-identical** to the annual-step
   model's at every duration, because the monthly rates compound back to the annual ones and leave
   `pols_if` at every anniversary where it was. `result_surplus()` is unchanged, row for row.
4. **What a mid-year exit is paid.** A claim in a non-anniversary month is now paid the balances
   standing at the **last** anniversary, which on a *gezillmert* contract makes the guaranteed leg of
   a surrender exactly zero through the whole first policy year. The annual grid had to pay a
   month-0 surrender the value the coming anniversary would close at.
5. **The *Zahlweise* became real.** A *Beitrag* is collected in instalments on its own cycle, so the
   four fractionated model points collect less than the annual grid charged them — and the
   `echt` / `unecht` distinction, which lived entirely in a multiplier, is now a difference in the
   frame as well.
6. **The totals the timing moved** on the anchor: death claims 2 506,85 → 2 446,09 €, surrender
   claims 10 104,99 → 9 112,99 €, expenses 1 327,88 → 1 314,12 €, `net_cf` −11 048,31 →
   −9 981,79 €, and policy year 1 +320,89 → +355,51 €. `premiums` and the *Ablauf* payment are
   unchanged.
7. **The closure identity's split.** Deaths and surrenders now interleave month by month, so the
   anchor reads 0,04355790 and 0,51566656 against 0,04409376 and 0,51513070; the maturing cohort
   0,44077554 and the total 1,00000000 are unchanged.
8. **A tenth published identity.** `check_surr_nonneg()` asserts the *Rückkaufswert* non-negative in
   every month, the monthly grid quoting one in eleven months of each year the annual grid never
   priced.
9. **The § 165 failure is a month-specific event.** `lapse_rate` is 1.0 for the election year and
   `lapse_rate_mth` places the whole of it in that year's **last month**, where the election falls.
   Spreading an annual 1.0 geometrically would have emptied the cohort eleven months early.

### What was corrected in these notes

The worked example is the model's own output, and building the model found five places where these
notes and the implementation disagreed. In each the model was right and the notes above have been
corrected, rather than the table being fitted to the prose.

1. **`q₁` named two different quantities and the notation table conflated them.** The tariff must be
   unisex, so what *prices and reserves* is a fixed portfolio blend of the two table rows —
   `mort_rate_at_age(x)`, ½ / ½ **[std]** — while the *decrement* is the policy's own sex-specific
   rate `mort_rate_base(t)`, scaled by `mort_be_factor`. Pricing off the policy's own row made
   `prem_gross_pp` differ between model points 1 and 7, which is pitfall 17 exactly.
2. **`check_res_roll_fwd()`'s identity carries the *Risikozuschlag*.** Because `rating_factor` loads
   the death leg and not the survivorship, the Fackler recursion reads `f · q₁(x(t)) · SD` on the
   right and `(1 − q₁(x(t)))` on the left. As first written it was correct only at
   `rating_factor = 1.00`, which model point 14 is not.
3. **The *gezillmerte Deckungskapital* does not stay negative for several years at the 25 ‰ ceiling**
   — it is positive from the first anniversary. Pitfall 3's assertion is therefore vacuous on every
   shipped model point, and both places now say so rather than implying a behaviour the base run
   does not show.
4. **`result_cf()` publishes a ninth column, `liability_cf`.** The eight specified columns are
   unchanged and in the stated order and the six flow columns still sum to `net_cf`; the ninth is
   appended because the conventions suite reads it *from the frame* to assert
   `net_cf(t) == −liability_cf(t)`.
5. **`res_zill_pp`, `res_min_pp` and `res_net_pp` are the premium-paying constructions throughout**,
   on the full `sum_assured`; only `res_pp` switches to the paid-up basis. Writing all four as
   switching makes `bfz_si_pp` depend on itself, the § 169 value that buys the paid-up sum being
   struck on the contract as it still is. For the same reason `check_surr_floor()` compares
   `res_guar_pp` with the other two only while the contract is premium-paying.


---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared grid.
The valuation layers consume them and are **cited, never reproduced**.

- **The German statutory *Deckungsrückstellung*.** § 341f HGB requires it to be formed at the
  *versicherungsmathematisch berechneter Wert*, **including profit shares already allocated** but
  **excluding *verzinslich angesammelte Überschussanteile***, and after deducting the present value of
  future premiums, by the **prospective method** [REG-R54]. `res_pp(t) × pols_if(t)` is this model's
  contribution to that line and `av_sur_pp(t) × pols_if(t)` is explicitly **not** part of it. Three things
  the model does not do: it does not floor the reserve at zero as the balance sheet does, so the
  negative early *gezillmert* values stay visible; it does not apply the § 4 DeckRV ceiling as a
  reserving constraint separate from the tariff, the shipped `alpha_rate` already sitting at it; and it
  carries no *Verwaltungskostenrückstellung* for the period after the *Beitragszahlungsdauer*, where the
  `gamma_rate` cost runs on with no `beta_rate` income — the pricing equation funds it, and the
  classical reserve convention here assumes the ongoing loadings meet the ongoing costs.
- **The *Zinszusatzreserve*.** An HGB reserve arising when the § 5 Abs. 3 DeckRV *Referenzzins* falls
  below a contract's tariff rate, financed out of the result and, under § 140 VAG's second escape hatch,
  out of the free RfB [REG-R10] [REG-R17]. It exists in no other jurisdiction in this repository and
  **this model does not compute it**, but it matters here: the ZZR is how a high-guarantee cohort
  consumes the surplus that would otherwise be declared, which is why a delib path is a scenario.
- **The RfB, the *Schlussüberschussanteilfonds* and the MindZV.** The surplus this model credits is the
  **output** of the insurer's declaration policy, not the MindZV minimum, which is a transfer to the RfB
  — 90 % of the *Kapitalanlageergebnis* after the *Rechnungszinsen*, 90 % of the *Risikoergebnis*, 50 %
  of the *übriges Ergebnis*, *Direktgutschrift* deducted, *Alt-* and *Neubestand* separate [R6]
  [REG-R18] — with the RfB [REG-R10], its collective part [REG-R19] and the
  *Schlussüberschussanteilfonds* of § 28 RechVersV [REG-R54] between it and the policy. **None of that
  is modelled.**
- **Solvabilität II.** Technical provisions are a best estimate — the probability-weighted average of
  future cash flows discounted at the relevant risk-free term structure — plus a risk margin [REG-R1]
  [REG-R2] [REG-R6], with EIOPA publishing the curves monthly and § 83 VAG making their use binding
  [REG-R4]. `BEL = Σ_t v(t) · liability_cf(t)` over the recursion above. The **future discretionary
  benefits** — the declared *Zinsüberschuss*, the *Schlussüberschussanteil* and the *Ansammlung* — are
  the substance of the best estimate here, and the crediting rule above is exactly the management
  action a market-consistent valuation must model. **No cost-of-capital rate, contract boundary rule or
  standard-formula shock in this library was read from a retrieved instrument**, so every such figure is
  **[std]** [REG-R2]. Under **IFRS 17** this is the archetypal direct-participating contract, measured
  under the variable fee approach on this same fulfilment-cash-flow engine; grouping, CSM and risk
  adjustment are out of scope [REG-R55].
- **The guarantee is an option.** A guaranteed sum insured plus a guaranteed *Rechnungszins* is a
  written put on the *Sicherungsvermögen*, and the deterministic path above prices none of it; a
  stochastic-on-deterministic run is what a time-value-of-options-and-guarantees calculation
  consumes. The outer boundary is the *Sicherungsfonds*: a fund-level 5 % haircut under § 222 VAG
  and an uncapped reduction under § 314 VAG, which also lets the supervisor **temporarily prohibit
  the *Rückkauf*** [REG-R12]. **A mass-surrender run here produces the values the contract owes, not
  the ones that would be paid if § 314 were in force.**

---

## Key sensitivities and model risks

In rough order of leverage on this product.

1. **The declared-rate path.** `decl_rate` sets `zins_ueberschuss_rate` one-for-one above the
   guarantee, and the credit compounds at `ans_rate` for up to twenty-five years, so it dominates
   the maturity benefit and every surrender value after the early durations. The base run is **one
   carrier's 2025 rate held level forever**, and that rate is trade-press reporting of a declaration
   covering "die klassischen Lebens- **und** Rentenversicherungen" jointly [R26]; the `low` and `nil`
   scenarios exist so the range is exercisable. **No endowment-specific declared rate exists in the
   corpus at all** — the market averages are stated by Assekurata to be for the *klassische private
   Rentenversicherung* [R25], and the base rate is for a mixed book, so that an endowment shares the
   annuity's declaration remains [unverified] (gap 2).
2. **The *Zillmerung* and the § 169 floor together.** `alpha_rate` at the 25 ‰ ceiling drives the
   negative early reserve, the whole early-duration surrender-value profile, the year-one strain and
   the duration at which the contract first earns any interest surplus at all. The ceiling is cited
   [R7] [REG-R16]; **the level is [std] and no German carrier's actual acquisition cost is public**
   (gap 7). Halving it moves the first five surrender values by more than any other single parameter.
3. **The mortality basis, in two directions at once.** The proxy's level and slope are both
   unsourced, and the same table serves a death leg and a survival leg whose directions of prudence
   are opposite [REG-R47] [REG-R48]. The survival leg dominates a twenty-five-year endowment's
   reserve, so a level error matters less than on a term cover — but `mort_be_factor` moves the
   *Risikoüberschuss* the model does **not** compute, so the sensitivity is understated by
   construction, and the proxy carries **no selection**, which overstates early deaths on newly
   written business.
4. **The lapse shape.** Cumulative surrender over twenty-five years removes a large part of the
   cohort before the *Ablauf*, and on an endowment the late years are the profitable ones, so the
   assumption governs how much of the loaded tail is collected. The duration-12 spike is the one
   feature the evidence supports [R10] [REG-R45]; **the levels are unsourced**, the market
   aggregates are not surrender rates [R20], and a user with experience data should replace the table.
5. **The terminal bonus, and the *Überschussverwendung* choice.** `term_rate = 0.40%` has **no
   source at all** (gap 1), accrues on the reserve for the whole term, and its payability on
   surrender — zero here — is a second unsourced choice that would move surrender values most. And
   switching `ansammlung` → `bonus` moves benefit **between** death and maturity without changing
   the surplus credited, while `→ beitragsverrechnung` moves it out of the benefit stream into the
   premium stream; the corpus does not establish which system the market uses [R28] (gap 4), so this
   is a structural rather than a parametric sensitivity.
6. **Two unmodelled paths: the *Beitragsfreistellung* take-up, and the balance-sheet levers.** The
   paid-up election is deterministic because no take-up rate exists in the corpus, yet a real German
   book converts a material share [R20] [REG-R28], and a projection showing none overstates future
   premium income and future benefits together. Alongside it, the *Bewertungsreserven* share is set
   to zero on the reasoning that the *Sicherungsbedarf* has routinely exhausted it [R8] [REG-R9],
   and the ZZR — how a high-guarantee cohort depresses the declared rate for everyone [REG-R17] — is
   not computed. All three would move the answer and none is a gross liability cash flow.
7. **Data provenance.** Every charge level, every behavioural rate, the terminal bonus, the
   *Ansammlungszinssatz*, the *Stornoabzug* schedule, the entry age, the sum insured and the
   mortality proxy are **[std]**; the corpus's only quantified carrier terms are Debeka's
   *Stornoabzug*, sub judice [S3] [R22] [R30], and Allianz's declared rate [S11]. **A calibration
   pass against a *Produktinformationsblatt*, a PRIIP-*Basisinformationsblatt* and a named insurer's
   § 28 RechVersV *Anhang* disclosure [REG-R54] is required before any quantitative use.**

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-kapitallebensversicherung-r1
[R10]: #delib-kapitallebensversicherung-r10
[R12]: #delib-kapitallebensversicherung-r12
[R14]: #delib-kapitallebensversicherung-r14
[R15]: #delib-kapitallebensversicherung-r15
[R18]: #delib-kapitallebensversicherung-r18
[R19]: #delib-kapitallebensversicherung-r19
[R2]: #delib-kapitallebensversicherung-r2
[R20]: #delib-kapitallebensversicherung-r20
[R22]: #delib-kapitallebensversicherung-r22
[R24]: #delib-kapitallebensversicherung-r24
[R25]: #delib-kapitallebensversicherung-r25
[R26]: #delib-kapitallebensversicherung-r26
[R28]: #delib-kapitallebensversicherung-r28
[R29]: #delib-kapitallebensversicherung-r29
[R3]: #delib-kapitallebensversicherung-r3
[R30]: #delib-kapitallebensversicherung-r30
[R4]: #delib-kapitallebensversicherung-r4
[R5]: #delib-kapitallebensversicherung-r5
[R6]: #delib-kapitallebensversicherung-r6
[R7]: #delib-kapitallebensversicherung-r7
[R8]: #delib-kapitallebensversicherung-r8
[R9]: #delib-kapitallebensversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R10]: #delib-reg-r10
[REG-R12]: #delib-reg-r12
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R24]: #delib-reg-r24
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R34]: #delib-reg-r34
[REG-R4]: #delib-reg-r4
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R52]: #delib-reg-r52
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R6]: #delib-reg-r6
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
