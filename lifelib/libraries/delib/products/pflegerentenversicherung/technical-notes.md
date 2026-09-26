# Technical Notes

**Status:** Draft, 2026-08-29 (research access date 2026-08-29).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Pflege_DE_S`**, **monthly** grid — for the standardized composite German
*Pflegerentenversicherung* defined in `product-spec.md` (same directory). This is not any single
insurer's product, and it was **drafted with no product document of any kind retrieved for it**:
direct HTTP egress from the build environment was blocked and the session's `WebSearch` budget was
exhausted before work on this product began. The citations have since been re-verified against the
primary documents, so that **27 of the 36 source entries in `sources.md` read `Retrieved: yes`, five
read `no` and four are partial** — a tag below is a record of a document read where its entry says
`yes`, and a pointer to be checked where it does not. [S#] / [R#] tags refer to the source list in
`sources.md` (numbering carried from `_research/pflegerentenversicherung.md`; frozen); [REG-R#] tags
refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering).
**[std]** marks standardizations introduced for the reference implementation; [unverified] marks
claims no source could corroborate. On this product **every biometric rate, every charge, every
lapse rate and the premium itself is [std]** — a fact stated here once and repeated at each
assumption table rather than left to be inferred. Parameter values are identical to those in
`product-spec.md`. Cells names, model-point columns and CSV headers are English `lower_snake_case`;
German terms of art keep their German form in prose.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — *Beiträge*,
  *Pflegerente* payments, surrender payments, any *Todesfallleistung*, and expenses — for a
  single-policy model point, on an expected (probability-weighted) basis. The model publishes what
  a valuation layer consumes; it does **not** discount the projected stream, does not compute a
  *Deckungsrückstellung*, does not compute a *Zinszusatzreserve* and does not compute capital. Those
  layers are referenced under *Valuation and reserve pointers*, never reproduced.
- **The one place a discount rate appears.** The *Beitrag* is a **priced** quantity, struck by
  equivalence at the *Rechnungszins* on the first-order (*erster Ordnung*) bases [REG-R8] [REG-R47],
  so the model carries a second, self-contained actuarial-value engine — the `tar_*` cells — whose
  only output is `premium_mth_pp()`. **That engine discounts; the projection does not.**
- **Projection frequency.** **Monthly grid.** The *Pflegerente* is a monthly annuity, the *Beitrag* a
  monthly instalment, and the *Pflegegrad* can change in any month, so the monthly grid is the
  contract's own rather than a refinement of an annual one. The `_S` suffix follows lifelib.
- **What `t` counts, and the frame.** `t` is the **policy month index, 0-based**: `t = 0` is the
  month of issue, and `t` counts complete months elapsed since issue. `age(t) = age_at_entry + t //
  12`, so the attained age steps at the policy anniversary. The frame **starts** at
  `t = duration_mth_init()`, which is `0` for new business and the elapsed duration for an in-force
  model point, and **ends** at `proj_len() - 1`, so the frame is
  `range(duration_mth_init(), proj_len())` and the policy year is the 1-based label
  `y(t) = t // 12 + 1`. Where the frame starts is a product fact and is not asserted by the
  conventions suite; contiguity is.
- **`proj_len()` is the number of projected periods**, the **exclusive end** of the frame counted
  from `t = 0` — the library-wide reading, and lifelib's own `range(proj_len())`. Here

      proj_len() = 12 * (omega_age() - age_at_entry())

  which depends only on the entry age and the terminal age, **not** on `duration_mth_init()`. The
  anchor cell (entry age 45, `omega_age = 110`) therefore has `proj_len() = 780` and runs to
  `t = 779`, 780 monthly rows, attained ages 45 to 109. A point opening at `duration_mth_init() = d0`
  publishes `proj_len() - d0` rows and still ends at its own `proj_len() - 1`:
  `duration_mth_init` shortens the frame at the front, never at the back.
- **Terminal age.** `omega_age = 110` **[std]**, with `mort_rate(t) = 1.0` forced in the final year
  of age so the model is a closed system rather than a truncated one and the decrement closure holds
  exactly. It is a modelling choice, not a table fact — the DAV tables run higher [R15] [REG-R51] —
  and it costs nothing material: an active life aged 45 survives to 110 with probability of the
  order of 1e-4 on the shipped basis.
- **Timing conventions [std].** Within month `t`: the *Beitrag* is collected **at the start** of the
  month, in advance, from the lives then in the premium-paying states; the *Pflegerente* is paid
  **at the start** of the month, in advance, to the lives then in a paying *Pflegegrad*; per-policy
  and premium-related expenses are charged at the start of the month; transitions act **over** the
  month; and death and surrender benefits fall **at the end** of the month. `pols_if(t)` is the
  count at the **start** of month `t` and is the weight on that same `result_cf()` row's cash flows,
  as the house style requires; end-of-period state is reached through `pols_if_at(t, "END")`.
- **Why the annuity is in advance.** German *Renten* are conventionally *monatlich vorschüssig*, and
  paying in advance puts the annuity on the same weight as the premium it replaces, which is what
  lets `check_waiver()` reconcile the two streams against one ledger.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  annuity, surrender, death benefit and expenses −), with the outgo-positive orientation published
  as `liability_cf(t) = -net_cf(t)`. Intermediate values at full precision; displayed cash flows to
  euro cents and `pols_if` to six decimals **[std]**.
- **Out of scope, deliberately, each in one line.** No *Überschussbeteiligung* — the surplus chassis
  belongs to `products/kapitallebensversicherung/`. No *Beitragsdynamik*: the acceptance rate on each
  offer is a behavioural assumption this corpus cannot support. No *Beitragsfreistellung* and no § 38
  VVG premium-default conversion: every voluntary exit is a surrender, and the direction of the bias
  is stated in the product specification. No taxation of premium or benefit, the benefit's treatment
  being an open question [R23] [REG-R41]. No select mortality after onset of care — the shipped
  in-care mortality is an aggregate, and the consequence is pitfall 9 and model risk 9. No
  *Pflege-Bahr* *Zulage*, statutorily unavailable [R8]. And no three-month *Nachprüfung* notice tail:
  whether § 174 VVG reaches a *Pflegerente* through § 177 was not established [REG-R29] [unverified];
  § 176 VVG extends §§ 150–170 *entsprechend* to the *Berufsunfähigkeitsversicherung* only, which is
  a point against the extension but not a decision on it.
## Model point attributes

`model_point_table.csv` is indexed by `point_id` and is the **only** input file without a
`provenance` column, a model point being a configuration rather than an assumption (delib ruling 2).
"Exercised by" names the points that make the attribute do work.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Index; `Projection` is parameterized by it | all |
| `policy_id` | str | Human-readable identifier, `PFL-0000NN` | all |
| `sex` | enum {M, F} | The **projection** basis. Pricing is unisex [REG-R34], so this must not reach `premium_mth_pp()` | 1 (F) vs 2 (M), identical otherwise |
| `age_at_entry` | int | Age last birthday at issue; drives `proj_len()` and every rate lookup | 14 (18, the youngest permitted), 13 (65, the oldest) |
| `duration_mth_init` | int | Complete months elapsed at the projection start; `0` for new business. The frame opens at this `t` | 11 (240), 12 (336) |
| `status` | enum {aktiv, pg1…pg5} | State at the projection start | 12 (`pg3`, in claim) |
| `rente_mth` | float | The *vereinbarte Pflegerente* at *Pflegegrad* 5, EUR per month — the scaling constant of the whole benefit | 13 (1 500), 14 (500) |
| `staffel_id` | str | Key into `benefit_scale_table.csv`: `delib_std` or `bahr` | 5 (`bahr`) |
| `prem_end_age` | int | Attained age at which the *Beitrag* ceases; `110` (= `omega_age`) means lifelong | 4 and 9 (65, *abgekürzte Beitragszahlungsdauer*) |
| `prem_mode` | enum {monthly, quarterly, half_yearly, annual, single} | Instalment frequency; `single` is the *Einmalbeitrag* | 1, 3, 4, 5, 6 |
| `premium_mth` | float | The contractual monthly *Beitrag*. **`0.0` means "derive by equivalence"** | 10 (75.00 supplied), 11 and 12 (in-force premiums) |
| `rating_factor` | float | *Risikozuschlag* multiplier on the gross premium; `1.00` at standard rates | 13 (1.50) |
| `wartezeit_months` | int | *Wartezeit* from inception, in months | 7 (36) |
| `karenz_months` | int | *Karenzzeit* from onset, in months | 7 (6) |
| `leistungsdynamik` | float | Annual escalation of the annuity in payment; `0.0` = off | 8 (0.02) |
| `beitragsrueckgewaehr` | bool | *Beitragsrückgewähr* death benefit on/off | 9 (True) |
| `stornoabzug_rate` | float | Deduction from the *Rückkaufswert*, as a fraction; `0.0` = off | 10 (0.05) |
| `pols_if_init` | float | Policy count at the frame's first `t`; `1.0` everywhere here | all |

**The three attributes most easily got wrong**, each a numbered pitfall: `sex` is a *projection*
input and must not touch the price [REG-R34]; `premium_mth = 0.0` is a sentinel, not a free contract;
and `duration_mth_init` shifts where the frame **starts** without changing `proj_len()`.

### The fourteen model points

| # | Configuration | What it exercises |
|---|---|---|
| 1 | **Anchor.** F, entry 45, aktiv, 1 000 €/mth, `delib_std`, lifelong, monthly, premium derived | The worked example |
| 2 | M, entry 45, otherwise identical to 1 | Unisex pricing against a sex-specific projection: same `premium_mth_pp()`, different claims |
| 3 | F, entry 55, quarterly, lifelong, `delib_std` | The upper half of the purchase cluster; quarterly instalments |
| 4 | M, entry 40, premiums to age 65, half-yearly | *Abgekürzte Beitragszahlungsdauer*; half-yearly instalments; the paid-up tail |
| 5 | F, entry 50, annual mode, `staffel_id = bahr` | The statutory 10/20/30/40/100 grid, where *Pflegegrad* 1 **is** insured and waived |
| 6 | F, entry 60, `prem_mode = single` | The *Einmalbeitrag*: one payment at `t = 0`, no premium-paying ledger thereafter |
| 7 | M, entry 50, `wartezeit_months = 36`, `karenz_months = 6`, monthly | Both waiting devices, and the *Karenz* ledger |
| 8 | F, entry 45, `leistungsdynamik = 0.02`, monthly | The escalation ledger; `esc_pg` diverges from `pols_pg` |
| 9 | M, entry 45, `beitragsrueckgewaehr = True`, premiums to age 65, monthly | The death-benefit stream, `claims_death` non-zero |
| 10 | F, entry 48, `premium_mth = 75.00`, `stornoabzug_rate = 0.05` | A supplied premium instead of a derived one; a non-zero *Stornoabzug* |
| 11 | M, entry 42, `duration_mth_init = 240`, aktiv, monthly | An in-force point opening at `t = 240` with 20 years run |
| 12 | F, entry 55, `duration_mth_init = 336`, `status = pg3` | An in-force point **in claim**: waived premium and a paying state at the frame's first row |
| 13 | **Boundary.** M, entry 65 (top of the observed band), 1 500 €/mth, `rating_factor = 1.50` | Shortest pre-claim period, highest premium, a *Risikozuschlag* |
| 14 | **Boundary.** F, entry 18 (bottom of the band), 500 €/mth, monthly | Longest projection (`proj_len() = 1104`, `t = 0 … 1103`), smallest benefit, expense-dominated |

Between them the fourteen exercise both premium forms, all four instalment frequencies, both
*Leistungsstaffeln*, every switchable option, two in-force points and both ends of the age band.

**Why model point 9 does not pay for life.** The *Beitragsrückgewähr* is the one option whose cost is
not a modest loading, and at a *Rechnungszins* of 1,00 % it is close to the whole premium: returning
nominal premiums on a death that is on average forty years away is worth about 0.67 of what was paid,
against a premium stream whose own present value is discounted *and* thinned by survival. Written
with a lifelong *Beitragszahlungsdauer* the equivalence's denominator, `U (1 − β) − D1 − a1`, falls to
3.6 of 313.5 units and the model point becomes a knife-edge: the premium is 2,659.56 € a month and a
small change in any basis would send it negative. Point 9 therefore pays to 65, which is how the
German market writes a *Beitragsrückgewähr* tariff, and its premium is 622.92 € a month — still **9,7
times** the anchor's, which is the honest measure of what a gross return of premiums costs on this
basis rather than the "roughly doubles" the research file reasons to at a higher technical rate.

---

## Input files

Every file is a plain UTF-8 CSV in the model folder's **parent**, read once per model by a reader
cells in the `Data` Space (the `annuallife/TradLife_A` layout). Every file **except**
`model_point_table.csv` carries a final `provenance` column, one tag per row — delib ruling 2.

| File | Index columns | Value columns | Content |
|---|---|---|---|
| `model_point_table.csv` | `point_id` | the eighteen attributes above | The fourteen model points. **Exempt** from `provenance` |
| `benefit_scale_table.csv` | `staffel_id`, `pflegegrad` | `benefit_pct`, `provenance` | The *Leistungsstaffel*: 0/30/50/75/100 % for `delib_std`, 10/20/30/40/100 % for `bahr` [R8] |
| `mort_table.csv` | `sex`, `age` | `mort_rate`, `provenance` | Annual **active-life** mortality, ages 18–109, both sexes |
| `incidence_table.csv` | `sex`, `age` | `inc_rate`, `provenance` | Annual rate of entering **any** *Pflegegrad* from the active state, ages 18–109, both sexes |
| `care_table.csv` | `pflegegrad` | `entry_share`, `det_rate`, `rec_rate`, `mort_mult`, `provenance` | The whole in-care basis in five rows: the distribution of the grade first entered, the annual deterioration rate to the next grade, the annual recovery rate to the previous grade or to active, and the force-of-mortality multiple over an active life of the same age |
| `lapse_table.csv` | `policy_year` | `lapse_rate`, `provenance` | Annual lapse from the **active** state, policy years 1–40; year 40's rate applies to every later year |
| `surrender_table.csv` | `policy_year` | `rkw_prem_ratio`, `provenance` | The guaranteed *Rückkaufswert* as a fraction of premiums paid to date, policy years 1–40, clamped as for lapse |
| `expense_table.csv` | `item` | `value`, `unit`, `provenance` | `acq_permille`, `admin_prem_pct`, `admin_mth_pp`, `claim_expense_pp`, `expense_infl` |
| `basis_table.csv` | `param` | `value`, `provenance` | `rechnungszins`, `omega_age`, `unisex_mix_male`, `rec_age_ref`, `rec_age_decay`, `inc_cap`, `beitragssumme_cap_age`, `roll_fwd_tol`, and the five first-order prudence margins `inc_margin`, `det_margin`, `rec_margin`, `care_mort_margin`, `act_mort_margin` |

Nine files, each read by a reader cells in `Data`; the suite asserts there are no orphans.

---

## State variables

The contract is a **multi-state** risk. The state space is the one § 15 SGB XI defines [R2]
[REG-R51], plus the two absorbing exits a life-assurance contract adds:

```
   aktiv ──►  PG1  ⇄  PG2  ⇄  PG3  ⇄  PG4  ⇄  PG5
     │  ▲      │        │        │        │        │
     │  └──────┘ Reaktivierung / Herabstufung      │
     │         │        │        │        │        │
     ▼         ▼        ▼        ▼        ▼        ▼
   storno                    tot  (absorbing)
```

Forward moves are deterioration, backward moves are *Herabstufung* and, out of PG1,
*Reaktivierung*; death is reachable from every state. **Lapse is reachable only from `aktiv`**
[std]: a claimant whose premium is waived has nothing to lapse from and everything to lose. Pitfall
12 tests it.

| Variable | Description | Updated |
|---|---|---|
| `proj_len` | Number of projected months, `12 * (omega_age - age_at_entry)`; the frame's exclusive end | once per point |
| `duration_mth(t)`, `policy_year(t)`, `age(t)` | Months since issue (equal to `t`), the *Versicherungsjahr* `t // 12 + 1`, and the attained age `age_at_entry + t // 12` | monthly |
| `pols_act(t)`, `pols_karenz(t, g, z)` | Lives active at the start of month `t`; lives in *Pflegegrad* `g` whose *Karenzzeit* clock stands at `z`, `1 ≤ z ≤ karenz_months`, the ledger being empty when `karenz_months = 0` | monthly recursion |
| `pols_pg(t, g)` | Lives in *Pflegegrad* `g` at the start of month `t` whose *Karenzzeit* has been served — the ledger the annuity is paid on | monthly recursion |
| `esc_pg(t, g)` | The **escalation-weighted** counterpart of `pols_pg(t, g)`: the sum over those lives of `(1 + leistungsdynamik)^(months since the annuity began / 12)`. Equal to `pols_pg` exactly when the dynamic is off | monthly recursion |
| `pols_care(t)`, `pols_if(t)` | Everyone in care, waiting or paid, `Σ_z Σ_g pols_karenz + Σ_g pols_pg`; and `pols_act + pols_care`, the in-force count at the **start** of month `t` | monthly |
| `pols_if_at(t, timing)` | `"BEG"` = `pols_if(t)`; `"END"` = `pols_if(t + 1)`. End-of-period state goes through here and never through `pols_if` | monthly |
| `pols_in_term(t)`, `pols_waived(t)`, `pols_prem(t)` | In-force units inside the premium term (`age(t) < prem_end_age`); of those, the units in a *Pflegegrad* whose `benefit_pct` is positive — the *Beitragsbefreiung* population; and the difference, the units that actually pay | monthly |
| `pols_entry(t, g)`, `pols_grad(t, g)` | Lives entering *Pflegegrad* `g` from the active state during month `t`, and lives graduating out of the *Karenz* ledger into `pols_pg(·, g)` | monthly |
| `pols_death(t)`, `pols_lapse(t)` | Deaths during month `t` from every state; lapses from the active state only, after the insured decrements | monthly |
| `pols_dead_cum(t)`, `pols_lapse_cum(t)` | Cumulative absorbing counts at the start of month `t`; `cum_prem_max_pp(t)` is premiums payable to date on an uninterrupted path, the base of both the *Rückkaufswert* and the *Beitragsrückgewähr* | monthly |
| `tar_pols_act(t)`, `tar_pols_pg(t, g)`, `tar_pols_prem(t)` | The same ledgers on the **first-order** basis, without lapse — the pricing engine's state | monthly |

There is **no account value** and **no paid-up state**, and the *Deckungskapital* — a real object of
this contract — is deliberately **not** a state variable: the library publishes undiscounted cash
flows and leaves the reserve to the layer that consumes them, with the guaranteed *Rückkaufswert*
entering as data (product spec, footnote 21).

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Benefit | A monthly *Pflegerente*, paid in advance, equal to `benefit_pct(g) × rente_mth` for the insured's current *Pflegegrad* `g` | [S4] |
| *Leistungsstaffel* `delib_std` | 0 / 30 / 50 / 75 / 100 % across grades 1 to 5 | **[std]**, product spec footnote 12 |
| *Leistungsstaffel* `bahr` | 10 / 20 / 30 / 40 / 100 % — the *Pflege-Bahr* grid **as the market writes it, not as the statute fixes it**. § 127 Abs. 2 Nr. 4 SGB XI requires only a *Geldleistung* at every *Pflegegrad*, at least 600 € at grade 5, capped at the SGB XI benefit level; the percentage schedule belongs to the PKV-Verband's *brancheneinheitliche Vertragsmuster* under Abs. 2 Satz 2, which this library has not retrieved | shape **[std]**; [R8] for what the statute fixes |
| Trigger | The statutory *Pflegegrad* of §§ 14, 15 SGB XI, determined by the *Medizinischer Dienst* or by an independent assessor under § 18 Abs. 1, not by the insurer. Wordings commonly **pin** the statutory text to an edition date or copy it into the conditions rather than tracking the live statute | [R2] [R6]; [S1] [S2] [S4]; [REG-R51] |
| Care setting | Irrelevant to the benefit; the same annuity is payable at home and in a *Pflegeheim* | **[std]**, product spec footnote 1 |
| *Beitragsbefreiung* | **Full**, from the first month in which any annuity is payable; revived on exit from the paying grades. The one retrieved wording waives on the same trigger but makes the waiver **permanent** after twelve months' continuous annuity at grade 4 or 5 | [S4]; detail **[std]** |
| Premium form | Level monthly *Beitrag*, guaranteed for the life of the contract, adjustable only on the § 163 VVG route | [R11]; [REG-R27] |
| Premium cessation | On death; on the start of an insured annuity; at `prem_end_age` | [S4] |
| Equivalence principle | The gross premium is struck so that, on the first-order bases at the *Rechnungszins*, the expected present value of premiums equals that of benefits plus expenses | [REG-R8] [REG-R47] |
| *Rechnungszins* | **1,00 %** p.a. — § 2 Abs. 1 DeckRV for new business from 1 January 2025; Abs. 2 keeps the rate used at conclusion for the contract's whole term | [R13]; [REG-R14] [REG-R15] |
| *Höchstzillmersatz* | **25 ‰ of the *Summe aller Prämien***, § 4 Abs. 1 DeckRV, cut from 40 ‰ by the LVRG from 1 January 2015; the retrieved wording applies exactly this, at *"2,5 % der … zu zahlenden Beiträge"* | [R13]; [S4]; [REG-R16] [REG-R20] |
| *Rückkaufswert* | The *Deckungskapital* on the premium bases, floored by the value that results from spreading acquisition and distribution costs evenly over the first **five** contract years | [REG-R28] |
| *Stornoabzug* | Admissible only if agreed, quantified and appropriate (§ 169 Abs. 5 VVG); a deduction for unamortised acquisition costs is expressly ineffective. **The one retrieved *Pflegerenten* wording agrees 25 %**, rising to 50 % after a partial withdrawal — see the model-risk note at the end of this file | [R11] [REG-R28]; [S4] |
| Unisex | Sex may not enter the premium for contracts concluded from 21 December 2012 | [REG-R34] |
| *Wartezeit* / *Karenzzeit* | Contractual, both **0** in the base run, and the one retrieved underwritten tariff also has *Wartezeit* **keine**; § 127 Abs. 2 Nr. 6 SGB XI caps a *Pflege-Bahr Wartezeit* at *"höchstens fünf Jahre"* | [R8]; [S5]; base **[std]** |

**What is *not* in this table.** There is still **no cited premium**, no cited charge, no cited
transition rate and no cited *Rückkaufswert* level for this product, so this class is unusually thin
beside `frlib/products/temporaire_deces`, which could tabulate a published rate card. Everything
numeric that is missing here appears in class (c) as **[std]**, and that displacement is the single
most important thing to know about this model. **What changed in the provenance pass of 2026-08-30**
is that three of those gaps now have published comparators rather than nothing at all — the DAV's
first-order bases and prudence loadings for *Pflegegrade*, the GDV's in-force average premium, and
one carrier's *Stornoabzug* — and every one of them is recorded in `sources.md` and **not**
implemented. See "What the retrieved documents say about the shipped model" there.

### (b) Insurer-discretionary current elements

Thinner than on any savings product in delib, and for a structural reason: **a *Pflegerente* is a
life contract, so the insurer's discretion over price is confined to § 163 VVG and to the surplus
rebate** [REG-R27]. There is no bonus rate, no crediting rate and no charge scale to declare.

| Input | Snapshot value | Basis |
|---|---|---|
| *Überschussbeteiligung* in any application form | **None** — no *Beitragsverrechnung*, no *verzinsliche Ansammlung*, no *Bonus* uplift of the *vereinbarte Rente* | mechanic [R11] [R12] [REG-R24]; omission **[std]** (1) |
| The *Bruttobeitrag* / *Zahlbeitrag* spread | **Zero.** The model projects the *Bruttobeitrag* | [REG-R27] [REG-R53]; **[std]** (1) |
| § 163 VVG re-rating / tariff drift | **Never invoked**; the premium is struck once, at issue, on the bases shipped | [REG-R27]; **[std]** (2) |
| *Nachprüfung* intensity | **Not modelled** as a separate decrement: recovery and downgrade are biometric transitions, not claims-management outcomes | [R6] [S4]; **[std]** (3) |

1. delib publishes gross undiscounted cash flows and demonstrates the *Überschussbeteiligung*
   chassis in `products/kapitallebensversicherung/`; a discretionary *Beitragsverrechnung* would need
   a declared-rate assumption this corpus cannot supply (gap 18), and would make the projected premium
   a discretionary quantity — precisely what the product's proposition says it is not. The
   *Zahlbeitrag* is nevertheless what a customer pays, so a reader comparing this model's premium with
   a market quotation is comparing a *Bruttobeitrag* with a *Zahlbeitrag* and should expect the model
   to sit **above** the quotation.
2. § 163 is a management action conditional on emerging experience, not a projected assumption; a
   model that built one in would be asserting that the guarantee it demonstrates does not hold.
3. On a *Berufsunfähigkeitsrente* the insurer runs its own *Nachprüfung* and claims-management
   intensity is a real assumption [REG-R29]. Here the evidence is the statutory determination [R6],
   so re-verification is a documentation exercise and every exit from a paying grade is biometric.
   That is the sharpest modelling difference between `Pflege_DE_S` and `BU_DE_S`.
### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German source publishes an expense loading, a commission
scale, a lapse rate or a surrender-value table for **this product** (research gaps 2, 3, 19, 20).
The proxies below reproduce the *mechanics* the research file establishes; they are **not**
calibrations, and none is a proxy for DAV 2008 P.

**Two statements this section used to make about DAV 2008 P are wrong and are corrected here.** The
table is **not** unpublished: the DAV issues the derivation as a free *Ergebnisbericht* with the
bases in Anhänge 1 to 3, and a companion report that re-derives them **for the *Pflegegrade***
[R15]. And a *Pflegegrad*-shaped basis therefore does exist — the profession built one rather than
mapping the scales, which is what the BGH has since held cannot be done [REG-R36] [REG-R51]. **delib
still redistributes none of it and reproduces no value from it**; that is this library's own choice.
Three things about the published bases matter to anyone replacing the tables below: they are a
***Stufenmodell*** (*"mindestens Pflegegrad g ist erreicht"*), **not** a five-state per-grade chain;
they are transitions from *Pflegestufen* experience rather than *Pflegegrad* observations, the DAV
saying so in terms; and they come with published prudence loadings, which the margins at the end of
this section do not match. **A replacement must preserve four
properties**: (a) incidence by attained age, sex and *grade of entry*, because a stroke or a fracture
enters directly at grade 3 or 4; (b) deterioration dominating recovery above age 75; (c) mortality in
care as a grade-increasing multiple of active mortality; and (d) transition probabilities out of each
state summing, with the stay probability, to one.

**Active-life mortality [std]** — a Gompertz proxy, sex-specific, German-population-shaped, and
**not** DAV 2008 T or the DAV 2008 P active-life table [R16] [REG-R48] [REG-R52]:

    mort_rate(sex, x) = 1 - exp(-B_sex * c_sex ** x)      ages 18 to omega_age - 2
    mort_rate(sex, omega_age - 1) = 1.0                   the limiting-age convention

`B_M = 1.47884e-05`, `c_M = 1.110680`, `B_F = 4.76290e-06`, `c_F = 1.119962`, fixed by two anchors
per sex — `q(65) = 1.35 %` and `q(85) = 10.5 %` male, `0.75 %` and `7.0 %` female **[std]**. Those
anchors are what a substitute table must reproduce for the worked example to close, and the `Data`
docstring states them.

**Incidence into care [std]** — the rate at which an active life enters **any** *Pflegegrad*:

    inc_rate(sex, x) = min(I0_sex * exp(g_sex * (x - 65)), inc_cap)

`I0_F = 0.0110`, `g_F = 0.1400`, `I0_M = 0.0085`, `g_M = 0.1380`, `inc_cap = 0.50`. The slope is
anchored to **prevalence roughly doubling every five years of age above 75**, a growth rate of
`ln 2 / 5 = 0.1386`, and the level so that the model's own probability of reaching an insured grade
before death, from the anchor cell's entry age, is of the order of the **45 %** the research file
argues, with a mean age at first insured grade in the low eighties [unverified]. **The anchor is now
measurable and it is softer than 0.1386.** The observed *Pflegequoten* for 2023 rise by factors of
1,80 · 1,88 · 1,74 · 1,49 · 1,18 across the five-year bands from 70–75 to 95+ [R18] — about
`ln 1.8 / 5 = 0.117` over the range where this model earns its claims, and flattening sharply above
90 where the `inc_cap` of 0.50 does not yet bind. **The shipped slope is left where it is** and the
divergence is reported: changing it moves the worked example and the golden tests. The female parameters are the higher pair, which is
the sex differential the whole unisex tension turns on. The cap is a shape device: without it the
exponential exceeds one before age 100.

**The in-care basis [std]**, five rows of `care_table.csv`, and the most consequential table here:

| *Pflegegrad* | `entry_share` | `det_rate` (to `g+1`, annual) | `rec_rate` (to `g-1`/aktiv, annual) | `mort_mult` |
|---|---|---|---|---|
| 1 | 0.20 | 0.28 | 0.10 | 1.5 |
| 2 | 0.38 | 0.24 | 0.06 | 2.5 |
| 3 | 0.24 | 0.20 | 0.04 | 3.5 |
| 4 | 0.13 | 0.16 | 0.02 | 6.0 |
| 5 | 0.05 | 0.00 | 0.01 | 9.0 |

`entry_share` sums to 1.00 and is deliberately **not** the stock distribution, which the Destatis
table for end-2023 puts at **13,8 / 40,4 / 29,6 / 11,8 / 4,3 %** [R18] — not the 9 / 44 / 27 / 14 /
6 % this file previously quoted. Entrants skew lower than the stock because deterioration moves
people up over a spell, and using the stock as the entry mix is pitfall 17; the corrected stock,
with 54,2 % rather than 53 % in the two lowest grades, does not disturb that argument. **What no
source supplies is the entry mix itself, or the time spent at each grade** — Assekurata states in
terms that no information exists on how long people remain in each *Pflegegrad*, the grades dating
only from 2017 [S14] — so `entry_share` stays **[std]**. `mort_mult` is a
multiple on the **force** of active mortality at the same age, carrying the research file's most
load-bearing biometric statement — the mortality of a *Pflegebedürftiger* is **of the order of two to
three times an active life's at grade 2 and five to ten times at grade 5** [unverified]. Recovery is
further damped with age, `rec_rate(g, x) = rec_rate_g * exp(-rec_age_decay * max(0, x - rec_age_ref))`
with `rec_age_ref = 75` and `rec_age_decay = 0.10` **[std]**, which is what makes deterioration
dominate recovery above 75 — property (b) of a replacement table.

Three consequences follow, all three pitfalls. **The annuity in payment is short**, of the order of
three to five years, not the fifteen to twenty of a healthy-life pension at the same age — and this
is now checkable: the *BARMER-Pflegereport 2024*, via [S14], puts mean duration of
*Pflegebedürftigkeit* at about **five years** where care begins after 60, **4,0 for men and 5,7 for
women**, against about **25 months** mean stay in a *Pflegeheim*. The model's implied spell sits at
the low end of that for women — so pricing
it on DAV 2004 R would be prudent in exactly the wrong direction [R16] [REG-R49]. **Grade and
mortality are correlated**, so the highest-paying state is the shortest-lived. And **a deferred
period bites harder than its length suggests**, because a material share of new claimants die inside
it.

**Lapse [std]**, from the **active** state only, and zero once the premium term has ended:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6–10 | 11–20 | 21–40 |
|---|---|---|---|---|---|---|---|---|
| `lapse_rate` | 6.0 % | 5.0 % | 4.0 % | 3.5 % | 3.0 % | 2.5 % | 2.0 % | 1.5 % |

Year 40's rate applies to every later year. **No lapse rate for this product at any duration was
established** (gap 20); the shape is a modeller's construction, argued from *Zillmerung* — the
*Rückkaufswert* is near zero for the first years, so an early lapse is expensive to the policyholder
and the profile is flatter than a savings product's, and a paid-up contract has no premium-driven
exit at all. The monthly rate is `1 - (1 - lapse_rate(t)) ** (1/12)`.

**The guaranteed *Rückkaufswert* [std]**, as a fraction of premiums paid to date by
*Versicherungsjahr* `y(t) = t // 12 + 1` — the scale-free form, and the form a German contract
states [REG-R28]:

| Policy year | 1 | 2 | 3 | 4 | 5 | 10 | 15 | 20 | 25 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rkw_prem_ratio` | 0.00 | 0.00 | 0.05 | 0.12 | 0.20 | 0.42 | 0.50 | 0.56 | 0.60 | 0.64 | 0.70 |

with intermediate years interpolated in the shipped file and year 40's ratio applying thereafter.
Year `k`'s ratio applies **throughout** policy year `k`, `t = 12(k − 1) … 12k − 1`: it is the
current *Versicherungsjahr*, not the completed one, so a surrender at `t = 24` — two completed
years — already takes year 3's 0.05.
The shape encodes two cited facts: the 25 ‰ *Zillmerung* allowance [REG-R16], which is why the first
two years are zero, and the § 169 Abs. 3 five-year spread **floor** [REG-R28], which is why it turns
positive in year three. It never approaches 1.00, the contract having consumed risk premium
throughout.

**Expenses [std]**, all five levels placeholders, the structure cited:

| Item | Value | Unit | Rationale |
|---|---|---|---|
| `acq_permille` | 25.0 | ‰ of *Beitragssumme*, at `t = 0` | Set **exactly at** the § 4 DeckRV *Höchstzillmersatz* [REG-R16], so the ceiling binds visibly |
| `admin_prem_pct` | 0.030 | fraction of each premium collected | Placeholder; absorbs the *Ratenzahlungszuschlag* the model does not charge separately |
| `admin_mth_pp` | 2.00 | EUR per policy in force per month, `t = 0` prices | Placeholder, a plausible fraction of a mass-market monthly premium |
| `claim_expense_pp` | 1.50 | EUR per annuity payment made | Set **low** — the trigger is determined by a third party [R6], so claims cost is well below a *Berufsunfähigkeitsrente*'s [REG-R29] |
| `expense_infl` | 0.015 | annual | Placeholder; over a 65-year projection it is a factor of about 2.6 on the per-policy line |

The *Beitragssumme* the acquisition charge is struck on is
`premium_mth_pp() * 12 * (min(prem_end_age, beitragssumme_cap_age) - age_at_entry)` with
`beitragssumme_cap_age = 85` **[std]**, and for the single-premium form the *Einmalbeitrag* itself. A
lifelong-premium contract has no finite *Beitragssumme* without a convention; the cap is that
convention, and it is a parameter, not a citation.

**The first-order margins [std].** German practice runs two parallel bases over one contract:
*erster Ordnung* — prudent, statutorily required [REG-R8], fixing the *Bruttobeitrag* — and *zweiter
Ordnung*, the best estimate the projection runs on, with the *Sicherheitszuschlag* the wedge whose
**direction forks by risk** [REG-R47]. For care, prudence means higher incidence, faster
deterioration, slower recovery, longer duration in care and lower active mortality, because a life
that survives is a life that can claim:

| Margin | Value | Applied to | Direction |
|---|---|---|---|
| `inc_margin` | 1.25 | `inc_rate` | more claims |
| `det_margin` | 1.15 | `det_rate` | faster progression to the higher-paying grades |
| `rec_margin` | 0.80 | `rec_rate` | fewer recoveries, so longer spells |
| `care_mort_margin` | 0.85 | in-care mortality | longer annuities |
| `act_mort_margin` | 0.90 | active mortality | more lives survive to claim |

All five are **[std]** and the responsible actuary's judgment sets them in practice [REG-R11]
[REG-R56]. **This file used to add that no German source gives a *Sicherheitszuschlag* level for a
*Pflegetafel*. The DAV does** [R15] [REG-R8], by minimum *Pflegegrad*: a *Gesamtzuschlag* on
incidence of **24,5 / 21,4 / 20,5 / 24,0 / 31,2 %**, a *Gesamtabschlag* on *Invalidensterblichkeit*
of **28,5 / 24,2 / 24,2 / 24,3 / 25,7 %**, and **13,6 %** on *Aktivensterblichkeit*. Against those,
`inc_margin` 1.25 sits inside the published range and `act_mort_margin` 0.90 is close to 0.864; but
`care_mort_margin` 0.85 is **materially less prudent** than the published 0.715–0.758, and
`det_margin` and `rec_margin` have no published counterpart because the *Stufenmodell* has no
per-grade transitions. **Nothing here was changed**: these are pricing bases, and moving one moves
the worked example and the golden tests. The **first-order basis carries no lapse at all**, which is both
German practice and what keeps the model acyclic. Pricing blends the sexes at
`unisex_mix_male = 0.50` **[std]** while the projection uses the point's own sex; "pricing unisex on
a 50 / 50 mix while writing 60 / 40" is model risk 7 [REG-R34].

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t`, `x(t)`, `y(t)`, `g` | policy month, 0-based, `t = d0 … n − 1` with `d0 = duration_mth_init` and `n = proj_len` the number of projected months; attained age `age_at_entry + t // 12`; policy year `t // 12 + 1`; *Pflegegrad* `1 … 5` |
| `π_g` | `benefit_pct(g)`, the *Leistungsstaffel* percentage |
| `R` | `rente_mth`, the *vereinbarte Pflegerente* at *Pflegegrad* 5 |
| `P` | `premium_mth_pp()`, the level monthly gross *Beitrag* per policy |
| `m` | `prem_mode_months()` — 1, 3, 6, 12, or 0 for the *Einmalbeitrag* |
| `μ_A(t)`, `μ_g(t)`, `ι(t)` | force of active-life mortality at `x(t)`; force of mortality in *Pflegegrad* `g` = `mort_mult(g) × μ_A(t)`; force of incidence into care, **0** while `t < wartezeit_months` |
| `s_g` | `entry_share(g)`, the distribution of the grade first entered |
| `δ_g(t)`, `ρ_g(t)`, `w(t)` | forces of deterioration `g → g+1` and recovery `g → g-1` (from PG1, to active); and the monthly lapse probability from the active state, `lapse_rate_mth`, **0** outside the premium term |
| `ℓ_A(t)`, `W_{g,z}(t)`, `ℓ_g(t)` | `pols_act(t)`, `pols_karenz(t, g, z)`, `pols_pg(t, g)` |
| `E_g(t)` | `esc_pg(t, g)`, the escalation-weighted counterpart of `ℓ_g` |
| `d`, `K` | `leistungsdynamik`, the annual escalation of the annuity in payment; `karenz_months` |
| `i` | `rechnungszins`; `v = (1 + i) ** (-1/12)`, used **only** in the pricing engine |
| `α`, `β`, `γ`, `c`, `f` | `acq_permille/1000`, `admin_prem_pct`, `admin_mth_pp`, `claim_expense_pp`, `expense_infl` |

Forces are per annum; `R`, `P` and every cash-flow component are EUR.

### Rates, forces and the monthly step

Every shipped rate is **annual**, and every transition inside a month is computed from **forces held
constant over the month**, the competing transitions sharing one survival probability in proportion
to their forces. Writing `q` for an annual rate, the force is `μ = -ln(1 - q)`; with forces
`μ_1 … μ_k` out of a state,

    p_stay = exp(-(μ_1 + … + μ_k) / 12)        p_j = (μ_j / Σ_k μ_k) * (1 - p_stay)

so `p_stay + Σ_j p_j = 1` exactly, by construction. This is the standard constant-force,
proportional-allocation convention, and **declaring it is not optional**: adding monthly rates
instead, or applying `q/12`, gives different answers wherever the forces are large — which on this
product is exactly where the money is. Pitfalls 7 and 8 test it. From the active state, with `μ_A`
and `ι`, and from *Pflegegrad* `g`, with `μ_g`, `δ_g`, `ρ_g` (`δ_5 = 0`; `ρ_1` leads to the active
state):

    p_act_stay(t)  = exp(-(μ_A + ι) / 12)      p_pg_stay(t, g)   = exp(-(μ_g + δ_g + ρ_g) / 12)
    p_act_death(t) = (μ_A / (μ_A + ι)) * (1 - p_act_stay(t))
    p_act_care(t)  = (ι   / (μ_A + ι)) * (1 - p_act_stay(t))
    p_pg_death(t, g)  = (μ_g / S) * (1 - p_pg_stay(t, g))
    p_pg_worse(t, g)  = (δ_g / S) * (1 - p_pg_stay(t, g))
    p_pg_better(t, g) = (ρ_g / S) * (1 - p_pg_stay(t, g)),        S = μ_g + δ_g + ρ_g

Both sets are published as cells, and `check_states()` rests on their summation to one.
### The in-force recursions

**Active state.** Entrants leave, deaths leave, reactivations arrive, and the survivors of all three
are exposed to lapse — **lapse acting after the insured decrements**, the same ordering frlib's term
model uses and stated because the alternatives give different answers:

    pols_entry(t, g) = ℓ_A(t) * p_act_care(t) * s_g
    pols_reactiv(t)  = [ ℓ_1(t) + Σ_z W_{1,z}(t) ] * p_pg_better(t, 1)
    pols_lapse(t)    = [ ℓ_A(t) * p_act_stay(t) + pols_reactiv(t) ] * w(t)
    ℓ_A(t+1)         = [ ℓ_A(t) * p_act_stay(t) + pols_reactiv(t) ] * (1 - w(t))

**The *Karenz* ledger**, present only when `K > 0`. Entrants join at `z = 1` and advance one month at
a time, subject to the same transitions as a served life; the clock is **discarded** on reactivation,
because the *Karenzzeit* runs from onset and a recovered life who later relapses starts a new onset:

    W_{g,1}(t+1)    = pols_entry(t, g)
    W_{g,z+1}(t+1)  = Σ_h W_{h,z}(t) * p_karenz(t, h → g),      1 ≤ z < K
    pols_grad(t, g) = Σ_h W_{h,K}(t) * p_karenz(t, h → g)

where `p_karenz(t, h → g)` is `p_pg_stay` for `h = g`, `p_pg_worse` for `g = h + 1`, `p_pg_better`
for `g = h - 1`, and zero otherwise. When `K = 0` the ledger is empty and
`pols_grad(t, g) = pols_entry(t, g)` — the degenerate case the base run runs in.

**The paying ledger**, with the `g = 1` recovery term flowing to the active state instead and the
`g = 5` deterioration term absent:

    ℓ_g(t+1) = ℓ_g(t) * p_pg_stay(t, g) + ℓ_{g-1}(t) * p_pg_worse(t, g-1)
             + ℓ_{g+1}(t) * p_pg_better(t, g+1) + pols_grad(t, g)

**The escalation ledger** is the same population weighted by each life's own escalation factor since
its annuity began: the identical recursion with one extra factor, entrants joining at weight 1.

    E_g(t+1) = (1 + d) ** (1/12) * [ E_g(t) * p_pg_stay(t, g) + E_{g-1}(t) * p_pg_worse(t, g-1)
                                   + E_{g+1}(t) * p_pg_better(t, g+1) ] + pols_grad(t, g)

When `d = 0` this is the `ℓ_g` recursion exactly, so `E_g ≡ ℓ_g` in the base run — an invariant
`check_esc_ledger()` asserts. Carrying escalation as a **value ledger** rather than a
duration-since-onset cohort dimension is what keeps the model O(n) instead of O(n²); the price is
that it reports only the aggregate escalation, which is all the cash flow needs.

**Deaths, and the closure.**

    pols_death(t)       = ℓ_A(t) * p_act_death(t)
                        + Σ_g [ ℓ_g(t) + Σ_z W_{g,z}(t) ] * p_pg_death(t, g)
    pols_dead_cum(t+1)  = pols_dead_cum(t) + pols_death(t)
    pols_lapse_cum(t+1) = pols_lapse_cum(t) + pols_lapse(t)

    pols_if(t) + pols_dead_cum(t) + pols_lapse_cum(t) = pols_if_init()     for every t

The last line is `check_states()`. Because `mort_rate` is forced to 1 in the final year of age, the
identity closes at `t = n` — one past the last projected month — with `pols_if = 0`, so the
decrements sum to `pols_if_init()` exactly
— a closure a reader can check with a calculator on the worked example.
### Premium, waiver and the premium-paying population

    pols_in_term(t) = pols_if(t)                      if x(t) < prem_end_age else 0
    pols_waived(t)  = Σ_{g : π_g > 0} ℓ_g(t)          restricted to the in-term population
    pols_prem(t)    = pols_in_term(t) - pols_waived(t)

Three consequences follow directly from the *Leistungsstaffel*, and each is a test. A life in a
*Karenz* ledger **pays**, because no annuity is yet payable and the waiver runs with the annuity. A
life at *Pflegegrad* 1 on the `delib_std` grid **pays**, because `π_1 = 0`; on the `bahr` grid,
where `π_1 = 0.10`, the same life is **waived**. And a life that is downgraded out of the paying
grades **starts paying again**, so `pols_prem` is not monotone.

The instalment is charged only on due months:

    premium_due(t)  = (m > 0) and (t % m == 0) and (x(t) < prem_end_age)
    premium_pp(t)   = P * m           if premium_due(t) else 0
    premiums(t)     = premium_pp(t) * pols_prem(t)

For the *Einmalbeitrag* (`m = 0`), `premium_pp(0) = P_single` and zero thereafter. A waiver that
begins between two due dates therefore takes effect **at the next due date**, which is the German
convention for a *Beitragsbefreiung* on a fractionated contract and is stated because the
alternative — refunding the unearned instalment — is a different and equally arguable rule the model
does not implement.

`cum_prem_max_pp(t)` is the premium payable to date on an uninterrupted path, `P` times the number
of premium-months elapsed inside the term (for the single-premium form, `P_single` from `t = 0`).
It is a **deterministic** quantity, not a ledger, and it is what both the *Rückkaufswert* and the
*Beitragsrückgewähr* are struck on.

### Benefits

    claims(t, "ANNUITY") = R * Σ_g π_g * E_g(t)
    claims(t, "LAPSE")   = rkw_pp(t) * pols_lapse(t)
    claims(t, "DEATH")   = brg_pp(t) * pols_death(t)
    claims(t)            = claims(t, "ANNUITY") + claims(t, "LAPSE") + claims(t, "DEATH")

with

    rkw_pp(t) = rkw_prem_ratio(min(y(t), 40)) * cum_prem_max_pp(t) * (1 - stornoabzug_rate)
    brg_pp(t) = cum_prem_max_pp(t)   if beitragsrueckgewaehr else 0.0

Note what `claims(t, "ANNUITY")` is weighted on: `E_g(t)`, the escalation ledger, **not** `ℓ_g(t)` —
identical in the base run, not identical with the dynamic on, and using `ℓ_g` would silently drop the
escalation. Note also that the *Karenz* ledger contributes nothing: a life inside its deferred period
is in care, counted in `pols_if`, pays its premium and receives no annuity.

**The *Beitragsrückgewähr* implemented here is the gross form** — return of premiums payable to date,
with **no** offset for annuity already paid. The market's more common form nets the annuity off
[S4]; the model does not, because the netting is floored at zero **per life** and the
ledgers are aggregates, so netting at the aggregate level would let a life that received a large
annuity subsidise one that received none. The consequence — the option overstates the death benefit
relative to the market-standard form — is stated rather than hidden, and pitfall 11 asserts it.

### Expenses and net cash flow

    expense_infl_factor(t) = (1 + f) ** (t / 12)
    acq_expense_pp()       = α * beitragssumme()
    expenses(t)            = acq_expense_pp() * 1{t = 0}
                           + γ * expense_infl_factor(t) * pols_if(t)
                           + β * premiums(t)
    claim_expenses(t)      = c * expense_infl_factor(t) * Σ_{g : π_g > 0} ℓ_g(t)
    net_cf(t)              = premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
    liability_cf(t)        = -net_cf(t)

The acquisition charge falls at `t = 0` only, so **an in-force model point never incurs it** — its
frame opens at `t = duration_mth_init > 0`. That is correct (the cost was incurred before the
valuation date) and it is worth knowing before comparing an in-force point's first row with a
new-business point's.

`claim_expenses` is per **annuity payment made**, so it is weighted on the paying grades only and a
*Pflegegrad* 1 life on the `delib_std` grid generates none. It is published as its own `result_cf()`
column because it is a per-event cost rather than a per-policy one.

### The pricing engine — `premium_mth_pp()`

Where `premium_mth > 0` on the model point, that is the premium and the engine is not consulted.
Where it is `0.0`, `P` is struck by equivalence on the **first-order** bases: every rate multiplied
by its margin, blended 50 / 50 across the sexes, **no lapse**, discounted at `v = (1+i)^(-1/12)`.
The `tar_*` ledgers obey exactly the recursions above with `w ≡ 0` and the margined forces. Define,
over `t = 0 … n − 1` on the tariff ledgers:

    A  = Σ_t v**t * R * Σ_g π_g * tar_esc_pg(t, g)                  EPV of the annuity
    U  = Σ_{t : premium_due(t)} v**t * m * tar_pols_prem(t)         EPV of premium in units of P
    G  = Σ_t v**t * γ * expense_infl_factor(t) * tar_pols_if(t)     EPV of per-policy admin
    C  = Σ_t v**t * c * expense_infl_factor(t) * Σ_{g:π_g>0} tar_pols_pg(t, g)
    D1 = Σ_t v**t * (premium-months elapsed at t) * tar_pols_death(t)    (0 unless BRG)
    a1 = α * 12 * (min(prem_end_age, beitragssumme_cap_age) - age_at_entry)

Everything on the benefit side that scales with `P` — the *Beitragsrückgewähr* and the *Zillmerung*
allowance — is linear in `P`, so `P * U = A + P * D1 + P * a1 + β * P * U + G + C` solves in closed
form:

    P = (A + G + C) / [ U * (1 - β) - D1 - a1 ]
    premium_mth_pp()    = rating_factor * P
    prem_net_level_pp() = A / U            the net level premium, benefits only

For the *Einmalbeitrag*, `U = 1` and the same expression gives the *Einmalbeitrag* directly. The
*Risikozuschlag* multiplies the **gross** premium, never the benefit.

`check_prem_equiv_resid(t)` publishes the per-month discounted imbalance
`v**t * [premium_pp_tar(t) * tar_pols_prem(t) - benefit_tar(t) - expense_tar(t)]`, whose sum over `t`
is zero when the equivalence holds; `check_prem_equiv()` is that sum against a tolerance scaled by
`P * U`. It is not a tautology: both sides are assembled from the ledgers rather than from the
closed form, so substituting a best-estimate rate into one leg, or dropping the *Zillmerung* term,
makes it fail.
### `result_cf()`

`result_cf()` returns a `DataFrame` indexed by `t` (`df.index.name == "t"`), contiguous from
`duration_mth_init()` to `proj_len() - 1`, in this column order — eleven cash-flow and exposure columns
and then `liability_cf`:

| # | Column | Meaning |
|---|---|---|
| 1 | `pols_if` | In force at the **start** of month `t`; first value equals `pols_if_init()` exactly |
| 2 | `pols_act` | Of which active |
| 3 | `pols_care` | Of which in care — the *Karenz* and paying ledgers together |
| 4 | `pols_prem` | Of which actually paying a *Beitrag* |
| 5 | `premiums` | *Beitrag* income, in advance |
| 6 | `claims_annuity` | *Pflegerente* paid, in advance |
| 7 | `claims_lapse` | *Rückkaufswert* paid on surrender, at month end |
| 8 | `claims_death` | *Beitragsrückgewähr* paid on death, at month end; structurally 0 in the base run |
| 9 | `expenses` | Acquisition, per-policy administration and premium-related administration |
| 10 | `claim_expenses` | Per-annuity-payment claims cost |
| 11 | `net_cf` | `premiums - claims_annuity - claims_lapse - claims_death - expenses - claim_expenses` |
| 12 | `liability_cf` | The same stream outgo-positive, `-net_cf(t)` exactly. Published as a column because the conventions suite verifies the sign convention in the frame rather than in prose |

A second frame, `result_states()`, publishes the ledgers and rates a reader needs to follow the
projection: `pols_pg1` … `pols_pg5`, `pols_karenz`, `pols_entry`, `pols_grad`, `pols_reactiv`,
`pols_death`, `pols_lapse`, `mort_rate`, `mort_rate_care_pg5`, `inc_rate`, `lapse_rate` and
`premium_pp`. It is not part of the house contract and carries no `check_*`.

### The published identities

`check_*()` takes no argument and returns a **`bool`** over all `t`; the per-`t` residual is
`check_*_resid(t)`. Six identities are published, and the conventions suite calls every one of them
on every model point.

| Check | Identity |
|---|---|
| **`check_net_cf`** (delib ruling 1) | `net_cf(t) = premiums(t) - claims(t, "ANNUITY") - claims(t, "LAPSE") - claims(t, "DEATH") - expenses(t) - claim_expenses(t)` — `net_cf` rebuilt from the statement's own published parts, so the headline number is reconciled in code and not only in prose |
| `check_pols_roll_fwd` | `pols_if(t+1) = pols_if(t) - pols_death(t) - pols_lapse(t)`: lives leave the in-force population only by death or surrender, and every *Pflegegrad* transition is internal |
| `check_states` | `pols_act(t) + Σ_{g,z} pols_karenz(t,g,z) + Σ_g pols_pg(t,g) + pols_dead_cum(t) + pols_lapse_cum(t) = pols_if_init()`: the ledgers plus the absorbed partition the initial cohort at every `t` |
| `check_waiver` | `pols_prem(t) + pols_waived(t) = pols_in_term(t)`: the *Beitragsbefreiung* splits the in-term population and neither loses nor creates a policy |
| `check_esc_ledger` | `esc_pg(t,g) ≥ pols_pg(t,g)` for every `t, g` when `leistungsdynamik ≥ 0`, with **equality** when it is zero |
| `check_prem_equiv` | `Σ_t check_prem_equiv_resid(t) ≈ 0`: the gross premium closes the first-order equivalence, assembled from the tariff ledgers rather than from the closed form |

`check_net_cf` is mandatory across the library; the other five are this product's own. All six use
`roll_fwd_tol` from `basis_table.csv`.

---

## Processing order

Inside month `t`, in this order. Nothing here is optional: several of the pitfalls below are simply
this list executed in a different sequence.

1. **Set the clocks.** `x(t) = age_at_entry + t // 12`; `y(t) = t // 12 + 1`. At
   `t = duration_mth_init()` seed the ledgers from `status` and `pols_if_init()` instead of rolling
   them in — an active point seeds `pols_act`, a point in claim seeds `pols_pg(·, g)` at its grade
   with the *Karenz* already served.
2. **Classify the in-force.** `pols_in_term(t)`, then `pols_waived(t)` from the paying grades, then
   `pols_prem(t)` as the difference. The *Karenz* ledger is in-term and unwaived.
3. **Collect the *Beitrag*, in advance.** If `premium_due(t)`, `premiums(t) = P × m × pols_prem(t)`;
   otherwise zero. Accumulate `cum_prem_max_pp(t)`.
4. **Pay the *Pflegerente*, in advance**, on the **escalation** ledger:
   `claims(t, "ANNUITY") = R × Σ_g π_g × esc_pg(t, g)`. The *Karenz* ledger receives nothing.
5. **Charge start-of-month expenses.** `acq_expense_pp()` at `t = 0` only; per-policy administration
   on `pols_if(t)`, inflated; premium-related administration on the premium just collected; and
   `claim_expenses(t)` on the annuity payments just made.
6. **Look up the month's forces at `x(t)`.** `μ_A`, and `ι` — **zero while `t < wartezeit_months`**;
   `μ_g = mort_mult(g) × μ_A`; `δ_g`; `ρ_g`, damped above `rec_age_ref`. Then `w(t)`, zero outside
   the premium term.
7. **Apply the transitions over the month**, constant forces, proportional allocation. From the
   active state: death, entry into care split by `entry_share`, or stay. From each grade, in both
   the *Karenz* and the paying ledger: death, deterioration, recovery, or stay.
8. **Advance the *Karenz* clock** by one month and graduate the `z = K` cohort into `pols_pg`.
9. **Apply lapse**, to the survivors of the active state **after** the insured decrements and after
   the reactivation inflow. `pols_lapse(t)` is the result; nothing in care lapses.
10. **Pay the end-of-month benefits.** `claims(t, "LAPSE") = rkw_pp(t) × pols_lapse(t)`, and
    `claims(t, "DEATH") = brg_pp(t) × pols_death(t)` where the option is on.
11. **Roll the escalation ledger**: escalate the surviving weights by `(1 + d)^(1/12)`, then add the
    graduating entrants at weight 1.
12. **Post the ledgers to `t + 1`** and form
    `net_cf(t) = premiums - claims_annuity - claims_lapse - claims_death - expenses - claim_expenses`.

The projection ends at `t = proj_len() - 1`. There is **no maturity, no survival benefit and no tail
state**: the contract runs for life, and the closure identity is carried by the decrements.
## Known modeling pitfalls

The specific ways an implementation of *this* product looks right and is wrong. Each is a test in
`tests/test_pflegerentenversicherung_de.py`.

1. **Applying an average benefit percentage to an average survival curve.** Grade and mortality are
   correlated: *Pflegegrad* 5 pays most and is lived in shortest. Assert `claims(t, "ANNUITY")`
   equals `R × Σ_g π_g × esc_pg(t, g)`, and that replacing it by `π̄ × R × pols_care(t)`, with `π̄`
   the **entry-mix** mean percentage 0.3815, understates the projected annuity total by 30 % on the
   anchor cell — 9,248.24 € against 13,200.11 €. The trap is that the substitution is *exact* at
   `t = 1`, where the stock is still the entry mix; the error opens as deterioration moves the stock
   up the schedule to a stock-weighted mean of 0.544519. Substituting the **stock**-weighted mean
   instead reproduces the total by construction and tests nothing.
2. **Pricing the annuity in payment on an annuity table.** DAV 2004 R is prudent about people living
   *longer* [REG-R49]; this annuity is paid to a heavily impaired population. Assert
   `mort_rate_care(t, g) ≥ mort_rate(t)` for every `g` and `t`, strictly increasing in `g`, and that
   the **force** multiple `mort_force_care(t, g) / mort_force(t)` is exactly `mort_mult(g)` — 9.0 at
   grade 5 — at every age below the limiting one. Assert it on forces and not on rates: the *rate*
   ratio at grade 5 falls from 8.97 at age 45 to 6.85 at 85, 4.31 at 95 and 1.00 at the limiting age,
   because a rate saturates and a force does not. That compression is the scale, not the basis.
3. **Treating "in claim" as one state exited only by death.** There are three exits. Assert
   `Σ_t pols_reactiv(t) > 0`, that recovery moves lives down the grades, and that suppressing
   recovery and downgrade raises the projected annuity total.
4. **Insuring *Pflegegrad* 1 by accident.** On `delib_std`, `π_1 = 0`. Assert `claims(t, "ANNUITY")`
   is invariant to `pols_pg(t, 1)` and that a grade-1 life is counted in `pols_prem`, not
   `pols_waived`.
5. **Waiving the premium at the wrong grade.** Assert `pols_waived` excludes grade 1 on `delib_std`
   (point 1) and includes it on `bahr` (point 5), with `check_waiver()` closing on both.
6. **Forgetting that the premium revives on a *Herabstufung*.** Assert the *flow* rather than the
   stock: `Σ_t pols_pg(t,2) × p_pg_better(t,2) > 0` on `delib_std`, lives leaving the insured grades
   and starting to pay again; `pols_prem(t) ≥ pols_act(t)` at every `t`, strictly wherever
   `pols_pg(t,1) > 0`, because an uninsured-grade life and a *Karenz* life both pay; and
   `check_waiver()` closing throughout. The **stock** `pols_prem(t)` is nevertheless monotone
   decreasing on every shipped model point — attrition dominates the revival flow by three orders of
   magnitude — so a test asserting non-monotonicity would be asserting a coincidence, not the
   mechanic.
7. **Adding monthly transition probabilities instead of allocating one survival.** Assert
   `p_pg_stay + p_pg_death + p_pg_worse + p_pg_better == 1` to 1e-12 for every `t` and `g`, and the
   same for the three active-state probabilities.
8. **Dividing an annual rate by twelve.** Assert `mort_rate_mth(t) == 1 - (1 - mort_rate(t))**(1/12)`
   and the same form for lapse; that the monthly rate is strictly **below** the annual one wherever
   that is positive, which is the house convention; and that `q/12` is strictly below
   `1 - (1 - q)^(1/12)`, so **dividing by twelve understates the monthly decrement**. The direction
   is worth stating because it is the opposite of the intuition: twelve monthly rates *added*
   overshoot the annual rate (`12 x 0.00006499 = 0.00077984` against `q_A(45) = 0.00077956`), while
   twelve of them *compounded* reproduce it exactly. An earlier draft of these notes asserted the
   overshoot the wrong way round; the model contradicted it and the model is right.
9. **Treating the *Karenzzeit* as a benefit gate on the aggregate.** It is a deferral clock per
   onset. On point 7 assert `Σ_t Σ_g pols_grad(t,g) < Σ_t Σ_g pols_entry(t,g)` strictly, the
   shortfall equalling deaths and recoveries recorded inside the *Karenz* ledger.
10. **Escalating the annuity at general-population duration.** With `d = 0.02` on point 8 the
    projected annuity total rises from 13,200.11 € to 15,101.44 €, **+14,4 %**, and the equivalence
    premium by **+12,2 %**. Assert both, and `esc_pg == pols_pg` exactly on point 1. An earlier draft
    of these notes predicted "less than 5 %" from a four-year spell; the model contradicts it and the
    model is right on the shipped basis, because the escalation compounds over elapsed time in
    **care** — *Pflegegrad* 1 months included, where nothing is paid — and because deterioration puts
    the largest benefit percentages at the end of a spell, where the escalation factor is largest.
    `ln(1.144) / ln(1.02) = 6,8` years of payment-weighted elapsed duration against a mean spell in an
    insured grade of 5,5 years. The comparison that survives is the weaker one: 14,4 % is below the
    18 % the same escalation buys on a healthy-life annuity of seventeen-year duration, but not far
    below it, and a *Leistungsdynamik* on this basis is not cheap.
11. **Netting the annuity off a *Beitragsrückgewähr* at the aggregate level.** The floor at zero is
    per life; the model pays the **gross** form. Assert
    `claims(t, "DEATH") == cum_prem_max_pp(t) × pols_death(t)` on point 9 and `== 0.0` on point 1.
12. **Paying a surrender value out of the paying state.** Assert `pols_lapse(t) ≤ pols_act(t)`,
    `claims(t, "LAPSE") == 0` wherever `pols_act(t) == 0`, and `lapse_rate(t) == 0` once
    `x(t) ≥ prem_end_age` (point 4).
13. **Charging the *Zillmerung* on the wrong base.** The 25 ‰ ceiling is a per-mille of the
    *Beitragssumme*, not of the annual premium [REG-R16]. Assert
    `acq_expense_pp() == 0.025 × premium_mth_pp() × 12 × (min(prem_end_age, 85) - age_at_entry)`,
    charged at `t = 0` only, so an in-force point never incurs it.
14. **Striking the equivalence premium on the projection basis.** Assert `check_prem_equiv()` is
    `True`, that `premium_mth_pp()` is invariant to every value in `lapse_table.csv`, and that
    `tar_inc_rate(t)` exceeds the **unisex-blended** best-estimate incidence
    `0.5 i_M(x) + 0.5 i_F(x)` by exactly `inc_margin` at every age below the `inc_cap`. Against the
    anchor cell's own *female* incidence the ratio is 1.128 at age 45 and 1.089 at 85, not 1.25:
    the blend and the margin are two separate operations and only the second is prudence.
15. **Pricing on the model point's own sex.** Assert points 1 and 2 — female and male, identical
    otherwise — have **equal** `premium_mth_pp()` and **unequal** projected annuity totals, the
    female point's being larger [REG-R34].
16. **Collecting a premium in a month that is not a due date.** Assert `premiums(t) == 0` at every
    non-due `t` on points 3, 4 and 5, and `premium_pp(t) == premium_mth_pp() × prem_mode_months()` at
    every due `t`.
17. **Using the *Pflegegrad* stock distribution as the entry mix.** The stock is
    13,8 / 40,4 / 29,6 / 11,8 / 4,3 % at end-2023 [R18]; entrants are not. Assert `Σ_g entry_share(g) == 1.0` and that the
    model's own stock share at grades 4 and 5 over the whole projection **exceeds** `entry_share`.

Two further errors are worth naming because they are the ones a *user* will make. **Reading a
payment-frequency difference as a price difference**: the model folds the *Ratenzahlungszuschlag*
into the administration assumption, so annual mode prices slightly *below* monthly, the opposite
sign to a real tariff. And **treating `proj_len()` as the last projected index**: it is the number
of projected months, the frame's exclusive end, so the last index is `proj_len() - 1`; and because
the frame starts at `duration_mth_init()`, an in-force point publishes `proj_len() - duration_mth_init()`
rows, not `proj_len()`.

---

## Policyholder behaviour modelling

Every dynamic formula here is a **[std]** reference construction; **no German calibration evidence
for any of them exists in this corpus** (research gap 20).

- **Base lapse [std].** The duration table in class (c), from the active state only, zero after the
  premium term ends. The argument for the shape, not its level, is *Zillmerung*: the *Rückkaufswert*
  is near zero for the first years [REG-R16] [REG-R28], so an early lapse is expensive to the
  policyholder and the profile is flatter than a savings product's.
- **No lapse from a paying grade [std].** A claimant with a waived premium has no premium to default
  on and a live annuity to forfeit. A *Pflegegrad* 1 life on `delib_std` does still pay and could in
  principle lapse; the population is small and the model does not model it.
- **Premium-shock lapse [std], optional, off.** The *Beitrag* is level and guaranteed, so the
  affordability shock frlib's `temporaire_deces` models has no counterpart here. What could replace
  it is a *Zahlbeitrag* shock — a withdrawal of the surplus rebate raises the amount actually called
  without invoking § 163 [REG-R27] [REG-R53] — and the model carries no rebate, so the module is
  empty and is named only so that a user who adds a rebate knows what to add with it.
- **Selective lapsation [std], optional, off.** Lapsers are healthier, so persisters' incidence
  should be loaded: `inc_rate_eff(t) = inc_rate(t) × [1 + λ × max(0, w_cum(t) - w_ref)]` with
  `w_ref = 0.30`, `λ = 0.25` and base run `λ = 0`. The effect is **smaller** here than on a term
  cover, because cumulative lapse is largely complete decades before the risk period.
- **Not modelled at all, each for a stated reason.** *Beitragsfreistellung* take-up — no split
  between the three German exits exists in the corpus [REG-R28]. *Beitragsdynamik* acceptance — a
  behaviourally driven second premium path with no evidence behind it. *Höherstufung* application
  behaviour — the insured applies and the state re-assesses [R6], so grade change is biometric here
  rather than elective. And anti-selection at purchase, which underwriting removes [S4] and which
  decays long before the claims arrive.

---

## Worked example

**Configuration.** Model point 1, the anchor cell, in full: `point_id = 1`;
`policy_id = "PFL-000001"`; `sex = F`; `age_at_entry = 45`; `duration_mth_init = 0`;
`status = aktiv`; `rente_mth = 1,000.00` EUR per month, the *vereinbarte Pflegerente* at
*Pflegegrad* 5; `staffel_id = delib_std`, so the *Leistungsstaffel* is
0 / 30 / 50 / 75 / 100 % across grades 1 to 5; `prem_end_age = 110`, equal to `omega_age`, so the
*Beitrag* is payable for life; `prem_mode = monthly`, so `prem_mode_months = 1` and a *Beitrag* is
due in every month of the term; `premium_mth = 0.00`, the sentinel that makes the model strike the
*Beitrag* by equivalence; `rating_factor = 1.00`, standard rates; `wartezeit_months = 0`;
`karenz_months = 0`; `leistungsdynamik = 0.00`; `beitragsrueckgewaehr = False`;
`stornoabzug_rate = 0.00`; `pols_if_init = 1.0`. Hence `proj_len() = 12 × (110 − 45) = 780`, the
frame runs from `t = 0` to `t = proj_len() − 1 = 779`, and the projection covers attained ages 45 to 109 — 780
monthly rows, of which the table below shows a representative selection together with the
full-precision totals.

**Assumptions, each tagged.** *Rechnungszins* `i = 1.00 %` p.a., used **only** in the pricing
engine [REG-R14] [REG-R15]. Active-life mortality
`mort_rate(F, x) = 1 − exp(−4.76290e−06 × 1.119962^x)` **[std]**, anchored at
`q(65) = 0.75 %` and `q(85) = 7.0 %`, with `mort_rate(F, 109) = 1.0` by the limiting-age convention
**[std]**. Incidence `inc_rate(F, x) = min(0.0110 × exp(0.1400 × (x − 65)), 0.50)` **[std]**,
anchored on prevalence doubling every five years of age above 75 — an anchor the retrieved
*Pflegequoten* put nearer a factor of 1,8 over 70–90 [R18], reported and not changed. Entry mix
0.20 / 0.38 / 0.24 / 0.13 / 0.05 across grades 1 to 5 **[std]**. Deterioration
0.28 / 0.24 / 0.20 / 0.16 / 0.00 and recovery 0.10 / 0.06 / 0.04 / 0.02 / 0.01 a year **[std]**, the
recovery rates damped by `exp(−0.10 × max(0, x − 75))` **[std]**. In-care mortality multiples
1.5 / 2.5 / 3.5 / 6.0 / 9.0 on the active force **[std]**. Lapse from the active state
6.0 / 5.0 / 4.0 / 3.5 / 3.0 % in policy years 1 to 5, 2.5 % in years 6–10, 2.0 % in 11–20 and 1.5 %
from year 21 **[std]**, converted by `1 − (1 − q)^(1/12)`. *Rückkaufswert*
0.00 / 0.00 / 0.05 / 0.12 / 0.20 of premiums paid in policy years 1 to 5, rising to 0.42 by year 10
and 0.70 by year 40 **[std]**, with `stornoabzug_rate = 0`. Expenses **[std]**: acquisition
`25 ‰ × Beitragssumme` at `t = 0`, the *Beitragssumme* being `P × 12 × (85 − 45) = 480 P`;
administration 3.0 % of each *Beitrag* collected plus 2.00 € per policy in force per month;
claim expense 1.50 € per annuity payment; expense inflation 1.5 % a year. First-order margins
**[std]**: incidence × 1.25, deterioration × 1.15, recovery × 0.80, in-care mortality × 0.85,
active mortality × 0.90, and **no lapse** in the tariff basis. Pricing blended 50 / 50 male / female
**[std]** [REG-R34]; the projection runs on the female basis. No *Wartezeit*, no *Karenzzeit*, no
*Leistungsdynamik*, no *Beitragsrückgewähr*, no *Überschussbeteiligung* and no behaviour modules.

The band the research file argues for this configuration is **about 50,00 € to 100,00 € a month**
**[std]** (product spec, footnote 9). It is derived arithmetic, not a market observation: a model
premium well outside it indicates an error in the bases, and one inside it is not thereby
validated. The table below prints the model's own equivalence premium; the text under it says which
end of the band it lands at and why.

### The model's own output

Every figure is transcribed from `Projection[1].result_cf()`, money to the cent and policy counts to
six decimals. The frame has **780 rows**, `t = 0 … 779`; fourteen are shown. `claims_death` is a
column of the frame, is **structurally zero at every `t`** here (`beitragsrueckgewaehr = False`), and
is omitted rather than printed as 780 zeros. The equivalence premium is
**`premium_mth_pp() = 64.198409` € a month**.

| `t` | `x(t)` | `pols_if` | `pols_care` | `pols_prem` | `premiums` | `claims_annuity` | `claims_lapse` | `expenses` | `claim_expenses` | `net_cf` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 45 | 1.000000 | 0.000000 | 1.000000 | 64.20 | 0.00 | 0.00 | 774.31 | 0.00 | -710.11 |
| 1 | 45 | 0.994793 | 0.000056 | 0.994748 | 63.86 | 0.02 | 0.00 | 3.91 | 0.00 | 59.93 |
| 2 | 45 | 0.989613 | 0.000111 | 0.989523 | 63.53 | 0.04 | 0.00 | 3.89 | 0.00 | 59.59 |
| 12 | 46 | 0.939288 | 0.000644 | 0.938758 | 60.27 | 0.26 | 0.00 | 3.71 | 0.00 | 56.29 |
| 60 | 50 | 0.798781 | 0.003771 | 0.795452 | 51.07 | 1.86 | 1.60 | 3.25 | 0.01 | 44.35 |
| 120 | 55 | 0.698284 | 0.009864 | 0.689306 | 44.25 | 5.52 | 3.92 | 2.95 | 0.02 | 31.85 |
| 240 | 65 | 0.547048 | 0.035456 | 0.514343 | 33.02 | 21.39 | 5.65 | 2.46 | 0.07 | 3.45 |
| 360 | 75 | 0.391509 | 0.080375 | 0.318167 | 20.43 | 45.97 | 5.83 | 1.84 | 0.17 | -33.38 |
| 420 | 80 | 0.276904 | 0.092056 | 0.193720 | 12.44 | 49.35 | 4.20 | 1.31 | 0.21 | -42.64 |
| 480 | 85 | 0.143383 | 0.073044 | 0.078218 | 5.02 | 36.02 | 1.87 | 0.67 | 0.18 | -33.71 |
| 540 | 90 | 0.039295 | 0.028934 | 0.013981 | 0.90 | 12.90 | 0.30 | 0.18 | 0.07 | -12.56 |
| 600 | 95 | 0.003283 | 0.003060 | 0.000696 | 0.04 | 1.20 | 0.01 | 0.02 | 0.01 | -1.19 |
| 660 | 100 | 0.000055 | 0.000053 | 0.000015 | 0.00 | 0.02 | 0.00 | 0.00 | 0.00 | -0.02 |
| 779 | 109 | 0.000000 | 0.000000 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **Total** | | **268.956131** | **24.241784** | **247.014740** | **15,857.95** | **13,200.11** | **2,191.72** | **1,941.10** | **52.67** | **-1,527.65** |

**The Total row is summed over all 780 rows at full precision and then rounded**, not summed from the
rounded cells, and here the two visibly differ: summing the rounded cells gives premiums 15,857.92,
`claims_annuity` 13,200.02, `claims_lapse` 2,191.67, expenses 1,941.02, `claim_expenses` 52.58 and
`net_cf` -1,527.51 — the last of these 0,14 € away. The gap is not noise that cancels. **107 of the
780 `claims_annuity` cells are positive amounts below half a cent**, and every one of them rounds
down to 0.00, so the error accumulates in one direction; `claim_expenses` does the same, its 1,50 €
per payment falling on a paying population of the order of 1e-5 for the first two decades.

### Three independent checks

**Check 1 — the equivalence premium, from the four actuarial values.** The premium is not read off a
rate card; it is the solution of the first-order equivalence, and the values that determine it are
published as cells: `epv_benefits() = A = 17,789.761930`, `epv_prem_units() = U = 313.500018`,
`epv_admin() = G = 892.884210`, `epv_claim_expense() = C = 69.389246`, with `β = admin_prem_pct =
0.030` and the *Zillmerung* allowance `a1 = 0.025 × 12 × (85 − 45) = 12.000000` in units of `P`:

    P = (17,789.761930 + 892.884210 + 69.389246) / (313.500018 x 0.970 - 12.000000)
      = 18,752.035386 / 292.095018  =  64.198409

which is `premium_mth_pp()` to the sixth decimal. Two by-products are worth reading. `U` is
**26,13 years'** worth of discounted premium, against the "of the order of 27 years' worth" the
research file argues from the other direction. And `prem_net_level_pp() = A / U = 56.745649`, so the
whole expense loading is `64.198409 / 56.745649 = 1.131336` — **13,13 %** over the net level premium,
of which the *Zillmerung* allowance alone is 2,53 € a month: strike `a1` out of the denominator and
the premium falls to `18,752.035386 / 304.095018 = 61.665`.

**Check 2 — the first month's decrements, from the annual rates.** Nothing here needs the model. Read
two annual rates out of the CSVs at age 45 female, convert them to forces, allocate one month's exits
between them in proportion, and apply the lapse rate afterwards:

    q_A(45) = 0.00077956    mu_A = -ln(1 - q_A) = 0.00077986
    i(45)   = 0.00066891    iota = -ln(1 - i)   = 0.00066913      mu_A + iota = 0.00144900

    p_act_stay(0)  = exp(-0.00144900 / 12)                        = 0.99987926
    p_act_death(0) = (0.00077986 / 0.00144900) x (1 - 0.99987926) = 0.00006498
    p_act_care(0)  = (0.00066913 / 0.00144900) x (1 - 0.99987926) = 0.00005576
                                                            sum   = 1.00000000 exactly

    w(0) = 1 - (1 - 0.06)^(1/12) = 0.00514301
    pols_act(1)   = 0.99987926 x (1 - 0.00514301) = 0.99473687
    pols_lapse(0) = 0.99987926 x 0.00514301       = 0.00514239
    pols_death(0) = 0.00006498     pols_care(1) = 0.00005576   (entrants, no Karenzzeit to serve)
    pols_if(1)    = 0.99473687 + 0.00005576       = 0.99479262

against the table's `pols_if(1) = 0.994793`, and the roll-forward closes on the same three numbers:
`1.00000000 - 0.00006498 - 0.00514239 = 0.99479262`. Note where the lapse falls — on the survivors of
**both** insured decrements, not on the opening cohort. Applying it to the opening cohort instead
would put `pols_lapse(0)` at 0.00514301, 6,2e-7 of a policy adrift in the first month and materially
more once the decrements are large. Both orderings are internally consistent and both close
`check_pols_roll_fwd()`, which is exactly why the processing order has to be **declared** rather than
inferred from a check.

**Check 3 — the first annuity payment, grade by grade.** The month-0 entrants split across the grades
by `inc_share`, and with `karenz_months = 0` they graduate in the same month, so
`pols_pg(1, g) = esc_pg(1, g) = pols_entry(0, g)`:

| `g` | `inc_share(g)` | `pols_pg(1, g)` | `benefit_pct(g)` | contribution |
|---:|---:|---:|---:|---:|
| 1 | 0.20 | 0.0000111516 | 0.00 | 0.00000000 |
| 2 | 0.38 | 0.0000211880 | 0.30 | 0.00635640 |
| 3 | 0.24 | 0.0000133819 | 0.50 | 0.00669095 |
| 4 | 0.13 | 0.0000072485 | 0.75 | 0.00543638 |
| 5 | 0.05 | 0.0000027879 | 1.00 | 0.00278789 |
| | 1.00 | 0.0000557578 | | **0.02127162** |

`1,000.00 × 0.00002127162 = 0.0212716` €, the table's `claims_annuity(1) = 0.02`. This is also the
arithmetic of pitfall 1. The entry-mix mean percentage is `0.38 × 0.30 + 0.24 × 0.50 + 0.13 × 0.75 +
0.05 × 1.00 = 0.3815`, and applying it to `pols_care(1)` reproduces the annuity **exactly**, because
at `t = 1` the stock *is* the entry mix. It does not stay that way: over the projection the stock
share by grade is 9.49 / 24.25 / 27.64 / 21.04 / 17.57 % against an entry share of
20 / 38 / 24 / 13 / 5 %, and the stock-weighted mean percentage is 0.544519. Applying the entry-mix
mean to `Σ_t pols_care(t) = 24.241784` gives 9,248.24 € against 13,200.11 € — a **30 % understatement
of the whole benefit**, produced by an error no total in the frame would reveal.

**The closure identity.** Read one month past the last projected row, at `t = proj_len() = 780`:
`pols_dead_cum(780) = 0.493968059928` and
`pols_lapse_cum(780) = 0.506031940072` sum to **1.000000000000** with `pols_if(780) = 1.5e-23`: the
decrements account for the entire policy, exactly, because `mort_rate` is forced to 1.0 at age 109.
The cash flow statement closes the same way at every `t` — at `t = 0`,
`64.198409 − 774.306859 = −710.108450`, with `expenses(0) = 770.380907 + 2.000000 + 1.925952`, the
allowance `0.025 × 30,815.236279`, the month's per-policy administration and 3,0 % of the *Beitrag*
just collected. The largest `check_net_cf_resid(t)` anywhere in the frame is 1.4e-14, and
`check_prem_equiv()` closes to 9.3e-12.

### Reading the result

**The premium lands at 64,20 € a month, in the lower half of the argued 50,00–100,00 € band** [std].
Three things put it there. The entry mix is weighted to the two lowest grades, which pay 0 % and
30 %, so the stock-weighted average benefit is 54,5 % of the *vereinbarte Rente*. The model's own
mean spell in an **insured** grade is 5,5 years, at the top of the three-to-five the research file
argues. And the expense loading is 13,13 %, modest because the claims cost is per payment and low.

**The sign pattern is the product's whole economic story.** Month 0 is -710,11 €, almost all of it the
25 ‰ *Zillmerung* allowance charged in one go. From `t = 1` the contract runs positive — the level
*Beitrag* is far above the risk premium — and the monthly margin decays from 59,93 € to 3,45 € by age
65. **`net_cf` turns negative for good at `t = 252`, attained age 66**, where the incidence curve
overtakes the level premium and, in the layer this model does not compute, where the *Deckungskapital*
peaks. Annuity outgo peaks at 49,82 € in month 407 (age 78) and the population in care at 0.092120 in
month 417 (age 79); the last three decades are run-off. Undiscounted the contract collects
15,857.95 € and pays 17,385.60 € of benefit and expense, for -1,527.65 € — not a loss but the
consequence of publishing an **undiscounted** stream whose income falls thirty years before its outgo.

### A second scenario: the male twin, model point 2

Model point 2 is model point 1 with `sex = M` and nothing else changed — the model's own statement of
the unisex tension: **the two cells are priced identically and project differently.**

| `t` | `x(t)` | `pols_if` | `pols_care` | `pols_prem` | `premiums` | `claims_annuity` | `claims_lapse` | `expenses` | `claim_expenses` | `net_cf` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 45 | 1.000000 | 0.000000 | 1.000000 | 64.20 | 0.00 | 0.00 | 774.31 | 0.00 | -710.11 |
| 1 | 45 | 0.994719 | 0.000045 | 0.994683 | 63.86 | 0.02 | 0.00 | 3.91 | 0.00 | 59.93 |
| 12 | 46 | 0.938452 | 0.000517 | 0.938027 | 60.22 | 0.21 | 0.00 | 3.71 | 0.00 | 56.30 |
| 120 | 55 | 0.688060 | 0.007570 | 0.681181 | 43.73 | 4.20 | 3.87 | 2.91 | 0.01 | 32.74 |
| 240 | 65 | 0.517213 | 0.024372 | 0.494872 | 31.77 | 14.23 | 5.44 | 2.35 | 0.05 | 9.71 |
| 360 | 75 | 0.332372 | 0.045899 | 0.291187 | 18.69 | 24.19 | 5.37 | 1.60 | 0.10 | -12.56 |
| 420 | 80 | 0.214158 | 0.047250 | 0.172470 | 11.07 | 22.80 | 3.80 | 1.05 | 0.11 | -16.68 |
| 480 | 85 | 0.098388 | 0.033682 | 0.069319 | 4.45 | 14.73 | 1.72 | 0.49 | 0.08 | -12.58 |
| 540 | 90 | 0.023361 | 0.012108 | 0.013274 | 0.85 | 4.73 | 0.33 | 0.12 | 0.03 | -4.36 |
| 600 | 95 | 0.001538 | 0.001188 | 0.000612 | 0.04 | 0.40 | 0.01 | 0.01 | 0.00 | -0.38 |
| **Total** | | **251.397804** | **13.561865** | **239.326567** | **15,364.38** | **6,936.34** | **2,086.29** | **1,871.13** | **28.29** | **4,442.33** |

`premium_mth_pp()` is **64.198409** on both cells, to every decimal, because the pricing engine reads
the unisex blend and never `sex()`. The projections are not close: the male cell's `claims_annuity`
total is **6,936.34 €, 52,5 % of the female cell's**, and its `net_cf` total is **+4,442.33 €** against
**-1,527.65 €**. That 5,969.98 € gap is the cross-subsidy the unisex rule requires, priced on a
50 / 50 mix; a book written 60 / 40 female against this price carries a tenth of it — about 597 € of
undiscounted net cash flow per policy — unfunded. Two drivers pull in opposite directions and
incidence wins: male active mortality is higher at every age (`q(M, 45) = 0.0016637` against
`q(F, 45) = 0.0007796`; `q(M, 85) = 0.1049833` against `0.0699052`), so fewer men survive to claim,
and male incidence is lower (`i(M, 85) = 0.1342987` against `i(F, 85) = 0.1808911`), so fewer of the
survivors claim.

### The switchable variants beside the anchor

All four cells run on the same tables and differ only in the model point. Totals over the whole frame,
summed at full precision and then rounded:

| | 1 — anchor | 2 — male twin | 5 — `bahr` grid | 8 — *Leistungsdynamik* |
|---|---:|---:|---:|---:|
| Configuration | F 45, `delib_std` | M 45, `delib_std` | F 50, `bahr`, annual | F 45, `d = 0.02` |
| `premium_mth_pp()` | 64.198409 | 64.198409 | 55.444644 | 72.038378 |
| `proj_len()` | 780 | 780 | 720 | 780 |
| `premiums` | 15,857.95 | 15,364.38 | 12,289.30 | 17,794.54 |
| `claims_annuity` | 13,200.11 | 6,936.34 | 10,110.36 | 15,101.44 |
| `claims_lapse` | 2,191.72 | 2,086.29 | 1,482.02 | 2,459.37 |
| `expenses` | 1,941.10 | 1,871.13 | 1,556.50 | 2,093.27 |
| `claim_expenses` | 52.67 | 28.29 | 57.74 | 52.67 |
| `net_cf` | -1,527.65 | 4,442.33 | -917.32 | -1,912.22 |

**The `bahr` grid is not simply a cheaper contract.** Point 5 enters five years later, so its premium
is not comparable with the anchor's; the *shape* is. On 10 / 20 / 30 / 40 / 100 % the middle steps are
roughly two thirds of `delib_std`'s while grade 1 is insured for the first time, and the second effect
surfaces where a reader would not look for it: `claim_expenses` is **higher** on point 5 (57.74 €)
than on the anchor (52.67 €) despite a frame sixty months shorter, because a grade-1 life now
generates an annuity payment and so a per-payment cost — about a tenth of the care-months that
`delib_std` charges nothing for — and because point 5 sits five years closer to the claim ages. The
same life is also **waived** on `bahr` and **pays** on `delib_std`.

**The *Leistungsdynamik* costs more than the draft of these notes predicted**, and pitfall 10 has been
rewritten to the model's number: +14,4 % on the annuity total and +12,2 % on the premium, not the
"less than 5 %" a four-year spell suggests. `esc_pg == pols_pg` exactly on the anchor at all 780 × 5
combinations — `check_esc_ledger()` asserts it — and diverges on point 8: at `t = 480`,
`esc_pg(480, 3) = 0.024913` against `pols_pg(480, 3) = 0.022576`, a factor of 1.1035 which is exactly
the average escalation the lives then in grade 3 have accrued.

**What the model and test stages changed in these notes.** Six things, listed so the diff is not
silent. The worked example above replaced a placeholder. Model point 9 acquired a premium-paying term
to age 65, for the reason given under *The fourteen model points*. Pitfalls 1, 2, 6, 10 and 14
carried numeric predictions the model contradicts and were rewritten to what the model actually
produces — respectively the entry-mix rather than the stock-weighted mean percentage, the force
rather than the rate multiple, the revival *flow* rather than a non-monotone stock, +14,4 % rather
than "less than 5 %", and the unisex-blended rather than the sex-specific incidence. **Pitfall 8
asserted an inequality in the wrong direction** — that twelve times the monthly rate is below the
annual rate — and was rewritten when the test module put it to the model: twelve monthly rates
*added* overshoot, and it is `q/12` that falls short. The count of sub-cent `claims_annuity` cells
above was 108 in the draft and is **107** in the frame. `liability_cf` was added to the
`result_cf()` column list as column 12, because the conventions suite verifies the sign convention in
the frame. And two paragraphs duplicated in the draft — the *Currency, sign and rounding* bullet and
steps 11 and 12 of the processing order — were reduced to one each. **Nothing in the shipped tables
was changed to make a prediction come true.**

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are cited, not reproduced.

- **The *Deckungsrückstellung*.** § 341f HGB requires it prospectively on the tariff bases
  [R12] [REG-R54]; the DeckRV fixes the *Höchstrechnungszins* those bases may use — 1,00 % for new
  business from 1 January 2025, and whatever rate the cohort was written on, for the whole term
  [REG-R14] [REG-R15] — and caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme* [REG-R16]. Here
  the reserve rises for roughly thirty-five years, peaks where the incidence curve crosses the level
  premium, and runs off: an ageing reserve in economic function and a *Deckungsrückstellung* in law.
  **The model does not compute it**, and the *Rückkaufswert* enters as contractual data rather than
  as a derived reserve — which is what keeps `check_prem_equiv_resid(t)` a closure residual rather
  than a reserve in disguise.
- **The *Zinszusatzreserve*.** An HGB reserve with no counterpart elsewhere in this repository,
  driven by the ten-year *Referenzzins* of § 5 Abs. 3 DeckRV under the *Korridormethode* [REG-R17].
  A long-dated, interest-sensitive contract is exactly what attracts it. Not computed here.
- **The § 169 VVG floor.** A model carrying a zillmerised reserve applies **two** rules separately —
  what the DeckRV lets the insurer reserve, and what § 169 makes it pay with acquisition costs spread
  over at least five years — the tighter binding [REG-R16] [REG-R28]. `surrender_table.csv` encodes
  the *result* of both. Whether a pure-risk *Pflegerente* is inside § 169 at all is open (gap 9).
- **Solvency II best estimate.** Probability-weighted future cash flows discounted at the relevant
  risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R6], reaching German life
  business through the VAG rather than directly: `BEL = Σ_t v(t) × liability_cf(t)`. **No
  cost-of-capital rate, contract-boundary rule or standard-formula shock in this library was read
  from a retrieved instrument.**
- **The contract boundary, easier here than on a *Pflegetagegeld*.** The premium is level and
  guaranteed, adjustable only on the narrow § 163 route [REG-R27], so the insurer has no unilateral
  right to reprice the individual contract — the usual trigger for a boundary at the next repricing
  date. The whole projected stream is therefore inside the boundary on the natural reading; a
  *Pflegetagegeld* under § 203 VVG is the opposite case [R14] — MB/EPV § 8b recalculates every
  premium in an observation unit on a breach [S2]. The boundary point itself is still [unverified];
  no Solvency II instrument was retrieved for this product.
- **Surplus, IFRS 17 and professional standards.** The *Risikoergebnis* — the release of the
  first-order margins as experience emerges — is the dominant surplus source here [REG-R47],
  distributed under the MindZV and the RfBV [REG-R10] [REG-R18] [REG-R19]; the model produces the
  best-estimate leg and the `tar_*` engine the first-order leg, and neither becomes a declared rate.
  IFRS 17 fulfilment cash flows plus a CSM [REG-R55] are fed by the same engine, with grouping, CSM
  and risk adjustment out of scope. The DAV's *Fachgrundsätze* bind the responsible actuary who
  signs the bases [REG-R11] [REG-R56].

---

## Key sensitivities and model risks

In rough order of leverage for a German *Pflegerente* block.

1. **Duration in care — the in-care mortality multiples.** The direct multiplier on the liability and
   still the weakest-evidenced quantity in the model (gap 19); the research file's own arithmetic
   shows a mean spell moving from four years to five changing the premium by about a quarter. The
   shipped multiples are **[std]** order-of-magnitude reasoning, and they carry the product. **The
   overall spell is now sourced** — about five years where care begins after 60, 4,0 for men and 5,7
   for women [S14] — which puts the model's implied three-to-five years at the low end for women and
   makes this sensitivity, if anything, sharper. **The per-grade sojourn times are not sourced and
   apparently cannot be**, the *Pflegegrade* dating only from 2017.
2. **Incidence level and slope.** The slope is anchored to prevalence doubling every five years above
   75 and compounds over sixty-five years, so it is the more dangerous of the two: ±0.01 on `g` moves
   incidence at 90 by about a third. **The anchor is now measured and is softer than assumed**: the
   observed five-year prevalence ratios are 1,80 · 1,88 · 1,74 · 1,49 · 1,18 from 70–75 upward,
   about `ln 1.8 / 5 = 0.117` against the shipped 0.1386 [R18]. Shipped unchanged, reported here.
3. **The *Pflegegrad* definitional break.** DAV 2008 P was built on the *Pflegestufen*, the BGH has
   held that no inference runs from a *Pflegegrad* back to a *Pflegestufe* [REG-R36] [REG-R51], and
   the 2017 reform widened the insured population [R9]. **This is still the largest basis risk in the
   product**, it is not a parameter, and no sensitivity here captures it — but it is now a risk with
   a published response: the DAV's re-derivation of the bases for *Pflegegrade*, on a *Stufenmodell*
   rather than a per-grade chain, and from *Pflegestufen* data rather than observations [R15].
4. **The *Rechnungszins*.** Benefits fall on average some thirty-five years after issue, so this is
   the **most interest-sensitive product in delib**. It is also the one pricing assumption that is
   genuinely cited [REG-R14] [REG-R15].
5. **The middle steps of the *Leistungsstaffel*.** The time-weighted average benefit over a spell is
   about half the top step, so two tariffs with the same 100 % top step differ by more than the
   headline suggests. Compare model point 1 with model point 5.
6. **Lapse and the *Stornoabzug*.** Nothing supports any lapse level (gap 20). Here lapse is
   *profitable* — an early lapser paid for years and never reached the risk period — so the usual
   protection intuition is inverted, and the pricing basis deliberately excludes it. **The
   *Stornoabzug* is a separate and newly quantified risk**: the model ships 0 % with a 5 % model
   point, while the one *Pflegerenten* wording retrieved agrees **25 %**, rising to 50 % after a
   partial withdrawal, justified as compensating the change in the residual book's risk profile
   [S4] [REG-R28]. On a lapse-heavy block the difference between 0 % and 25 % is a first-order
   effect on surrender outgo, and it is **not** implemented here.
7. **The unisex mix.** Pricing blends 50 / 50 while the projection runs on the point's own sex; a
   book written 60 / 40 female against a 50 / 50 price is under-priced by the whole mismatch, and the
   mix is endogenous to the price [REG-R34].
8. **Expense levels and the *Zillmerung* base.** Every level is **[std]** (gap 2). At 500 € a month
   on point 14 the per-policy expense line, not the biometrics, decides whether the cell is viable.
9. **No select mortality after onset.** Mortality is highest immediately after onset, especially at
   grades 4 and 5 [unverified]; the model uses an aggregate. **The model therefore understates how
   much a *Karenzzeit* removes**, so point 7's reduction is a floor rather than an estimate.
10. **The terminal age and the payment convention.** `omega_age = 110` with `q = 1` forced in the
    last year of age, and annuity and premium both in advance — declared conventions rather than
    facts. Moving the annuity to arrears would shift the benefit stream a month and break the
    waiver's alignment with it.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R11]: #delib-pflegerentenversicherung-r11
[R12]: #delib-pflegerentenversicherung-r12
[R13]: #delib-pflegerentenversicherung-r13
[R14]: #delib-pflegerentenversicherung-r14
[R15]: #delib-pflegerentenversicherung-r15
[R16]: #delib-pflegerentenversicherung-r16
[R18]: #delib-pflegerentenversicherung-r18
[R2]: #delib-pflegerentenversicherung-r2
[R23]: #delib-pflegerentenversicherung-r23
[R6]: #delib-pflegerentenversicherung-r6
[R8]: #delib-pflegerentenversicherung-r8
[R9]: #delib-pflegerentenversicherung-r9
[REG-R1]: #delib-reg-r1
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
[REG-R24]: #delib-reg-r24
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R29]: #delib-reg-r29
[REG-R34]: #delib-reg-r34
[REG-R36]: #delib-reg-r36
[REG-R41]: #delib-reg-r41
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R51]: #delib-reg-r51
[REG-R52]: #delib-reg-r52
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R8]: #delib-reg-r8
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
