# Technical Notes

**Status:** Draft, 2026-08-29 (sources assembled); citations re-verified against the primary
documents 2026-08-30.

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Index_DE_S`**, **monthly** grid — for the standardized composite German *Indexpolice* defined in
`product-spec.md` (same directory). This is not any single insurer's contract. [S#]/[R#] tags refer to
the source list in `sources.md` (numbering carried from `_research/indexpolice.md`; frozen); [REG-R#]
tags refer to the cross-product reference library `references/regulatory-and-actuarial-references.md`
(its own frozen numbering). **[std]** marks standardizations introduced for the reference
implementation; [unverified] marks claims that no retrieved document corroborates. Parameter values are
identical to those in `product-spec.md`. Cells names, model-point columns and CSV headers are English
`lower_snake_case`; German terms of art keep their German form in prose.

**The retrieval conditions govern these notes as they govern the specification.** They were drafted
with direct HTTP egress blocked and the session's search budget exhausted, from the authoring model's
own knowledge of German practice; the citations have since been re-verified against the primary
documents, and **32 of the 38 entries in `sources.md` now read `Retrieved: yes`**. Cap and quota
levels, charge levels and parts of the commercial envelope are now established **for individual
carriers but not for the market**, and no shipped level has been changed on the strength of one, so
class (b) and class (c) below remain **[std] throughout** — three of them now known to sit off the
retrieved evidence, as `model.md` records — while class (a) is cited to statutes read as canonical
XML and, for the index clauses, to two AVB read in full [S2] [S7]. What the model reproduces exactly
is the **mechanics**, and the two constructed *Indexjahre* of the research file are wired into the
shipped index path so that the mechanics are asserted against them cell by cell.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — premiums in; death,
  surrender and *Rentenbeginn* benefits out; insurer expenses — for a single-policy model point on an
  expected (probability-weighted) basis, together with the two state variables that make this product
  what it is: the *Deckungskapital* and the *Höchststandsicherung* ledger of locked-in credits.
- **Out of scope, and said so.** Discounting; the *Deckungsrückstellung* and the *Zinszusatzreserve*
  [REG-R14] [REG-R17]; Solvency II technical provisions, risk margin and SCR [REG-R1] [REG-R2]; the RfB
  and the MindZV minimum-allocation arithmetic itself [REG-R18] (the model consumes a **declared** rate,
  it does not derive one); the *Schlussüberschussanteil* and the *Bewertungsreserven* share [REG-R9]
  [REG-R24]; the *Rentenphase*, which is `products/sofortrente/`; *Beitragsfreistellung* as a decrement;
  *Dynamik*; and tax of any kind.
- **The accumulation phase only.** The projection runs from inception (or from the valuation date for an
  in-force point) to *Rentenbeginn*, where the capital falls due as a single terminal amount. Whether it
  is taken as a *Kapitalabfindung* or converted at the *Rentenfaktor* changes **what is reported**, not
  the terminal cash flow: either way the capital leaves the accumulation contract at the end of the
  last policy year, `k = proj_len_y() − 1`, in the frame's last month.
- **Projection frequency: monthly, over a contract whose own clock is annual.** The *Indexjahr* is
  twelve months, the surplus is declared once a year, the *Wahlrecht* is exercised once a year and the
  credit is struck once a year — so **every one of those constructions keeps the policy year as its
  argument**, and the model runs on two clocks. What the monthly step is *for* is the *Indexjahr*
  itself: its twelve monthly observations were always the mechanic, and on the annual grid they lived
  inside a single cells, read from a wide external table and invisible from the frame.
  `index_month(t)`, `index_return_mth(t)` and `index_return_capped_mth(t)` now put them on the frame,
  one row each, so *capped above and not floored below* can be read month by month. The grid also
  dates the forfeiture — a surrender in month 7 of an *Indexjahr* loses that year's credit — where the
  annual grid silently gave every exit the favourable year-end date. What it does **not** change is
  the settlement: the credit is struck at the year end and nowhere inside it, because that is the
  contract. (`FRV_DE_S` is monthly for a different reason again: a unit account genuinely *is* priced
  monthly, and its charge cliff falls at month 61.)
- **The frame is 0-based and `t` counts policy months from issue.** `duration(t) = t // 12` is the
  **0-based policy year** `k`, and every annual construction in this file takes it; the contractual
  **policy year is the 1-based label `k + 1`** and is derived, never indexed by. The attained age
  steps on the **anniversary**, `age(t) = entry_age + duration(t)`, and `is_anniv(t)` is
  `t % 12 == 11`, the month the annual machinery acts in. A **new-business** point starts at `t = 0`;
  an **in-force** point starts at `t_start() = 12 × dur_init`, `dur_init` being a 0-based count of
  completed policy **years**, so the conversion is a multiplication and no model point column
  changed; `k_start() = dur_init` is the same instant on the annual clock. `result_cf()` is indexed
  `t_start() … proj_len() − 1`, contiguous, and its first `pols_if` value is `pols_if_init()`.
- **`proj_len()` is the exclusive end of the frame in months**, `proj_len() = 12 × proj_len_y()` with
  `proj_len_y() = ann_start_age − entry_age` the number of policy years, so
  `result_cf().index[-1] == proj_len() − 1` — the library's reading of `proj_len()` and lifelib's own
  `for t in range(proj_len())`, asserted in the conventions suite. It is **not** the row count of an
  in-force point: one at `dur_init = 8` publishes `324 − 96 = 228` rows and still reports
  `proj_len_y() = 27`.
- **Two speeds on each decrement.** `mort_rate(t)` and `lapse_rate(t)` return the **annual** rate of
  the policy year `t` falls in — the vectors tabulated below, flat across the year's twelve months —
  and `mort_rate_mth(t)` and `lapse_rate_mth(t)`, each `1 − (1 − r)^(1/12)`, are what the recursion
  applies. The twelfth is **geometric and never `r / 12`**, so twelve compound back to the year's rate
  exactly and `pols_if` at every anniversary is what the annual grid gave — and with it the account,
  every *Indexgutschrift*, the *Höchststandsicherung* ledger and the guaranteed capital.
- **The *Indexjahr* is aligned with the policy year [std].** The contractual *Indexstichtag* need not
  fall on the policy anniversary, and no carrier's convention was established. The model has no other
  defensible alignment, and the misalignment would change the calibration of the Cap rather than the
  mechanic. `index_month(t) = t % 12 + 1` is the alignment stated as arithmetic.
- **Timing conventions [std].** The premium at the **start of the policy year** — annual in advance,
  which is what § 12 Abs. 1 VVG makes the *Versicherungsperiode* for this tariff, so `prem_due(t)` is
  true in the first month of each policy year and nowhere else; the premium charges deducted as the
  premium is credited; the reserve charge and the guaranteed interest struck on the post-premium
  balance, once a year; the insurer's acquisition expense in the frame's first month and a twelfth of
  the year's maintenance each month, on the opening in-force of that month; decrements and benefits at
  the **end of each month**; the *Indexjahr* credit at the **end of the policy year**, to the
  **survivors of all twelve months only**.
- **What a mid-year exit is paid.** The policy year's own amount: a death in any month of policy year
  `k` is paid `db_pp(k)` and a surrender `cv_pp(k)`, both struck on `av_pp_at(k, "AFT_GUAR")` — the
  account **before** that year's credits, because the payoff exists only at the *Indexjahr* end. The
  account of this tariff is defined at anniversaries and nowhere between them, so the monthly grid
  moves **when** the claim falls and **how many policies are exposed** to it, not what it is worth.
- **Age basis** age last birthday **[std]**, the basis the delib registry fixes for the whole library.
  **Currency** EUR. **Sign**: `net_cf(t)` is **income-positive** (premiums +, benefits and expenses −),
  with the outgo-positive orientation published as `liability_cf(t) = −net_cf(t)`. **Rounding**: full
  precision internally, displayed money to the cent and `pols_if` to six decimals **[std]**.
- **Unisex pricing, sex-distinct best-estimate mortality.** Sex may not be a rating factor [REG-R34], and
  it is not: no premium, charge or benefit in this model depends on `sex`. It selects the
  best-estimate mortality row only, and mortality here is a **timing** assumption — the death benefit is
  the account value with a floor, not a sum insured — so the choice moves the result very little.

### Model inputs — the external CSVs

Inputs are **external files in the model folder's parent**, read once per model in the unparameterized
`Data` Space (the `annuallife/TradLife_A` layout). **Every file but `model_point_table.csv` carries a
final `provenance` column**, one tag per row — delib's second ruling, asserted by the conventions suite.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the 22 model-point attributes below (exempt from `provenance`) |
| `index_return_table.csv` | `index_id`, `t` | `m01` … `m12` — the twelve monthly index returns of *Indexjahr* `t`, as decimals; `provenance` |
| `index_param_table.csv` | `index_id`, `t` | `cap` (monthly Cap `C`), `quote` (*Partizipationsquote* `q`); `provenance` |
| `surplus_rate_table.csv` | `t` | `surplus_rate` (the declared *Überschussanteilsatz* `b`, = the option budget); `provenance` |
| `election_table.csv` | `elect_id`, `t` | `w` — the fraction of the year's surplus directed to the index arm; `provenance` |
| `mort_table.csv` | `sex`, `age` | `qx`; `provenance` |
| `lapse_table.csv` | `t` | `lapse_rate` (the base rate before the terminal-year override); `provenance` |
| `freq_load_table.csv` | `prem_freq` | `freq_load` (the *Ratenzahlungszuschlag* multiplier); `provenance` |

Three index paths are shipped, all **[std]**, and their construction is stated so that a reader can
rebuild them exactly rather than take them on trust:

- **`eqidx_vol17`** — the broad **equity price index** case. Monthly returns drawn from
  `numpy.random.default_rng(20260829).normal(0.0060, 0.0500, size=(40, 12))`, rounded to four decimal
  places: monthly mean 0,60 % and monthly standard deviation 5,00 %, i.e. an arithmetic 7,2 % a year at
  an annualised 17,3 % — the research file's own volatility assumption and a plausible level for a broad
  European equity index. The **17,3 %** figure stays [unverified] — no index rulebook or realised-
  volatility series was retrieved for the EURO STOXX 50 or any other underlying — but the index itself
  is now a named one at a retrieved carrier [S2]. **Rows `k = 8` and `k = 9` — policy years 9 and 10 —
  are then overwritten** with the research file's constructed Example A and Example B (below), so that
  the two examples the whole mechanic turns on are reproduced by the model rather than restated in
  prose.
- **`houseidx_vol5`** — the **volatility-targeted house multi-asset index** case, from
  `numpy.random.default_rng(20260830).normal(0.0025, 0.0144, size=(40, 12))`, rounded to four decimal
  places: 0,25 % a month at an annualised 5,0 %, the volatility target the research file records for
  this design generation. The **5 % target stays [unverified], and now for a stated reason**: two German
  house multi-asset indices are named in retrieved carrier documents — R+V's *Solactive Multi Anlage
  Stabil Index* (SOMAS) and the *Stuttgarter M-A-X Multi-Asset Index* [S7] [S8] — and **neither
  publishes a volatility target or an index-level fee** on the pages that describe it. The path carries
  a 6,00 % monthly Cap and a 100 % *Partizipationsquote*, because a low-volatility underlying is cheap
  to buy options on and that is the design's selling point; note that the one **published** house-index
  quota is Stuttgarter's **70 %** [S8], so 100 % is generous against the single observation available.
- **`zero_path`** — every monthly return exactly zero, for every year. It is not a scenario; it is an
  **instrument**: it isolates the guaranteed accumulation, makes every *Indexjahr* credit exactly
  0,00 €, and lets the *Beitragsgarantie* floor at *Rentenbeginn* be tested where it actually binds.

**Example A (`k = 8`, policy year 9)**, monthly returns in per cent:
1,80 / −2,40 / 4,60 / 0,90 / −3,70 / 2,20 / 3,40 / −1,10 / 0,40 / 5,20 / −0,80 / 2,60.
**Example B (`k = 9`, policy year 10)**:
6,50 / −2,10 / 5,80 / −1,90 / −2,40 / 4,20 / −3,10 / 0,60 / −2,80 / 5,10 / −1,70 / −1,20.

---

## Model point attributes

Twenty-two columns. The last column of the table says which model points exercise the attribute away
from its base value, so that no column is carried without being tested.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | key; **model point 1 is the worked example's anchor cell** | all |
| `policy_id` | str | label, `DE-IDX-nnnn`; reporting only | all |
| `sex` | enum {M, F} | selects the best-estimate mortality row; **never a rating factor** [REG-R34] | 3, 5, 7, 10, 12 |
| `entry_age` | int | age last birthday at inception; `age(t) = entry_age + t` | 3–13 |
| `dur_init` | int | completed policy years at the valuation date; 0 = new business; the frame starts at `t_start() = 12 × dur_init`, `dur_init` already being a 0-based elapsed count of policy **years** | 8, 13 |
| `pols_if_init` | float | policies represented at `t_start()` | — (1.0 everywhere) |
| `ann_start_age` | int | attained age at *Rentenbeginn*; `proj_len() = ann_start_age − entry_age` | 6 |
| `prem_form` | enum {level, single} | *laufender Beitrag* or *Einmalbeitrag* | 7 |
| `prem_gross_pp` | EUR | the **annual-mode** premium (the *Jahresbeitrag*), or the single premium | 5, 6, 7, 8, 12, 13 |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | payment frequency; drives `freq_load()` | 4, 5, 6 |
| `prem_term_y` | int | *Beitragszahlungsdauer* in policy years, ≤ `proj_len()` | 6, 7, 9, 13 |
| `av_pp_init` | EUR | *Deckungskapital* per policy at the valuation date; 0 for new business | 8, 13 |
| `guar_locked_init` | EUR | the *Höchststandsicherung* ledger already accumulated — credits made before the valuation date | 8, 13 |
| `prem_paid_init` | EUR | premiums already paid, on the annual-mode basis; the base of the *Beitragsgarantie* so far | 8, 13 |
| `guar_level` | float | *Garantieniveau*: the *Beitragsgarantie* as a fraction of the *Beitragssumme* | 6, 9, 12 |
| `guar_rate` | float | the contract's *Rechnungszins*; a **cohort** fact, not today's rate [REG-R15] | 8, 13 |
| `payoff_form` | enum {cap, quote} | Cap design or *Partizipationsquote* | 2, 3 |
| `index_id` | str | key into `index_return_table.csv` **and** `index_param_table.csv` | 3, 9 |
| `elect_id` | str | key into `election_table.csv`: the *Wahlrecht* path `w(t)` | 10, 11, 12 |
| `death_min_rate` | float | *Mindesttodesfallschutz* floor on the death benefit, as a fraction of the *Beitragssumme* [REG-R45] | 13 |
| `ann_option` | enum {annuity, cash} | whether the terminal capital is reported as an annuity or as a *Kapitalabfindung* | 7 |
| `surr_charge_on` | int {0, 1} | whether the contractual *Stornoabzug* applies | 13 |

**The thirteen model points.** Between them they cover both premium forms, all four payment
frequencies, both payoff designs, all three index paths, all four election paths, both
*Kapitalwahlrecht* elections, both death-benefit forms, both *Stornoabzug* settings, two in-force
points, four *Rechnungszins* cohorts and four *Garantieniveaus*.

| # | Configuration, in one line |
|---|---|
| 1 | **Anchor.** M 40 → 67, 2 400,00 € a year annually for 27 years, Cap on `eqidx_vol17`, index arm every year, 90 % guarantee at 1,00 % |
| 2 | Anchor with `payoff_form = quote` — the *Partizipationsquote* on the **identical** index path, so the two designs are directly comparable |
| 3 | F 40 → 67, `houseidx_vol5` with `payoff_form = quote` — the volatility-targeted house-index case at a 100 % participation rate |
| 4 | M 35 → 67, **monthly** premiums (32 years) — the *Ratenzahlungszuschlag* at 5 % |
| 5 | F 45 → 67, **quarterly** premiums of 3 600,00 € a year (22 years) |
| 6 | M 50 → **65**, **half-yearly** premiums of 6 000,00 € a year, 80 % guarantee (15 years) |
| 7 | F 55 → 67, ***Einmalbeitrag*** of 50 000,00 €, `ann_option = cash` — a 12-year term, which is also the § 20 Abs. 1 Nr. 6 EStG boundary [REG-R45] |
| 8 | **In-force.** M 40 → 67 at `dur_init = 8`, `av_pp_init = 50 000,00 €`, 6 000,00 € a year, 0,90 % cohort rate — **its frame opens at `t = 96`, policy year `k = 8`, and that is its first projected *Indexjahr*, so it reproduces the research file's Examples A and B to the euro** |
| 9 | **Boundary — the guarantee binds.** M 55 → 67, 100 % *Beitragsgarantie*, `zero_path`: every credit is 0,00 € and the terminal capital falls **below** the guarantee |
| 10 | F 40 → 67, `elect_id = switch_at_15` — index arm to policy year 15 (`t ≤ 14`), safe arm thereafter |
| 11 | M 40 → 67, `elect_id = always_safe` — the *sichere Verzinsung* comparator, which reduces the contract to a *klassische Rentenversicherung* |
| 12 | F 30 → 67 (**37 years**, the longest), 1 800,00 € a year, 60 % guarantee, `elect_id = half_half` — a partial election |
| 13 | **In-force, boundary.** M 45 → 67 at `dur_init = 4`, `prem_term_y = 12` so premiums stop after policy year 12 (`k = 11`), `guar_rate = 0,25 %` **equal to the reserve charge**, `death_min_rate = 0`, `surr_charge_on = 0` |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len_y()`, `proj_len()` | the number of projected policy years; `12 ×` that, the frame's exclusive end in months | once per model point |
| `k_start()`, `t_start()` | the first projected policy year, `dur_init`; the first projected month, `12 × dur_init` | once per model point |
| `duration(t)`, `policy_year(t)`, `is_anniv(t)`, `index_month(t)` | the bridge between the clocks: the 0-based policy year of month `t`, its 1-based label, whether `t` is the year's last month, and which month of the *Indexjahr* it is | derived |
| `age(t)` | attained age in month `t` = `entry_age + duration(t)`; **steps on the anniversary** | annual step |
| `pols_if(t)` | policies in force at time `t`, the **start of month** `t`; `pols_if(t_start()) = pols_if_init()` | monthly recursion |
| `pols_if_at(t, timing)` | the within-month points of the same count: `"BEF_DECR"`, `"AFT_DEATH"`, `"AFT_LAPSE"` | within month `t` |
| `pols_surv_year_end(k)` | the survivors of all twelve months of policy year `k` — the population the *Indexjahr* credit is given to | once a policy year |
| `av_pp(k)` | *Deckungskapital* per policy at time `k`, the **start** of policy year `k`; `av_pp(k_start()) = av_pp_init` | annual recursion |
| `av_pp_at(k, timing)` | `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_CHARGE"`, `"AFT_GUAR"`, `"AFT_CREDIT"` | within policy year `k` |
| `av_at(k, timing)`, `av(k)` | the same balances at fund level, `× pols_if(12k)` | within policy year `k` |
| `prem_paid_pp(k)` | cumulative annual-mode premiums paid to time `k`, including `prem_paid_init` | annual, non-decreasing |
| `credit_cum_pp(k)` | the ***Höchststandsicherung*** ledger: every index and safe-arm credit made, cumulated | annual, non-decreasing |
| `guar_floor_pp(k)` | the *Beitragsgarantie*, `guar_level × prem_paid_pp(k)` | annual, non-decreasing |
| `guar_cap_pp(k)` | the guaranteed capital, `guar_floor_pp(k) + credit_cum_pp(k)` | annual, non-decreasing |
| `av_min_pp(k)`, `av_min_pp_at(k, timing)` | the shadow *Deckungskapital* on a **five-year** acquisition-cost spread, with the same within-year timings — the § 169 Abs. 3 floor [REG-R28] | annual recursion |
| `index_base_pp(k)` | `G(k)`, the participating capital of the *Indexjahr* of policy year `k` = `av_pp(k)`, **before** that year's premium | annual |

There is **no unit account, no unit price and no fund value** anywhere in this model, and that is a
product fact rather than a simplification: the capital is in the *Sicherungsvermögen* [REG-R7] and the
policyholder's claim is measured in euros. There is likewise **no paid-up sub-population**: German lapse
is a three-way decrement [REG-R28] and the reference implementation models surrender only (below).

---

## Assumption inputs

Three classes are distinguished. **(a)** is contractual or statutory and is cited; **(b)** is the
insurer's current discretionary scale, redetermined annually; **(c)** is the modeller's view of
experience. On this product classes (b) and (c) carry almost the whole result, and **every entry in
both is [std]** — not because retrieval established nothing, but because no shipped level was
changed on the strength of what it established; `model.md` records each comparison.

### (a) Contractual / guaranteed elements (cited)

| Input | Value / rule | Basis |
|---|---|---|
| Guaranteed rate `i_g` | `guar_rate`, a model-point column; **1,00 %** for a contract written in 2025–2026, 0,90 % for a 2017–2021 cohort, 0,25 % for 2022–2024 | [R7] [R18] [REG-R14] [REG-R15] |
| Payoff, Cap form | `max( Σ_{m=1..12} min(r(t,m), C(t)), 0 )` — capped above, **not floored below**, summed **not compounded**, the floor on the year | mechanic firm [S2] [S5]; levels **[std]** |
| Payoff, *Quote* form | `max( q(t) × (Π_m (1 + r(t,m)) − 1), 0 )` | mechanic firm; level **[std]** |
| Base of the participation | `G(t) = av_pp(k)`, the capital at the start of the *Indexjahr*, **before** that year's premium | **confirmed by clause** — [S2] Ziffer 3.3 Absatz 2 e), [S7] § 3 Ziffer 2; spec footnote 14 |
| *Höchststandsicherung* | a credit, once made, is permanently added to the guaranteed capital and enters `G` of every later year | mechanic firm |
| Guarantee at *Rentenbeginn* | `max( av_pp(n), guar_level × prem_sum_paid + credit_cum_pp(n) )`, the time-`n` values; **not** an annual guaranteed rate on the reserve | [R11] [R12]; composition **[std]** |
| Death benefit | `max( av_pp_at(k,"AFT_GUAR"), death_min_rate × prem_sum() )` — the account **excluding the running *Indexjahr***, floored at 50 % of the *Beitragssumme* | shape [S7] § 1 Ziffer 5 (*Policenwert*, min. 90 % of premiums), **not** [S9], whose default is no death benefit at all; floor **[std]** [R14] [REG-R45] |
| Surrender value | `max( av_pp_at(k,"AFT_GUAR"), av_min_pp(k) ) × (1 − storno_rate × surr_charge_on)` | [R2] [REG-R28]; level **[std]** |
| § 169 Abs. 3 floor | the *Deckungskapital* with acquisition costs spread evenly over the **first five contract years** | [R2] [REG-R28] |
| *Höchstzillmersatz* | acquisition charge capped at **25 ‰** — "Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten", DeckRV § 4 Abs. 1 | [R7] [REG-R16] |
| No credit in the year of exit | death, surrender and (for the year's decrements) the terminal year forfeit the running *Indexjahr* | **confirmed by clause** — [S2] Ziffer 3.3 and 9.2, [S7] § 3 Ziffer 5; spec footnote 18 |
| *Ratenzahlungszuschlag* | annual 1,000; half-yearly 1,020; quarterly 1,030; monthly 1,050 | **[std]** |
| *Rentenfaktor* | `max(rentenfaktor_guar, rentenfaktor_curr)`, **25,00 €** per 10 000 € per month | chassis fact; level **[std]** |
| *Selbsttötung* | three-year exclusion; **not modeled** — the death benefit is a return of capital, so it is close to inoperative | [R6] [REG-R26] |

### (b) Insurer-discretionary current elements (snapshot; redetermined annually)

| Input | Value | Basis |
|---|---|---|
| Declared surplus rate `b` = the option budget | **2,50 %** a year of `G`, level over the projection | **[std]** (1) |
| Monthly Cap `C` | **3,00 %** on `eqidx_vol17` and `zero_path`; **6,00 %** on `houseidx_vol5` | **[std]** (2) |
| *Partizipationsquote* `q` | **60 %** on `eqidx_vol17` and `zero_path`; **100 %** on `houseidx_vol5` | **[std]** (2) |
| *Mindest-Cap*, minimum budget | **none** — neither appears in either retrieved AVB, and both instead exclude the participation for a year in which the guarantee binds | [S2] Ziffer 3.5, [S7] § 2 Ziffer 1; spec footnote 17 |
| Current *Rentenfaktor* | **25,00 €**, equal to the guaranteed factor in the base run | **[std]** (3) |
| *Stornoabzug* | **2 %** of the base surrender value | **[std]**, spec footnote 27 |
| Cap announced before the election deadline | **yes** — parameters notified at least 3 weeks before the *Indexstichtag*, election due 7 days before | [S2] Ziffer 3.1; spec footnote 16 |

1. The declared rate **is** the option budget [R8] [REG-R18]. **It sits below the 2026 evidence**:
   Assekurata's survey puts the index-segment average at **3,07 %** and classic private annuities at
   2,62 % [R20] [REG-R53], and Stuttgarter publishes 2,16 % for its own safe arm [S8]. The value is a
   shipped input and is not changed in a provenance pass; the effect is a proportional understatement
   of every index credit. The retrieved AVB also define the budget more widely than the model does —
   the declared surplus **plus** the year's minimum share of the *Bewertungsreserven*, and at Allianz
   net of *Verwaltungskosten* ([S2] Ziffer 3.3 Absatz 1, [S7] § 3 Ziffer 9) — so `opt_budget_pp` is a
   lower bound on the contractual budget in two independent ways. **Holding it
   level is the strongest simplification in this file.** In reality the rate moves with the investment
   result and with the *Zinszusatzreserve* releases behind it [REG-R17]; and the feedback from the
   *Garantieniveau* through the asset mix to the declared rate — the whole design logic of *Neue
   Klassik* — is **not modeled at all**, so model point 9's 100 % guarantee credits the same declared
   rate as the anchor's 90 %, which a real insurer would not do.
2. **One carrier-published cap level is now on record — Allianz's illustrative 3,2 % [S5] — but no
   market panel is** [R21]. The Cap and the budget are **not independent parameters**, and the AVB says
   so: it is set annually on quotes from several financial institutions, given the surplus, the
   *Bewertungsreserven* *Sockelbetrag*, volatility and the index's dividend yield [S2] Ziffer 3.3
   Absatz 2 b). Concretely: the Cap is the level at which the option strip costs the budget. The
   research file's own arithmetic, at monthly `μ = 0,60 %` and `σ = 5,00 %`, gives an expected annual
   credit of about **2,97 %** against a 2,50 % budget with a **65 %** probability of a zero year; under
   a risk-neutral drift on a price index it prices the same strip at about **1,7 % of `G`**, *below*
   the 2,50 % budget — so the shipped pair (3,00 %, 2,50 %) is **not mutually consistent**, and at that
   volatility a 2,50 % budget would buy a cap somewhat **above** 3,00 %. The model therefore publishes a
   diagnostic, `index_budget_ratio()` = total index credits ÷ total option budget over the projection,
   and the worked example reports it. **A value far from 1 means the pair is off**, and the sensitivity
   section says which way.
3. Setting the two factors equal keeps the max-of-two rule exercised by a test rather than by the base
   path, so a reader can see that the rule is implemented without the base run depending on it.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German insurer publishes a mortality basis, a lapse rate, an
expense loading or an election distribution for this product, and no index-specific *Stornoquote* exists
at all.

**Mortality.** The market-standard bases are proprietary: **DAV 2008 T** for death cover and **DAV
2004 R**, a *Generationentafel* in attained age **and calendar year**, for every annuity promise
[REG-R48] [REG-R49]. They are the Deutsche Aktuarvereinigung's property, **are not public and are not
redistributed here**. The shipped `mort_table.csv` is a **[std] Gompertz-form proxy**:

    qx(M, x) = 0.001200 × 1.095^(x − 40),    qx(F, x) = 0.65 × qx(M, x),    ages 20 … 100

**The anchor a substitute table must preserve is `qx(M, 40) = 0.001200` exactly**, so the worked example
still closes. Two properties of the real bases the proxy deliberately does **not** have, and a user
replacing it should know which: it is a **period** table, not a generational one, so it understates a
long-deferred annuitisation [REG-R49]; and it carries no selection effect. Neither matters much here,
because **mortality in this model is a timing assumption, not an amount assumption** — the death benefit
is the account value with a floor — but both matter greatly to the *Rentenfaktor* the terminal capital
buys, which is why the *Rentenfaktor* is a **[std]** input rather than a computed one.

**Lapse.** The GDV publishes one market-wide *Stornoquote* by count for all *Hauptversicherungen*
together — **2,56 % in 2023, 2,51 % in 2022** — with **no product split, no duration split and no index
line at all** [R19], so the two irreconcilable market-wide figures this note previously weighed against
each other are not the published series; the published series is a single number that cannot be
disaggregated. **No index-specific rate exists**, and none is derivable: the tag stays because the only
retrievable statistic is aggregated past the level the model needs. BaFin adds a supervisory
observation but no figure — some products stand out with "sehr hohen Stornoquoten … speziell in den
ersten Jahren nach Vertragsabschluss", which is a comment on the shape delib models rather than a
calibration of it [R17]. The research file's own **[std]** is a level 3 % a year. delib refines that
to a duration shape, because a shape flat in duration ignores the strongest single driver of German
surrender behaviour — the **duration-12 and age-62 double threshold** of § 20 Abs. 1 Nr. 6 EStG, at
which only half the *Unterschiedsbetrag* becomes taxable and at the personal rate rather than by final
withholding [R14] [REG-R45]:

| Policy year (`t + 1`) | 1–2 | 3–11 | **12** | 13 … n−1 | **n** |
|---|---|---|---|---|---|
| Index `t` | 0–1 | 2–10 | **11** | 12 … n−2 | **n−1** |
| `lapse_rate_base(t)` **[std]** | 5 % | 3 % | **6 %** | 2 % | 2 % |
| `lapse_rate(t)` applied | 5 % | 3 % | 6 % | 2 % | **0 %** |

`lapse_table.csv` is keyed on the model's own 0-based **policy year**, read through `duration(t)`, so its
first row is `k = 0` and the tax step sits at `k = 11`. The mean over the anchor's 27 years is about **2,6 %**, so the level stays inside the
research file's **[std]** while the shape carries the tax threshold. **In the final period the applied
rate is zero [std]**: the end of period `n − 1` is *Rentenbeginn*, so a lapse and a maturity are the
same event at the same instant, and the whole surviving cohort is booked as a maturity. Unlike frlib's term
product, where the two paid the same nothing, **here they pay different amounts** — the surrender value
carries the *Stornoabzug* and forfeits the running *Indexjahr*, the maturity value carries neither and
takes the guarantee floor — so this convention moves real money and is not merely a bookkeeping split.

**A behavioural incentive the annual grid quietly assumed away, and the monthly grid does not.** With
no credit in the year of exit, the product rewards surrendering just **after** an *Indexjahr* end and
penalises surrendering just before one. An annual grid put every exit at a year end and so implicitly
gave each the favourable date; here a surrender in month 7 of an *Indexjahr* is a row of the frame and
the eleven unfavourable months are as real in the projection as the twelfth. What is still **not**
modelled is a behavioural response to the incentive — the surrender rate is unconditional — and that
remains a stated model risk. The premise is a clause rather than an assumption: both retrieved AVB credit the participation only at the start of the following *Indexjahr*
and neither refunds the unspent budget on a mid-year exit ([S2] Ziffer 3.3 and 9.2, [S7] § 3 Ziffer 5).
Allianz's AVB also has an incentive of its own that delib does not model: the *Stornoabzug* falls away
in the last year of the *Aufschubdauer* and in the last seven where the insured is at least 55 and the
contract at least ten years old, which pushes surrender towards the end of the term rather than towards
an *Indexjahr* boundary.

**The *Wahlrecht* election path is the behavioural assumption unique to this product.** It is a
policyholder election, so it belongs in class (c) and not in class (b). Real policyholders in this
family are widely believed to be inert — to elect once and never revisit — which if true makes the
annual right far less valuable than its description suggests; **no election distribution is
established** [unverified], and none is published: the AVB prescribe the mechanism, not the take-up.
What the AVB do settle is the **default on inertia**, and it is not neutral. R+V's contract "nimmt
grundsätzlich an der Indexpartizipation teil" [S7] § 2 Ziffer 1, so silence keeps the policyholder in
the index arm. Allianz's default is a two-branch rule: the previous split rolls over if index
participation was at least 50 %, but a contract at 25 % or 0 % — or one for which the participation was
excluded — is moved **to 50 % index participation** on silence, with the split across indices taken from
what other IndexSelect policyholders with the same *Indexstichtag* most often chose [S2] Ziffer 3.2.
**delib's `w` paths are exogenous and model neither default**, which for a book-level projection is a
real simplification: an inert population does not stay where it was put. Four **[std]** paths are
shipped: `always_index` (`w = 1`, the base run, because a base run in the safe
arm would reduce the product to `RV_DE_S`), `always_safe` (`w = 0`), `half_half` (`w = 0,5`) and
`switch_at_15` (`w = 1` through policy year 15, i.e. `t ≤ 14`, then 0).

**Expenses (insurer outgo) and contractual charges (deductions from the account).** These are two
different things and the model keeps them apart: a charge reduces the policyholder's *Deckungskapital*,
an expense is the insurer's cash outgo in `net_cf`. All levels **[std]**.

| Input | Value | Note |
|---|---|---|
| Acquisition charge `acq_cost_rate` | 2,5 % of the *Beitragssumme*, spread over `zill_years = 5` premium-paying years | at the *Höchstzillmersatz* [REG-R16] |
| Acquisition expense `acq_expense_rate` | 2,5 % of the *Beitragssumme*, incurred **in full at inception** | the *Zillmer* strain: paid out at once, recovered over five years |
| Premium charge `β` (`exp_prem_rate`) | 3 % of each gross premium collected | *Verwaltungskosten* |
| Reserve charge `γ` (`exp_av_rate`) | 0,25 % a year of the post-premium balance | *Verwaltungskosten* |
| Maintenance expense | 36,00 € per policy a year, inflating at `exp_infl = 1,5 %` | *Stückkosten* |
| Claim expense | **none** — not modeled | no source, and immaterial beside the benefit |

The charge income (`β` plus `γ` plus the amortised acquisition charge) and the expense outgo are
deliberately of the same order, so the *Kostenüberschuss* is small. **The model does not close the
MindZV loop**: it does not compute a cost result, take 50 % of it and add it to the declared rate
[REG-R18]. The declared rate is exogenous, and a user who changes the expense assumptions changes
`net_cf` without changing the surplus the policyholder receives. That is a stated limitation, not an
oversight.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | the 0-based **month** index, `t = t₀ … 12n−1`; `t₀ = t_start() = 12·dur_init` |
| `k` | `duration(t)` | the 0-based **policy year**, `t // 12`; `k₀ = k_start() = dur_init`, `n = proj_len_y() = ann_start_age − entry_age`; the contractual policy year is `k + 1`. Every annual construction below takes `k` |
| `m(t)` | `index_month(t)` | which month of its *Indexjahr* `t` is, 1-based: `t % 12 + 1` |
| `x(t)` | `age(t)` | attained age in month `t` = `entry_age + duration(t)`, stepping on the anniversary |
| `l(t)` | `pols_if(t)` | policies in force at time `t`, the start of **month** `t`; `l(t₀) = pols_if_init()` |
| `φ` | `freq_load()` | the *Ratenzahlungszuschlag* multiplier |
| `P_b(k)`, `P(k)` | `prem_base_pp(k)`, `prem_gross_pp(k)` | the annual-mode premium due in policy year `k`; the amount actually collected, `P_b(k)·φ`, in the first month of that year |
| `BS` | `prem_sum()` | *Beitragssumme* = `Σ_k P_b(k)` over the whole contract, **on the annual-mode premium** |
| `α(k)`, `α₅(k)` | `prem_charge_acq_pp(k)`, `prem_charge_acq_min_pp(k)` | the acquisition charge on the tariff spread and on the five-year spread |
| `β·P(k)` | `prem_charge_adm_pp(k)` | the premium-based administration charge |
| `P⁺(k)` | `prem_to_av_pp(k)` | the premium credited to the account, `P(k) − α(k) − β·P(k)` |
| `A(k)` | `av_pp(k)` | *Deckungskapital* per policy at time `k`, the start of policy year `k` |
| `γ`, `F(k)` | `exp_av_rate`, `av_charge_pp(k)` | the reserve charge rate; the amount charged, `γ·(A(k) + P⁺(k))` |
| `i_g`, `I(k)` | `guar_rate`, `guar_int_pp(k)` | the guaranteed rate; the guaranteed interest, `i_g·av_pp_at(k,"AFT_CHARGE")` |
| `G(k)` | `index_base_pp(k)` | the participating capital of the *Indexjahr* of policy year `k` = `A(k)` |
| `b(k)`, `w(k)` | `surplus_rate(k)`, `elect_index(k)` | the declared surplus rate; the fraction of it directed to the index arm |
| `r(k,m)`, `C(k)`, `q(k)` | `index_return(k, m)`, `index_cap(k)`, `index_quote(k)` | the month's index return; the monthly Cap; the *Partizipationsquote* |
| `r(t)` | `index_return_mth(t)` | the same return read on the monthly frame, `r(duration(t), index_month(t))` |
| `min(r, C)` | `index_return_capped_mth(t)` | the month's capped return, on the frame |
| `S(k)` | `index_sum(k)` | `Σ_{m=1..12} min(r(k,m), C(k))` |
| `Y(k)` | `index_return_year(k)` | `Π_{m=1..12}(1 + r(k,m)) − 1`, the compounded raw year return |
| `ρ(k)` | `index_credit_rate(k)` | the *Indexrendite*: `max(S(k), 0)` in the Cap form, `max(q(k)·Y(k), 0)` in the *Quote* form |
| `X(k)`, `U(k)` | `index_credit_pp(k)`, `surplus_credit_pp(k)` | the *Indexgutschrift* `ρ(k)·w(k)·G(k)`; the safe-arm credit `(1−w(k))·b(k)·G(k)` |
| `B(k)` | `opt_budget_pp(k)` | the option budget, `w(k)·b(k)·G(k)` |
| `K(k)` | `credit_cum_pp(k)` | the *Höchststandsicherung* ledger, `Σ_{u<k} (X(u) + U(u))` |
| `Π(k)`, `Γ(k)` | `prem_paid_pp(k)`, `guar_cap_pp(k)` | cumulative annual-mode premiums paid; the guaranteed capital, `guar_level·Π(k) + K(k)` |
| `q_d(t)`, `w_l(t)` | `mort_rate(t)`, `lapse_rate(t)` | the **annual** death and surrender rates of the policy year `t` falls in |
| `q^m_d(t)`, `w^m_l(t)` | `mort_rate_mth(t)`, `lapse_rate_mth(t)` | the **monthly** rates the recursion applies, each `1 − (1 − r)^(1/12)` |
| `D(k)`, `V(k)`, `M(k)` | `db_pp(k)`, `cv_pp(k)`, `mat_pp(k)` | the death benefit, the surrender value, the benefit at *Rentenbeginn* (non-zero only at `k = n−1`) |

`q_d` and `w_l` are dimensionless annual probabilities and `q^m_d`, `w^m_l` their geometric twelfths;
every other quantity above is EUR per policy, and the aggregate of any per-policy amount is that
amount times the count it is struck on.

### The premium

    P_b(k) = prem_gross_pp        for k < prem_term_y  (level form: policy years 1 … prem_term_y)
           = prem_gross_pp        for k = k₀ only      (single form)
           = 0                    otherwise
    P(k)   = P_b(k) · φ
    α(k)   = min(acq_cost_rate, zill_cap_rate) · BS / min(zill_years, prem_term_y)   for
             k < min(zill_years, prem_term_y), i.e. the first that many premium-paying
             years, 0 afterwards
    α₅(k)  = the same with zill_years replaced by 5, unconditionally
    P⁺(k)  = P(k) − α(k) − exp_prem_rate · P(k)
    Π(k+1) = Π(k) + P_b(k),      Π(k₀) = prem_paid_init

    prem_due(t) = ( t mod 12 == 0 )     the first month of each policy year, and no other
    premiums(t) = P(duration(t)) · l(t) where prem_due(t), else 0

`φ` multiplies the premium **collected**; it does **not** enter `BS`, and therefore does not enter the
acquisition charge or the *Mindesttodesfallschutz* floor. That is the [std] reading argued in the
specification, and getting it wrong is a numbered pitfall. On a single premium the acquisition charge
is taken in full at `k₀`, there being only one premium to take it from.

**The premium is collected annually in advance on the monthly grid too**, because § 12 Abs. 1 VVG makes
the *Versicherungsperiode* the year where premiums are not measured in shorter periods, and the
*Indexjahr* this product turns on is struck on the balance standing at the anniversary: splitting the
premium without splitting the *Indexjahr* would credit a policy with a year it did not pay for. The
*Ratenzahlungszuschlag* remains the whole of what the *Zahlweise* does here, and premium income is
identical to the annual-step model's.

### The account, and the *Indexjahr* inside it

    av_pp_at(k, "BEF_PREM")   = A(k)
    av_pp_at(k, "AFT_PREM")   = A(k) + P⁺(k)
    F(k)                      = γ · av_pp_at(k, "AFT_PREM")
    av_pp_at(k, "AFT_CHARGE") = av_pp_at(k, "AFT_PREM") − F(k)
    I(k)                      = i_g · av_pp_at(k, "AFT_CHARGE")
    av_pp_at(k, "AFT_GUAR")   = av_pp_at(k, "AFT_CHARGE") + I(k)
    av_pp_at(k, "AFT_CREDIT") = av_pp_at(k, "AFT_GUAR") + X(k) + U(k)
    A(k+1)                    = av_pp_at(k, "AFT_CREDIT")

**All of it takes a policy year**, and that is the one thing the monthly grid deliberately does not
refine: this tariff defines no monthly *Deckungskapital*, credits the guaranteed interest per
*Versicherungsjahr*, and settles the *Indexjahr* only at its end. A model that interpolated any of
those would be inventing a rule no wording states.

with the *Indexjahr* struck on the **opening** balance:

    G(k) = A(k)                                            ← before this year's premium
    B(k) = w(k) · b(k) · G(k)                              the option budget, spent
    U(k) = (1 − w(k)) · b(k) · G(k)                        the safe arm, credited
    S(k) = Σ_{m=1..12} min( r(k,m), C(k) )                 capped above, not floored below, SUMMED
    Y(k) = Π_{m=1..12} ( 1 + r(k,m) ) − 1
    ρ(k) = max( S(k), 0 )              if payoff_form == "cap"
         = max( q(k) · Y(k), 0 )       if payoff_form == "quote"
    X(k) = ρ(k) · w(k) · G(k)

**The twelve months of that sum are now rows of the frame.** `index_month(t) = t mod 12 + 1` names
which month of the *Indexjahr* month `t` is, `index_return_mth(t) = r(duration(t), index_month(t))` is
its return and `index_return_capped_mth(t)` its capped return, so

    S(k) = Σ_{t = 12k .. 12k+11} index_return_capped_mth(t)

holds by construction and is asserted in the test module. On the annual grid the same arithmetic lived
inside a single cells and could not be read off the projection at all; here *capped above and not
floored below* is visible month by month, which is the one feature of this product most often
misdescribed.

**The allocation identity, and it is the product's whole economics in one line:**

    B(k) + U(k) = b(k) · G(k)      for every policy year k

— the year's declared surplus is either spent on options or credited as interest, never both and never
neither. `check_surplus_alloc()` asserts it.

**The lock-in ledger and the guarantee:**

    K(k+1) = K(k) + X(k) + U(k),          K(k₀) = guar_locked_init
    Γ(k)   = guar_level · Π(k) + K(k)

`Γ` is monotone non-decreasing by construction, because both terms are; `check_lock_in()` asserts that,
together with `X(k) ≥ 0` and `U(k) ≥ 0`. **`A(k)` is not asserted monotone, and must not be**: with
`γ ≥ i_g` the account falls in a year that credits nothing, which is exactly model point 13's 0,25 %
cohort. The ratchet protects the credits, not the balance.

**The § 169 Abs. 3 shadow account** runs the identical recursion, and carries the identical within-year
timings, with `α₅` in place of `α` — the credits are the same, so only the acquisition profile differs:

    av_min_pp_at(k, "AFT_GUAR") = ( av_min_pp(k) + P(k) − α₅(k) − β·P(k) ) · (1 − γ) · (1 + i_g)
    av_min_pp(k+1)              = av_min_pp_at(k, "AFT_GUAR") + X(k) + U(k)

With `zill_years = 5` the two accounts coincide exactly and the floor is a no-op, which is the point:
delib's charge profile is already at the statutory floor. Set `zill_years = 1` and the floor bites.

### Decrements

    q_d(t)    = mort_table[sex, x(t)]                         the year's ANNUAL rate
    q^m_d(t)  = 1 − ( 1 − q_d(t) )^(1/12)                     the monthly rate applied
    w_l(t)    = 0                          if duration(t) == n − 1
              = lapse_table[duration(t)]   otherwise           the year's ANNUAL rate
    w^m_l(t)  = 1 − ( 1 − w_l(t) )^(1/12)                     the monthly rate applied
    pols_if_at(t, "BEF_DECR")  = l(t)
    pols_death(t)              = l(t) · q^m_d(t)
    pols_if_at(t, "AFT_DEATH") = l(t) − pols_death(t)
    pols_lapse(t)              = pols_if_at(t, "AFT_DEATH") · w^m_l(t)
    pols_if_at(t, "AFT_LAPSE") = pols_if_at(t, "AFT_DEATH") − pols_lapse(t)
    pols_maturity(t)           = pols_if_at(t, "AFT_LAPSE")   if t == 12n − 1, else 0
    l(t+1)                     = 0                            if t == 12n − 1
                               = pols_if_at(t, "AFT_LAPSE")   otherwise

    pols_surv_year_end(k)      = pols_if_at(12k + 11, "AFT_LAPSE")

Death and surrender are **sequential**, not competing: the month's deaths are taken first and the lapse
rate is applied to the survivors of death — the annual grid's own order, a twelfth at a time. Because
`(1 − q^m_d)^12 (1 − w^m_l)^12 = (1 − q_d)(1 − w_l)` exactly, `l(12k)` at every anniversary is the
annual grid's `l(k)` to the last bit, and `pols_surv_year_end(k)` — the population the *Indexjahr*
credit is given to — is unchanged. What the finer grid changes is the **split** of a year's exits
between the two decrements, not their total.

The surrender rate is zero **through the whole final policy year**, which is the library's convention
and is shared with `KLV_DE_S` and `RLV_DE_S`: that year ends at *Rentenbeginn* and the whole surviving
cohort is booked as a maturity. A within-final-year surrender is now expressible and is deliberately
not modelled, no source establishing one.

**Closure**, asserted by `check_pols_roll_fwd()`:

    Σ_{t=t₀..12n−1} [ pols_death(t) + pols_lapse(t) + pols_maturity(t) ] = pols_if_init()

### Benefits

    D(k) = max( av_pp_at(k, "AFT_GUAR"), death_min_rate · BS )
    V(k) = max( av_pp_at(k, "AFT_GUAR"), av_min_pp_at(k, "AFT_GUAR") ) · (1 − storno_rate · surr_charge_on)
    M(n−1) = max( A(n), Γ(n) )

    claims(t, "DEATH")    = D(duration(t)) · pols_death(t)
    claims(t, "LAPSE")    = V(duration(t)) · pols_lapse(t)
    claims(t, "MATURITY") = M(duration(t)) · pols_maturity(t)

**The counts are monthly and the amounts are annual.** A claim is recognised in the month it happens
and is paid the policy year's own amount, because the account it is paid out of is defined at
anniversaries.

**Read the asymmetry, because it is the point.** Death and surrender are struck on
`av_pp_at(k, "AFT_GUAR")` — the account **before** the year's index and safe-arm credits — because a
mid-year exit forfeits the running *Indexjahr* [std]. The maturity is struck on `A(n)`, the balance at
*Rentenbeginn*, **including** that year's credits, because the contract ran the *Indexjahr* to its end.
Two exits at the same instant therefore take different amounts, and a model that pays them the same has
lost the product's own rule. The monthly grid **dates** that forfeiture: the annual grid put every exit
at a year end and so silently gave each the favourable date, while here a surrender in month 7 of an
*Indexjahr* is a row of the projection. The payoff is still not pro-rated — no carrier convention for
that was established — so the forfeiture remains all-or-nothing [std] and the grid says when it bites.

Two reported quantities that are not cash flows:

    rentenfaktor()   = max( rentenfaktor_guar, rentenfaktor_curr )
    ann_monthly_pp() = M(n−1) / 10 000 × rentenfaktor()  if ann_option == "annuity", else 0.0

### Expenses and the cash flow statement

    exp_acq_pp(t)   = acq_expense_rate · BS      at t = t₀ and only if dur_init == 0
    exp_maint_pp(k) = exp_fixed_pp · (1 + exp_infl)^k          the YEAR's amount
    expenses(t)     = ( exp_acq_pp(t) + exp_maint_pp(duration(t)) / 12 ) · l(t)

    net_cf(t)          = premiums(t) − claims(t,"DEATH") − claims(t,"LAPSE") − claims(t,"MATURITY")
                         − expenses(t)
    liability_cf(t)    = − net_cf(t)

The maintenance level is a **twelfth of the year's amount** rather than a monthly amount of its own, so
a year of it on a closed cohort is exactly the annual grid's charge; the inflation factor steps on the
**anniversary**, because it compounds in policy years and a twelfth-rooted inflation would be a
different assumption wearing the same number. What the finer grid buys is that a policy leaving
mid-year bears administration only for the months it was there.

**`result_cf()` publishes, indexed by the month `t` and in this order:**

`pols_if`, `premiums`, `claims_death`, `claims_lapse`, `claims_maturity`, `expenses`, `liability_cf`,
`net_cf`.

The first column is `pols_if` and the frame contains `net_cf`, as the house style requires.
`result_cf_annual()` sums it into policy years, indexed by the 1-based `policy_year`, which is the view
the worked example below is stated on.

**The account movements live in `result_index()`**, the annual state table: `guar_int`,
`surplus_credit`, `index_credit` and `av` beside the *Indexjahr* itself. They are **state movements,
not cash flows** — credits to the policyholder's account that reach the insurer's cash flow only later,
through a benefit — they move once a policy year, and summing them into `net_cf` is a numbered pitfall.

The aggregates are struck on the count each amount actually attaches to.
`prem_to_av(k) = P⁺(k)·l(12k)`, `av_charge(k) = F(k)·l(12k)` and `guar_int(k) = I(k)·l(12k)` are on the
year's opening in-force, because the decrementing lives paid the premium and earned the guaranteed
interest before they left; but `surplus_credit(k) = U(k) · pols_surv_year_end(k)` and
`index_credit(k) = X(k) · pols_surv_year_end(k)` — **credits go to survivors**, because the
decrementing lives left before the *Indexjahr* closed. `av_released(k)` is the account those exits take
out of the account, and it is a cells in its own right for exactly that reason.

### The published identities

Six `check_*()` cells, each taking no argument and returning a `bool` over the whole frame, each with a
residual companion beside it. **The residual's argument follows its cells' clock**: `check_net_cf()`
and `check_pols_roll_fwd()` carry `check_*_resid(t)` per month, and the four annual identities carry
`check_*_resid(k)`, one per policy year. `check_net_cf()` is mandatory in this library.

| Check | Clock | Identity |
|---|---|---|
| `check_net_cf()` | month | `net_cf(t) = premiums(t) − claims_death(t) − claims_lapse(t) − claims_maturity(t) − expenses(t)` |
| `check_av_roll_fwd()` | **year** | `av(k+1) = av(k) + prem_to_av(k) − av_charge(k) + guar_int(k) + surplus_credit(k) + index_credit(k) − av_released(k)`, where `av_released(k) = av_pp_at(k,"AFT_GUAR")·(deaths + surrenders of policy year k) + A(k+1)·maturities`; at `k = n−1` the `A(k+1)` term is `A(n)` |
| `check_pols_roll_fwd()` | month | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t)`, and the three exits plus nothing sum to `pols_if_init()` |
| `check_surplus_alloc()` | **year** | `opt_budget_pp(k) + surplus_credit_pp(k) = surplus_rate(k) · index_base_pp(k)` |
| `check_lock_in()` | **year** | `guar_cap_pp(k+1) ≥ guar_cap_pp(k)`, `index_credit_pp(k) ≥ 0` and `surplus_credit_pp(k) ≥ 0` |
| `check_index_credit()` | **year** | `0 ≤ index_credit_rate(k) ≤ 12·index_cap(k)` in the Cap form and `≤ index_quote(k)·max(Y(k), 0)` in the *Quote* form |

A monthly residual for the account roll-forward would first have had to invent a monthly account, and
one for the *Indexjahr* a monthly settlement; neither exists in this contract, and the two-clock split
is what makes writing one impossible.

`av_released(k)` is the account the exits take **out of the account**, which is not the same as the
amounts they are **paid**: the death floor pays more than the account releases, the *Stornoabzug* pays
less, and the *Beitragsgarantie* pays more. Those three differences are insurer money, and keeping them
outside the account roll-forward is what makes `check_av_roll_fwd()` exact rather than approximate.

### Processing order, on two clocks

**The annual block runs once per policy year `k`, and is steps A1 to A8. The monthly block runs in
every month `t` of that year, and is steps M1 to M4.**

The annual block, for `k = k₀ … n−1`:

A1. **Open the year.** `A(k)`, `x(k) = entry_age + k`; the population is `l(12k)`. If `k ≥ n`, stop.
A2. **Strike the participating base**, `G(k) = A(k)` — before this year's premium. This is what the
    *Indexjahr* is measured on, and it is the reason a new-business point credits nothing at `k = 0`
    however well the index does.
A3. **Read the election and the declaration**: `w(k)` from `election_table.csv`, `b(k)` from
    `surplus_rate_table.csv`. Split the surplus: option budget `B(k) = w(k)·b(k)·G(k)`, safe-arm credit
    `U(k) = (1−w(k))·b(k)·G(k)`.
A4. **Take the premium in advance and decompose it**: `P(k) = P_b(k)·φ`, less the acquisition charge
    `α(k)` and the administration charge `β·P(k)`; credit the remainder to the account.
A5. **Deduct the reserve charge** `γ` on the post-premium balance, then **credit the guaranteed
    interest** `i_g` on the post-charge balance. The account now stands at `av_pp_at(k, "AFT_GUAR")`,
    and **this is the balance every exit of the year is measured on.**
A6. **Strike the year's benefit amounts**, `D(k)` and `V(k)`, on that balance — with **no index or
    safe-arm credit in the year of exit**.
A7. **Run the *Indexjahr*.** Cap each of the twelve monthly returns above at `C(k)` with **no floor on
    the month**; **sum** the twelve; floor the sum at zero — or, in the *Quote* form, apply `q(k)` to
    the compounded year return and floor that. The credit is `X(k) = ρ(k)·w(k)·G(k)`.
A8. **End of the year — credit and lock in.** Add `X(k)` and `U(k)` to the account of the
    **survivors of all twelve months**, `pols_surv_year_end(k)`; roll the ledger
    `K(k+1) = K(k) + X(k) + U(k)`, the guaranteed capital `Γ(k+1) = guar_level·Π(k+1) + K(k+1)`, the
    account `A(k+1)`, the premiums paid `Π(k+1)` and the shadow account `av_min_pp(k+1)`.

The monthly block, for `t = t₀ … 12n−1`:

M1. **Open the month.** `duration(t) = t // 12` selects the year's state; the population is `l(t)`;
    `index_month(t)` says which month of the *Indexjahr* this is, and `index_return_mth(t)` and
    `index_return_capped_mth(t)` publish its raw and capped returns.
M2. **Collect the premium where one is due**, `prem_due(t)` in the first month of the policy year:
    `premiums(t) = P(duration(t))·l(t)`.
M3. **Incur the insurer's expenses** on the month's opening in-force: the acquisition expense at `t₀`
    for new business, and a twelfth of the year's maintenance every month.
M4. **End of the month — decrements and benefits.** Deaths at `q^m_d(t)`; then surrenders at `w^m_l(t)`
    on the survivors of death. Deaths take `D(duration(t))`, surrenders `V(duration(t))`. Through the
    final policy year the surrender rate is zero, and at `t = 12n−1` the survivors of death are
    maturities taking `M(n−1) = max(A(n), Γ(n))`; report the annuity that buys at
    `max(rentenfaktor_guar, rentenfaktor_curr)`, or nothing if the *Kapitalwahlrecht* is exercised.
    Then roll `l(t+1)` and publish `net_cf(t)`.

Steps A2 and A8 are the pair that defines the product: the base is struck **before** the premium and
the credit lands **after** every one of the year's decrements.

---

## Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. **Each one is
a test** in `tests/test_indexpolice_de.py`.

**Pitfalls 2, 3 and 4 now have an external check.** Allianz publishes two worked *Indexjahre* on the
EURO STOXX 50 at an exemplary Cap of 3,2 % and *Partizipationssatz* of 75,00 % [S2] [S5], and the
arithmetic is delib's. In **2020/2021** the twelve monthly movements were +18,06 %, +2,26 %, −2,52 %,
+4,45 %, +7,78 %, +1,42 %, +1,63 %, +0,61 %, +0,62 %, +2,62 %, −3,53 %, +5,00 %; four of them capped to
3,20 %, the three negative months passing through **in full**, the twelve **summed** to **15,90 %**, and
75 % of that credited as an *Indexpartizipation* of **11,92 %** — against a point-to-point index gain of
43,69 %. In **2021/2022** the same arithmetic summed to **−26,96 %** and the *maßgebliche Jahresrendite*
was **0 %**. The carrier's own footnote is pitfall 3 stated by the insurer: "Die Wertentwicklung des
EURO STOXX 50® ergibt sich aus der Differenz der Kurse zu Beginn und zum Ende des Betrachtungszeitraumes,
**nicht aus der Summe der monatlichen Wertentwicklungen**." Re-running that table through this model's
`index_sum` and `index_credit_rate` at `cap = 0.032` reproduces 15,90 % and 0 % and would be a
worthwhile addition to the test file; **it is not in the shipped tests**, whose anchors are the
research file's constructed Examples A and B.

**One structural gap the same document exposes.** Allianz applies a monthly Cap **and** a
*Partizipationssatz* to the capped sum; delib's `cap` payoff form has no participation factor (`w` is
the election share) and its `quote` form has no cap, so `X(t) = q · max(S(t), 0) · G(t)` — the actual
Allianz payoff — **is not expressible in the shipped model**. Adding a `quote` multiplier to the `cap`
arm would move the worked example and its golden tests, so it is recorded here as a model change to
take deliberately and is not made in a provenance pass.

1. **Treating the contract as unit-linked.** There is no *Anlagestock*, no unit price and no fund value:
   the capital is in the *Sicherungsvermögen* and the surrender value is a reserve [R15] [REG-R7]
   [REG-R28]. Assert that no `unit_price` / `fund_value` cells exists, that `cv_pp(k)` derives from
   `av_pp`, and that a negative index year never reduces the account:
   `av_pp_at(k,"AFT_CREDIT") ≥ av_pp_at(k,"AFT_GUAR")` in every policy year.
2. **Flooring each month at zero.** `x(m) = min(r, C)` has **no lower bound**. On the anchor's `k = 9`
   (research Example B, policy year 10) the correct sum is **−2,60 %** and the credit is **0,00 €**; an
   implementation that floors each capped month gets `S = +12,60 %` and credits something. Assert
   `index_sum(9) < 0` and `index_credit_pp(9) == 0.0`.
3. **Compounding the capped returns instead of summing them.** The contractual formula is a **sum**. On
   `k = 8` (Example A, policy year 9) assert `index_sum(8) == 0.0890` exactly, and that the twelve
   `index_return_capped_mth(t)` of months 96 to 107 sum to it; compounding the same
   twelve capped returns gives **8,9599 %**, an error of 0,0599 points — small enough to look like
   rounding and large enough to be wrong at every duration.
4. **Applying the floor to the compounded raw return.** On `k = 9` the raw year return is
   `Y(9) = +6,4402 %` — **the index rose and the credit is zero**. An implementation that computes
   `max(Y, 0)` credits 6,44 %, and one that computes `max(q·Y, 0)` on the Cap model point credits
   3,86 %. Assert `index_return_year(9) > 0` while `index_credit_rate(9) == 0.0` on model point 1.
5. **Striking the participation on the wrong base.** `G(t) = av_pp(k)`, **before** the year's premium
   and before the year's charges — no longer **[std]** but the rule in both retrieved AVB, which
   exclude the year's premiums and *Zuzahlungen* from the *Bezugsgröße* ([S2] Ziffer 3.3, [S7] § 3
   Ziffer 2). Assert `index_base_pp(k) == av_pp(k)` in every policy year, and that on
   the anchor `index_credit_pp(0) == 0.0` even though `index_credit_rate(0) > 0` — the base is zero at
   inception. A model striking the base after the premium credits a first-year amount that does not
   exist.
6. **Crediting the index *and* the declared surplus.** They are alternative applications of **one**
   budget [R1] [R8]. Assert `check_surplus_alloc()`; assert `surplus_credit_pp(k) == 0.0` in every policy
   year on model point 1 (`w = 1`) and `index_credit_pp(k) == 0.0` in every policy year on model point 11
   (`w = 0`);
   and assert model point 12 (`w = 0,5`) splits the budget exactly in half.
7. **Adding the declared rate on top of the guaranteed rate.** The market's *laufende Verzinsung*
   **is** the guarantee plus the surplus, not a further credit above it [REG-R53]. In the index arm the
   surplus is not credited at all. Assert that on model point 9 (`zero_path`, `w = 1`) the account grows
   at exactly `(1 − γ)(1 + i_g)` on the post-premium balance every year, and that on model point 11
   (`w = 0`) it grows by exactly `i_g` plus `b·G(t)` and by nothing more.
8. **Crediting the *Indexjahr* to the lives that left during it.** Credits go to
   `pols_surv_year_end(k)`, not to `pols_if(12k)`. Assert `check_av_roll_fwd()` in every policy year, and
   assert `index_credit(t) == index_credit_pp(k) * pols_if_at(t, "AFT_LAPSE")`.
9. **Paying a pro-rata index credit on a mid-year exit.** No credit in the year of exit — the rule in
   both retrieved AVB, which credit the participation only at the start of the following *Indexjahr*
   ([S2] Ziffer 3.3, [S7] § 3 Ziffer 5) and add nothing pro rata for the running one. Assert
   `db_pp(k) == max(av_pp_at(k,"AFT_GUAR"), death_min_rate * prem_sum())` exactly, with no index term,
   and that `av_pp_at(k,"AFT_GUAR") < av_pp(k+1)` in every year the index credited something — the
   benefit is struck on the balance **before** the year's credits. Assert it on that balance and not
   on `db_pp` itself: the *Mindesttodesfallschutz* floor of 32 400,00 € exceeds the anchor's account
   until `k = 12` (policy year 13), so the death benefit before then is larger than the account at any
   timing, which is what a floor is for.
10. **Testing the lock-in as "the account never falls".** It is the **credits** that ratchet, not the
    balance. On model point 13 (`guar_rate = 0,25 % = γ`) the account is flat or falling once premiums
    stop, while `guar_cap_pp` is still monotone. Assert `check_lock_in()` on every point **and** that
    `av_pp(k+1) < av_pp(k)` for at least one `t` on model point 13 — the invariant that would fail if
    the ratchet had been written on the wrong quantity.
11. **Running the guarantee as an annual guaranteed rate on the reserve.** *Neue Klassik*: the
    *Beitragsgarantie* is owed **at *Rentenbeginn* only** — the retrieved Perspektive KID puts it
    exactly so, "Dieser Schutz vor künftigen Marktentwicklungen gilt jedoch nicht, wenn Sie vor dem
    vereinbarten Rentenbeginn einlösen" [S6], and R+V's AVB § 1 Ziffer 2 owes 90 % of premiums "zum
    vereinbarten Rentenbeginn" [S7]. Assert that `guar_cap_pp(k)` never
    enters a benefit before `t = n−1`, that `av_pp(k) < guar_cap_pp(k)` is permitted at intermediate
    `t`, and that `claims_maturity(n−1) == max(av_pp(n), guar_cap_pp(n)) * pols_maturity(n−1)`.
12. **Forgetting the *Beitragsgarantie* floor at *Rentenbeginn*.** Assert that on model point 9 the
    floor **binds**: `mat_pp(n−1) == guar_cap_pp(n) > av_pp(n)`, and that it does **not** bind on the
    anchor. A model with no floor and a model with a floor that never binds look identical on twelve of
    the thirteen points.
13. **Confusing the § 169 Abs. 3 floor with the *Höchstzillmersatz*.** Two different rules with two
    different functions: the DeckRV governs what may be **reserved**, § 169 VVG what must be **paid**
    [REG-R16] [REG-R28]. Assert that with `zill_years = 5` the shadow account equals the tariff account
    in every policy year (the floor is a no-op) while the 2 % *Stornoabzug* still bites, and that
    `cv_pp(k) < av_pp_at(k,"AFT_GUAR")` on every point with `surr_charge_on = 1`.
14. **Double-charging or mis-basing the *Ratenzahlungszuschlag*.** `φ` multiplies the premium
    **collected** and does **not** enter the *Beitragssumme*. On model point 4 (monthly) assert
    `prem_gross_pp(k) == 2 400,00 × 1,05 == 2 520,00` while `prem_sum() == 2 400,00 × 32 == 76 800,00`,
    so the acquisition charge and the 50 % death floor are unchanged by the payment frequency.
15. **Letting the Cap and the option budget be independent parameters.** They are not: the Cap is the
    level at which the option strip costs the budget. Assert `index_budget_ratio()` — total index credits
    over total option budget — and report it beside the worked example. At the shipped pair it is
    **not** 1, and the notes say which way and why (assumption class (b), footnote 2).
16. **Assuming the *Wahlrecht* is exercised optimally, or that its path is known.** It is a
    **behavioural** assumption, not a contractual one. Assert that model point 11 (`always_safe`)
    reproduces a *klassische Rentenversicherung* exactly — every index cells evaluates, none of them
    reaches the account — and that model point 10 (`switch_at_15`) has `index_credit_pp(k) == 0.0` for
    every `t ≥ 15` and `surplus_credit_pp(k) == 0.0` for every `t ≤ 14`.
17. **A lapse assumption flat in duration.** The duration-12 tax threshold is the strongest single
    driver of German surrender behaviour [R14] [REG-R45]. Assert `lapse_rate(11) > lapse_rate(10)` —
    policy year 12 against policy year 11 — and `lapse_rate(proj_len() − 1) == 0.0` while
    `lapse_rate_base(proj_len() − 1)` is still the table's 2 %.
18. **Reporting the credits inside `net_cf`.** `guar_int`, `surplus_credit` and `index_credit` are state
    movements; they reach the insurer's cash flow only through a benefit. Assert `check_net_cf()`, and
    assert that `net_cf` is unchanged when the three columns are dropped from the frame.

---

## Policyholder behaviour modelling

All formulas are **[std]** reference constructions; there is no German calibration evidence for any of
them, and none for this product specifically.

- **Base surrender.** The duration table above, with its year-12 step at the tax threshold and its zero
  in the final policy year. Cumulative surrender over the anchor's 27 years is a material fraction of
  the cohort, so the assumption governs how much of the ratcheted late-duration capital is ever carried
  to *Rentenbeginn*.
- **The *Wahlrecht* election.** Four shipped paths, base run `w = 1`. **The base run is a modelling
  choice, not a claim about behaviour**: the product exists to demonstrate the index mechanic, and a
  base run in the safe arm would reduce it to `RV_DE_S`. The alternative belief — that policyholders are
  inert and never revisit an election made at inception — is equally unevidenced and is the reason
  `switch_at_15` and `half_half` are shipped rather than described.
- **Dynamic surrender is not modeled, and the reason is specific to this product.** On a
  *fondsgebundene* contract a falling account value drives surrender; here the account cannot fall from
  the index, so the natural dynamic driver is absent. The candidate driver that *is* present — a run of
  zero *Indexjahre*, which at the research file's parameters is expected about two years in three — is
  a **disappointment** effect with no published calibration, and inventing one would put a large
  unevidenced number at the centre of the result. A reference multiplier for a user who wants one:
  `M(t) = 1 + λ · (number of consecutive zero credits ending at t − 1)`, with `λ = 0` in the base run.
- **The mid-year-exit incentive is not modeled either.** With no credit in the year of exit, a rational
  policyholder surrenders just after an *Indexjahr* ends. The monthly grid can now represent the
  alternative — an exit falls in the month it happens and the eleven unfavourable months are rows of
  the frame — so what is missing is no longer the grid but the **behaviour**: the surrender rate is
  unconditional and no published calibration of a timing response exists.
- **What the model deliberately does not do.** No *Beitragsfreistellung* decrement (the paid-up
  account diverges from the premium-paying one at the moment of conversion and tracking it needs a
  conversion-cohort ledger [REG-R28]); no *Dynamik* take-up; no *Zuzahlungen*; no *Kapitalwahlrecht*
  election **rate** — `ann_option` is a model-point configuration, and treating it as a take-up rate
  would stand in for a tax comparison the model does not perform [R14] [REG-R45].

---

## Worked example

**Configuration.** Model point 1, the anchor cell, in full: `point_id = 1`;
`policy_id = "DE-IDX-0001"`; `sex = M`; `entry_age = 40`; `dur_init = 0`, so `t_start() = 0` and the
table below is the **entire** projection; `pols_if_init = 1.0`; `ann_start_age = 67`, hence
`proj_len_y() = 67 − 40 = 27` policy years and `proj_len() = 324` months, `t = 0 … 323`;
`prem_form = level`; `prem_gross_pp = 2 400,00 €` (the annual-mode
*Jahresbeitrag*, i.e. the research file's 200,00 € a month taken annually); `prem_freq = annual`, so
`freq_load() = 1,000` and the premium collected equals the premium due; `prem_term_y = 27`, premiums
payable throughout, so `prem_sum() = 27 × 2 400,00 = 64 800,00 €`; `av_pp_init = 0,00 €`;
`guar_locked_init = 0,00 €`; `prem_paid_init = 0,00 €`; `guar_level = 0,90`, a *Beitragsgarantie* of
`0,90 × 64 800,00 = 58 320,00 €` at *Rentenbeginn* plus every locked-in credit; `guar_rate = 0,0100`,
the *Höchstrechnungszins* for 2025–2026 [R7] [R18] [REG-R15]; `payoff_form = "cap"`;
`index_id = "eqidx_vol17"`, so the Cap is 3,00 % a month and the *Indexjahre* at `k = 8` and `k = 9`
are the research file's Examples A and B; `elect_id = "always_index"`, so `w(k) = 1,00` in every one of
the 27 years and the safe arm is never used; `death_min_rate = 0,50`, a *Mindesttodesfallschutz* floor
of `0,50 × 64 800,00 = 32 400,00 €`; `ann_option = "annuity"`; `surr_charge_on = 1`.

**Assumptions, each tagged.** Guaranteed rate `i_g = 1,00 %` a year, credited on the post-charge balance
— the contract's *Rechnungszins*, at the *Höchstrechnungszins* for 2025–2026 [R7] [R18] [REG-R15].
Declared surplus rate `b(k) = 2,50 %` a year of `G(k)`, level over all 27 years **[std]** — the option
budget, consistent with the 2026 market averages [R20] [REG-R53]. Election `w(k) = 1,00` for every `k`
**[std]**, so `opt_budget_pp(k) = 2,50 % × G(k)` and `surplus_credit_pp(k) = 0,00 €` throughout.
Monthly Cap `C(k) = 3,00 %` for every `k` **[std]**, the midpoint of a 1,5–5,0 % band that no carrier
document could confirm. *Partizipationsquote* `q(k) = 60 %` **[std]**, carried but unused on this point.
Monthly index returns from `eqidx_vol17` **[std]**: 40 years × 12 months from
`numpy.random.default_rng(20260829).normal(0.0060, 0.0500, size=(40, 12))` rounded to four decimal
places — a monthly mean of 0,60 % and standard deviation of 5,00 %, an annualised 17,3 % — with row
`k = 8` replaced by Example A (1,80 / −2,40 / 4,60 / 0,90 / −3,70 / 2,20 / 3,40 / −1,10 / 0,40 / 5,20 /
−0,80 / 2,60 per cent) and row `k = 9` by Example B (6,50 / −2,10 / 5,80 / −1,90 / −2,40 / 4,20 /
−3,10 / 0,60 / −2,80 / 5,10 / −1,70 / −1,20 per cent). Mortality `qx(M, x) = 0,001200 × 1,095^(x − 40)`
**[std]**, so `mort_rate(0) = 0,001200` at attained age 40 and the proxy is anchored there; DAV 2008 T
and DAV 2004 R are cited by name and never shipped [REG-R48] [REG-R49]. Surrender
`lapse_rate_base` = 5 % in policy years 1–2 (`k = 0, 1`), 3 % in policy years 3–11, 6 % in policy year
12 (`k = 11`), 2 % from policy year 13 **[std]**, with `lapse_rate` zero through the whole final policy
year `k = 26` because its end is *Rentenbeginn*. Acquisition charge
`acq_cost_rate = 2,5 %` of the *Beitragssumme* **[std]** — `0,025 × 64 800,00 = 1 620,00 €` — spread
over `zill_years = 5` premium-paying years at `324,00 €` a year, inside the DeckRV § 4
*Höchstzillmersatz* of 25 ‰ [REG-R16]. Premium charge `β = 3 %` of each gross premium **[std]**, i.e.
`72,00 €` a year. Reserve charge `γ = 0,25 %` a year of the post-premium balance **[std]**. Acquisition
expense `acq_expense_rate = 2,5 %` of the *Beitragssumme* **[std]**, `1 620,00 €` incurred in full at
inception. Maintenance expense `36,00 €` a year inflating at `exp_infl = 1,5 %` **[std]**. *Stornoabzug*
`storno_rate = 2 %` of the base surrender value **[std]**. *Rentenfaktor* `25,00 €` per 10 000 € per
month, guaranteed and current equal **[std]**. No claim expense, no *Dynamik*, no *Beitragsfreistellung*,
no dynamic behaviour module, no discounting.

All amounts in euros; `pols_if` to six decimals, cash flows and balances to the cent. The **Total** row
is summed **at full precision and then rounded**, not summed from the rounded cells.

**The projection.** The cash flow columns are `Projection[1].result_cf_annual()`, the monthly frame
summed into policy years; `guar_int`, `index_credit` and `av` are `result_index()`, the annual state.
The key is the 0-based policy year `k = policy_year − 1`, so row `k` covers months `12k … 12k + 11`.
`surplus_credit` is **0,00 € in every year** — the anchor elects the index arm in all 27 — and
`liability_cf` is exactly `−net_cf`; both are omitted here for width. `av` is a **balance**, so its
column is deliberately not totalled: adding twenty-seven opening balances is not a quantity.

| k | x(k) | pols_if | premiums | claims_death | claims_lapse | claims_maturity | expenses | guar_int | index_credit | av | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 40 | 1.000000 | 2,400.00 | 37.98 | 98.87 | 0.00 | 1,655.15 | 19.99 | 0.00 | 0.00 | 608.00 |
| 1 | 41 | 0.948860 | 2,277.26 | 39.46 | 188.31 | 0.00 | 33.85 | 38.08 | 81.79 | 1,915.73 | 2,015.64 |
| 2 | 42 | 0.900233 | 2,160.56 | 41.39 | 163.80 | 0.00 | 32.90 | 55.21 | 186.81 | 3,730.48 | 1,922.46 |
| 3 | 43 | 0.871969 | 2,092.73 | 43.90 | 217.08 | 0.00 | 32.35 | 73.17 | 1,204.06 | 5,587.67 | 1,799.40 |
| 4 | 44 | 0.844477 | 2,026.75 | 46.55 | 297.50 | 0.00 | 31.80 | 100.28 | 0.00 | 8,360.99 | 1,650.90 |
| 5 | 45 | 0.817730 | 1,962.55 | 49.36 | 346.53 | 0.00 | 31.25 | 116.82 | 41.78 | 9,807.67 | 1,535.41 |
| 6 | 46 | 0.791700 | 1,900.08 | 52.33 | 393.74 | 0.00 | 30.70 | 132.75 | 0.00 | 11,465.08 | 1,423.30 |
| 7 | 47 | 0.766360 | 1,839.26 | 55.46 | 436.73 | 0.00 | 30.16 | 147.26 | 0.00 | 12,978.50 | 1,316.90 |
| 8 | 48 | 0.741686 | 1,780.05 | 58.78 | 476.85 | 0.00 | 29.63 | 160.80 | 1,239.56 | 14,394.07 | 1,214.79 |
| 9 | 49 | 0.717651 | 1,722.36 | 62.28 | 550.86 | 0.00 | 29.10 | 185.79 | 0.00 | 16,954.47 | 1,080.12 |
| 10 | 50 | 0.694231 | 1,666.15 | 65.97 | 584.59 | 0.00 | 28.56 | 197.19 | 0.00 | 18,152.02 | 987.03 |
| 11 | 51 | 0.671401 | 1,611.36 | 68.87 | 1,231.45 | 0.00 | 27.64 | 207.72 | 0.00 | 19,261.02 | 283.40 |
| 12 | 52 | 0.629062 | 1,509.75 | 75.18 | 416.27 | 0.00 | 26.78 | 210.68 | 823.46 | 19,656.70 | 991.52 |
| 13 | 53 | 0.614282 | 1,474.28 | 89.77 | 453.85 | 0.00 | 26.54 | 229.75 | 0.00 | 21,602.56 | 904.11 |
| 14 | 54 | 0.599646 | 1,439.15 | 102.63 | 473.76 | 0.00 | 26.29 | 239.88 | 0.00 | 22,651.89 | 836.46 |
| 15 | 55 | 0.585141 | 1,404.34 | 116.85 | 492.49 | 0.00 | 26.04 | 249.41 | 0.00 | 23,641.56 | 768.96 |
| 16 | 56 | 0.570753 | 1,369.81 | 132.54 | 510.02 | 0.00 | 25.77 | 258.35 | 0.00 | 24,571.29 | 701.48 |
| 17 | 57 | 0.556471 | 1,335.53 | 149.81 | 526.34 | 0.00 | 25.50 | 266.69 | 0.00 | 25,440.64 | 633.88 |
| 18 | 58 | 0.542280 | 1,301.47 | 168.80 | 541.45 | 0.00 | 25.22 | 274.43 | 0.00 | 26,249.06 | 566.00 |
| 19 | 59 | 0.528168 | 1,267.60 | 189.63 | 555.33 | 0.00 | 24.92 | 281.55 | 0.00 | 26,995.84 | 497.72 |
| 20 | 60 | 0.514121 | 1,233.89 | 212.44 | 567.95 | 0.00 | 24.62 | 288.05 | 0.00 | 27,680.11 | 428.89 |
| 21 | 61 | 0.500125 | 1,200.30 | 237.36 | 579.30 | 0.00 | 24.30 | 293.91 | 0.00 | 28,300.85 | 359.35 |
| 22 | 62 | 0.486168 | 1,166.80 | 264.53 | 589.34 | 0.00 | 23.96 | 299.14 | 0.00 | 28,856.92 | 288.96 |
| 23 | 63 | 0.472234 | 1,133.36 | 294.08 | 598.06 | 0.00 | 23.62 | 303.70 | 0.00 | 29,346.98 | 217.60 |
| 24 | 64 | 0.458311 | 1,099.95 | 326.15 | 605.42 | 0.00 | 23.26 | 307.59 | 0.00 | 29,769.58 | 145.12 |
| 25 | 65 | 0.444386 | 1,066.53 | 360.85 | 611.39 | 0.00 | 22.88 | 310.80 | 0.00 | 30,123.10 | 71.41 |
| 26 | 66 | 0.430446 | 1,033.07 | 402.00 | 0.00 | 31,240.67 | 22.69 | 313.29 | 0.00 | 30,405.82 | −30,632.29 |
| **Total** | — | — | **42,474.94** | **3,744.94** | **12,507.30** | **31,240.67** | **2,365.47** | **5,562.28** | **3,577.46** | — | **−7,383.44** |

The **Total** row is the sum **at full precision, then rounded**, over all 324 months. Four of the
eight totals differ from the sum of the twenty-seven already-rounded annual cells, each by a cent or
two: `claims_death` 3 744,94 € against 3 744,95 €, `claims_lapse` 12 507,30 € against 12 507,28 €,
`expenses` 2 365,47 € against 2 365,48 €, and `net_cf` −7 383,44 € against −7 383,48 €. **Assert the
full-precision totals**; a test written against the rounded column will fail on four of them and look
like a modelling error.

The shape is the one a *Zillmer*-financed savings contract has and no other: a **first year that is
almost the whole story of the strain** — 1 620,00 € of acquisition expense against 2 400,00 € of
premium, so the first policy year nets 608,00 € rather than the 2 000 € the premium suggests, and
within it the first **month** nets +765,32 € while the other eleven are each mildly negative — then
twenty-five thin positive years while the account builds, then one very large negative year when the
whole surviving cohort's capital falls due at once. The surrender spike in policy year 12 (`k = 11`,
1 231,45 € against 584,59 € the year before) is the § 20 Abs. 1 Nr. 6 EStG threshold in the lapse
table and nothing else.

**What the monthly grid moved, against the annual-step model this replaced.** Premiums, the maturity
and the whole annual layer are **identical**: the account, every *Indexgutschrift*, the
*Höchststandsicherung* ledger, the guaranteed capital and the surrender value are bit-identical on all
thirteen model points. Two columns moved:

| Column | Annual grid | Monthly grid | Why |
|---|---|---|---|
| `claims_death` / `claims_lapse` | 3 780,63 € / 12 476,88 € | **3 744,94 € / 12 507,30 €** | Deaths and surrenders compete month by month rather than once a year. The total exits at every anniversary are unchanged; the split is not |
| `expenses` | 2 376,60 € | **2 365,47 €** | A policy leaving mid-year bears administration for the months it was there |

### Independent checks

Six checks. Four rebuild a number in the table by a route the model does not take, and two are
closure identities — the decrements, and the cash flow statement itself.

**1. The first policy year `k = 0` — contractual policy year 1 — rebuilt end to end with a calculator.**
The acquisition charge is `0,025 × 64 800,00 = 1 620,00 €` over five years, `324,00 €` a year; the
administration charge is `0,03 × 2 400,00 = 72,00 €`; so `P⁺(0) = 2 400,00 − 324,00 − 72,00 =
2 004,00 €`. The account opens at zero, so `av_pp_at(0,"AFT_PREM") = 2 004,00`, the reserve charge is
`0,0025 × 2 004,00 = 5,01 €`, `av_pp_at(0,"AFT_CHARGE") = 1 998,99` and the guaranteed interest is
`0,01 × 1 998,99 = 19,9899 €` — the table's `guar_int` of **19,99**, on `pols_if(0) = 1`. That leaves
`av_pp_at(0,"AFT_GUAR") = 2 018,9799 €`, and the year's two benefit amounts follow from it: the
*Mindesttodesfallschutz* floor `0,50 × 64 800,00 = 32 400,00 €` dominates the account, so
`D(0) = 32 400,00 €`, and the surrender value is `V(0) = 2 018,9799 × 0,98 = 1 978,6003 €`. **Every
line so far is annual and is unchanged by the move to a monthly grid.**

The **decrements** are where the month enters. The year's rates are `q_d = 0,001200` at attained age 40
— the proxy's own anchor — and `w_l = 0,05`; their geometric twelfths are
`q^m_d = 1 − (1 − 0,0012)^(1/12) = 0,00010006` and `w^m_l = 1 − (1 − 0,05)^(1/12) = 0,00426532`, and
twelve months of each compound back to the year exactly, so `pols_if(12) = 0,948860` — the table's
second row to six decimals, and the annual grid's own number. Summed over the twelve months the year
produces **0,001172** deaths and **0,049968** surrenders, against the annual grid's 0,001200 and
0,049940: the competing-decrement shift, total exits unchanged. Hence
`claims_death = 32 400,00 × 0,001172 = 37,98 €` and
`claims_lapse = 1 978,6003 × 0,049968 = 98,87 €`. Expenses are `1 620,00` in the first month plus
twelve twelfths of `36,00` on a falling in-force, `1 655,15 €` in all. The year nets
`2 400,00 − 37,98 − 98,87 − 0 − 1 655,15 = 608,00 €`, of which **+765,32 €** falls in the first month
— the whole *Beitrag* against the whole acquisition expense — and the other eleven are each about
−14,50 €. Every figure in the first row is reproduced without the model.

**2. The *Indexjahr* of `k = 8` — policy year 9 — rebuilt on its own terms.** The twelve capped
monthly returns of research Example A sum to `S(8) = +8,90 %` (table below), which is positive, so
`ρ(8) = 8,90 %`. On the monthly grid those twelve are rows 96 to 107 of the frame and are readable one
by one as `index_return_capped_mth(t)`; their sum is `index_sum(8)` by construction, which the test
module asserts. The base is the **opening** balance `G(8) = av_pp(8) = 19 407,2450 €`, giving
`X(8) = 0,0890 × 19 407,2450 = 1 727,2448 €` per policy; the credit goes to the survivors of all twelve
months, `pols_surv_year_end(8) = 0,717651`, so
`index_credit(8) = 1 727,2448 × 0,717651 = 1 239,5583 €` — the table's **1 239,56**, and the annual
grid's figure to the cent. Two contrasts a reader can check on the same twelve numbers: **compounding**
the capped returns instead of summing them gives 8,9599 %, and the **raw** year return is
`Y(8) = +13,4548 %` against a raw sum of +13,10 %.

**3. The decrement closure.** Summed over all 324 **months**, deaths **0,073805**, surrenders
**0,501218** and maturities **0,424977** add to **1,000000** exactly — the whole opening cohort, with
nothing left in force at `t = 324`. This is `check_pols_roll_fwd()`'s second condition, and it is built
by direct summation over the exit cells with no reference to the recursion that produced `pols_if`. The
maturity count is the annual grid's to fifteen decimals; deaths and surrenders have traded 0,000779 of
a policy between them, which is the competing-decrement shift over the whole projection.

**4. The account roll-forward in policy year `k = 8`, at fund level.**

    av(8)              14,394.0730      = av_pp(8) x pols_if(96)
    + prem_to_av(8)     1,726.6439      = 2,328.00 x 0.741686
    − av_charge(8)         40.3018      = 54.3381 x 0.741686
    + guar_int(8)         160.8042
    + surplus_credit(8)     0.0000      w(8) = 1, so the safe arm is empty
    + index_credit(8)   1,239.5583      to pols_surv_year_end(8), not to pols_if(96)
    − av_released(8)      526.3103      = 21,897.7159 x (0.0018141 + 0.0222208)
    -------------------------------
    = av(9)            16,954.4673      the table's next row

Every term is struck on a **different population**, which is the whole difficulty of this product: the
premium, the charge and the guaranteed interest on the year's opening in-force `pols_if(12k)`, the
credit on the survivors of all twelve months, and `av_released` on the year's two exits at the balance
they left with. This is `check_av_roll_fwd()`, and it is stated **per policy year**: the account is
defined at anniversaries and the *Indexjahr* settles only at the year end, so there is no monthly
residual to write. The exits are summed over the year — 0,0018141 deaths and 0,0222208 surrenders
against the annual grid's 0,0018396 and 0,0221954 — and their total, which is what the balance
release depends on, is unchanged.

**5. The cash flow statement closes on the Total row.** `42 474,94 − 3 744,94 − 12 507,30 −
31 240,67 − 2 365,47 = −7 383,44 €`, which is the `net_cf` total to the cent, and at full precision
`42 474,939948 − 47 492,910425 − 2 365,474366 = −7 383,444842`. Note what is **not** in it: the
guaranteed interest of 5 562,28 € and the index credits of 3 577,46 € are movements of the
policyholder's account, live in `result_index()` rather than in the cash flow statement, and adding
them would move `net_cf` by 9 139,74 €. This is `check_net_cf()`, and it is asserted in every one of
the 324 months.

**6. The guarantee at *Rentenbeginn*.** The ledger closes at
`credit_cum_pp(27) = 4 851,4383 €` — its value at policy year `n = 27`, the sum of the per-policy index
credits over the 27 years, the safe arm being empty — and the *Beitragsgarantie* at
`0,90 × 64 800,00 = 58 320,00 €`, so the guaranteed capital is `guar_cap_pp(27) = 63 171,4383 €`. The
account stands at `av_pp(27) = 73 511,3936 €`, above it, so the floor **does not bind** on the anchor
and `mat_pp(26) = 73 511,39 €`. The maturity cash flow
is `73 511,3936 × 0,424977 = 31 240,67 €`, the table's last row. Reported beside it, and **not a cash
flow of this model**: `ann_monthly_pp() = 73 511,3936 / 10 000 × 25,00 = 183,78 €` a month.

### The budget diagnostic

`index_budget_ratio()` on the anchor is **0,2082** — total index credits 4 851,44 € against a total
option budget of 23 298,38 €. That is a long way from 1 and it needs reading carefully, because two
different things are in it.

- **On rates**, the twenty-seven *Indexjahre* credited an average of **2,1330 %** against a budget of
  2,50 %, a ratio of **0,853**. That is the like-for-like comparison, and it is consistent with the
  research file's expectation of about 2,97 % a year at these parameters, one realised path being a
  sample of size 27 from a distribution with a 65 % chance of zero in any year.
- **On amounts** the ratio collapses to 0,2082, and the reason is **timing, not pricing**: the path
  credits at a positive rate in policy years `k = 0, 1, 2, 3, 5, 8` and `12`, and in none after `k = 12` —
  and the rate of 12,04 % at `k = 0` lands on a base of zero — so the six years that actually credit all
  fall while the account is small and the twenty-one that do not fall while it is large. `G(t)` runs
  from 0,00 € at `k = 0` to 70 637,97 € at `k = 26`, and a rate ratio weighted by `G(k)` is dominated
  by the late years.

Both numbers are worth having and neither should be quoted alone. What the pair says about the shipped
parameters is that **the Cap and the option budget are not badly mismatched on this path** — 0,853 on
rates — while the amount ratio is a warning that a single deterministic index path cannot calibrate
anything. The research file's own risk-neutral arithmetic points the other way, pricing the strip at
about 1,7 % of `G` against a 2,50 % budget, i.e. a 2,50 % budget would buy a cap somewhat **above**
3,00 %. **A calibrated model would solve for the Cap; this one is given both and reports the
discrepancy**, which is the honest treatment when neither number could be established for any carrier.

### The two *Indexjahre* the mechanic turns on

`k = 8` and `k = 9` of `eqidx_vol17` — policy years 9 and 10 — are the research file's constructed
Example A and Example B, wired into the shipped path so that the model reproduces them rather than
restating them. Monthly returns in per cent, Cap `C = 3,00 %`:

| Month `m` | A: `r(8,m)` | A: `min(r, C)` | B: `r(9,m)` | B: `min(r, C)` |
|---|---|---|---|---|
| 1 | +1.80 | +1.80 | +6.50 | +3.00 |
| 2 | −2.40 | −2.40 | −2.10 | −2.10 |
| 3 | +4.60 | +3.00 | +5.80 | +3.00 |
| 4 | +0.90 | +0.90 | −1.90 | −1.90 |
| 5 | −3.70 | −3.70 | −2.40 | −2.40 |
| 6 | +2.20 | +2.20 | +4.20 | +3.00 |
| 7 | +3.40 | +3.00 | −3.10 | −3.10 |
| 8 | −1.10 | −1.10 | +0.60 | +0.60 |
| 9 | +0.40 | +0.40 | −2.80 | −2.80 |
| 10 | +5.20 | +3.00 | +5.10 | +3.00 |
| 11 | −0.80 | −0.80 | −1.70 | −1.70 |
| 12 | +2.60 | +2.60 | −1.20 | −1.20 |
| **Sum** | **+13.10** | **+8.90** | **+7.00** | **−2.60** |
| **Compounded `Y`** | **+13.4548** | | **+6.4402** | |

**Example A** is the strong year. The cap bound in three months and cost `13,10 − 8,90 = 4,20` points;
`S(8) = +8,90 %` and `ρ(8) = 8,90 %`.

**Example B is the case the product is criticised for**: the cap bound in four months and cost
`7,00 − (−2,60) = 9,60` points, `S(9) = −2,60 %`, and so `ρ(9) = max(−2,60 %, 0) = 0`. **The index
rose 6,4402 % over the year and the credit was nothing.** The capital was untouched, and the year's
option budget bought options that expired worthless. An implementation that floors each *month* at zero
gets `S = +12,60 %` here; one that applies the floor to the compounded raw return credits 6,44 %; one
that applies the *Partizipationsquote* to it credits 3,86 %. All three are wrong, and all three look
entirely plausible in a printout.

**Model point 8 reproduces both to the euro.** It is the in-force cell, `dur_init = 8` and
`av_pp_init = 50 000,00 €`, so its frame opens at month 96 — policy year `k = 8`, its first projected
*Indexjahr* — and its
base is exactly the research file's `G = 50 000,00 €`:

- `index_credit_pp(8) = 0,0890 × 50 000,00 = 4 450,00 €`, against a *sichere Verzinsung* arm that would
  have credited `0,0250 × 50 000,00 = 1 250,00 €` — the index arm paying **3,56 times** the safe arm;
- `index_credit_pp(9) = 0,00 €` on a base of 60 631,57 €, the safe arm having offered 1 515,79 €.

### The *Partizipationsquote* variant, on the identical index path

Model point 2 is the anchor with `payoff_form = "quote"` and nothing else changed, so the two payoff
designs run against the **same** twelve monthly returns in every year. Selected rows; the **Total** row
covers all 27 years, not only the six displayed:

| t | x(t) | pols_if | premiums | claims_death | claims_lapse | claims_maturity | expenses | guar_int | index_credit | av | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 40 | 1.000000 | 2,400.00 | 37.98 | 98.87 | 0.00 | 1,655.15 | 19.99 | 0.00 | 0.00 | 608.00 |
| 3 | 43 | 0.871969 | 2,092.73 | 43.90 | 226.81 | 0.00 | 32.35 | 76.45 | 2,036.27 | 5,916.59 | 1,789.67 |
| 8 | 48 | 0.741686 | 1,780.05 | 58.78 | 511.71 | 0.00 | 29.63 | 172.56 | 1,216.40 | 15,572.35 | 1,179.93 |
| 9 | 49 | 0.717651 | 1,722.36 | 62.28 | 584.15 | 0.00 | 29.10 | 197.01 | 675.83 | 18,079.93 | 1,046.84 |
| 12 | 52 | 0.629062 | 1,509.75 | 84.12 | 465.80 | 0.00 | 26.78 | 235.75 | 832.65 | 22,169.87 | 933.05 |
| 26 | 66 | 0.430446 | 1,033.07 | 538.84 | 0.00 | 41,875.02 | 22.69 | 419.94 | 0.00 | 41,097.09 | −41,403.48 |
| **Total** | | | **42,474.94** | **4,593.94** | **14,760.66** | **41,875.02** | **2,365.47** | **6,712.41** | **16,521.86** | — | **−21,120.16** |

Summed at full precision and then rounded, as above; here **four** of the eight totals differ from
the sum of the twenty-seven rounded annual cells, each by a cent or two: `claims_death`
(4 593,94 € against 4 593,95 €), `claims_lapse` (14 760,66 € against 14 760,64 €), `expenses`
(2 365,47 € against 2 365,48 €) and `index_credit` (16 521,86 € against 16 521,85 €). `index_credit`
agrees at the cent on the Cap design and does not here.

Every *Indexjahr* figure in this table is the annual-step model's: the `index_credit` column, the
budget ratio and the two rows the designs are compared on are bit-identical, because the *Indexjahr*
is an annual construction and the conversion did not touch it. Only `claims_death`, `claims_lapse` and
`expenses` moved, for the reasons given under the anchor.

The single most instructive row is `k = 9`. On the Cap design that year credits **nothing**; on the
*Quote* design the same twelve returns credit `max(0,60 × 6,4402 %, 0) = 3,8641 %` of `G(9)`, which is
**675,83 €** at fund level. At `k = 8` the ranking reverses — the Cap design credits 8,90 % against the
*Quote*'s `0,60 × 13,4548 % = 8,0729 %` — because Example A's give-up was concentrated in three months
while the *Quote* gives away 40 % of the year in every state. **The two designs are not
interchangeable and they fail differently**, which is why a product specification may not describe one
and price the other. Over the whole projection the *Quote* design credits 16 521,86 € against the Cap
design's 3 577,46 €, and its `index_budget_ratio()` is **0,9782** against **0,2082** — on this path, at
these levels, `q = 60 %` on a 17 %-volatility price index is close to a fair spend of the budget and
`C = 3,00 %` a month is not.

### The four designs at *Rentenbeginn*

All four are the same 40-year-old paying 2 400,00 € a year to 67 under a 90 % *Beitragsgarantie* at
`i_g = 1,00 %`, differing only in what the declared surplus buys. Every column below is **per policy**
at policy year `k = n = 27`, *Rentenbeginn*, so the credit columns are the ledger `credit_cum_pp(27)` and are
larger than the frame's fund-level totals, which carry the decrements: the anchor's 4 851,44 € of per-policy index
credits is the 3 577,46 € of the `index_credit` column above, before survivorship.

| Model point | Design | Index path | Index credits | Safe-arm credits | Account | Guaranteed capital | Benefit | Monthly *Rente* | `index_budget_ratio()` |
|---|---|---|---|---|---|---|---|---|---|
| 1 (anchor) | Cap 3,00 %/month | eqidx_vol17 | 4,851.44 | 0.00 | 73,511.39 | 63,171.44 | 73,511.39 | 183.78 | 0.2082 |
| 2 | Quote 60 % | eqidx_vol17 | 28,216.23 | 0.00 | 98,534.74 | 86,536.23 | 98,534.74 | 246.34 | 0.9782 |
| 3 | Quote 100 % | houseidx_vol5 | 46,118.84 | 0.00 | 116,178.75 | 104,438.84 | 116,178.75 | 290.45 | 1.6482 |
| 11 | *Sichere Verzinsung* | eqidx_vol17 | 0.00 | 25,967.50 | 95,425.52 | 84,287.50 | 95,425.52 | 238.56 | — |

Read the last row first: **the safe arm beats the anchor's Cap design by 21 914,13 € of terminal
capital on this path.** That is not an argument against the product — it is one realisation of a payoff
whose expected value the research file puts slightly *above* the safe arm, with a two-in-three chance
of a zero year — but it is exactly why the *Wahlrecht* comparison belongs in a specification and why
`always_index` is a modelling choice rather than a recommendation. Model point 3 shows the other end:
a volatility-targeted house index at a 100 % participation rate credits 46 118,84 €, and its
`index_budget_ratio()` of 1,65 says that at 5 % volatility the shipped Cap and *Quote* are, if anything,
*too generous* for the budget — which is the same calibration failure as the anchor's, pointing the
other way. **All four columns are the same 2,50 % of surplus, spent differently.**

### Two corrections made to these notes at the model stage

The model was built to the specification above and reproduces it; two numbers in the *Known modeling
pitfalls* list did not survive contact with it, and the notes rather than the model were corrected.

1. **Pitfall 2** said that an implementation flooring each month at zero would get `S = +9,60 %` on
   `k = 9` (Example B). 9,60 points is what the cap *gave away* that year, `7,00 − (−2,60)`; flooring
   each capped month at zero gives `3,00 + 3,00 + 3,00 + 0,60 + 3,00 = +12,60 %`. The pitfall's point is unchanged
   and the corrected figure is now in it.
2. **Pitfall 9** asked for `db_pp(k) < av_pp(k+1)` in every year the index credited something. That is
   false at early durations for a reason the product intends: the *Mindesttodesfallschutz* floor of
   32 400,00 € exceeds the account until `k = 12`, so the death benefit is larger than the account at
   *any* timing there. The assertion that carries the pitfall's meaning — that the death benefit is
   struck on the balance **before** the year's credits — is
   `av_pp_at(k,"AFT_GUAR") < av_pp(k+1)` in every year that credited, and that is what the pitfall now
   asks for.

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared grid.
The valuation layers consume them and are cited, never reproduced.

- **The German statutory *Deckungsrückstellung*.** § 341f HGB requires a provision at the
  *versicherungsmathematisch berechneter Wert* of the obligations, **including profit shares already
  allocated** and after deducting the present value of future premiums — the prospective method, with a
  retrospective fallback [REG-R54]. For this product the phrase "profit shares already allocated" is the
  operative one: **every locked-in index credit is an allocated profit share** and is inside the reserve
  from the moment it is credited, which is exactly what `credit_cum_pp` tracks. The discount rate is
  capped by the DeckRV [REG-R14] and is topped up by the *Zinszusatzreserve* where the reference rate
  falls below the tariff rate [REG-R17]. **delib computes none of this.**
- **The guarantee is an option and this model prices none of it.** The *Beitragsgarantie* at
  *Rentenbeginn*, plus a ratchet that makes every credit permanent, is a written put whose cost **rises
  with every good year** — unlike a plain maturity guarantee, under which a bad year can be recovered by
  a good one. A deterministic path values it at zero except where it happens to bind (model point 9). A
  time-value-of-options-and-guarantees calculation re-runs this recursion, the election path and the
  index path per scenario, and that is what the model is shaped to feed.
- **Solvency II.** Technical provisions are a best estimate — probability-weighted future cash flows
  discounted at the relevant risk-free term structure — plus a risk margin [REG-R1] [REG-R2] [REG-R4].
  `BEL = Σ_t v(t) · liability_cf(t)` over the recursion above. An Indexpolice sits in *insurance with
  profit participation*, **not** in *index-linked and unit-linked insurance* [R15], and its **future
  discretionary benefits** — the declared rate, and therefore the option budget — are the substance of
  its best estimate. **No Solvency II treatment of future discretionary benefits, management actions or
  contract boundaries in this library was read from a retrieved instrument** [REG-R2], so every such
  figure would be [unverified].
- **The declared rate is a management action, and treating it as a fixed assumption is the model's
  largest valuation-side simplification.** A market-consistent valuation would make `b(t)` a function of
  the projected investment result under the MindZV floor [REG-R18]; here it is an input.
- **IFRS 17.** The archetypal direct-participating contract, measured under the variable fee approach;
  the fulfilment-cash-flow engine is this same projection, and grouping, CSM and risk adjustment are out
  of scope. The VFA mechanics were not read and are [unverified] [REG-R55].

---

## Key sensitivities and model risks

In rough order of leverage for this product.

1. **The Cap, and its calibration against the option budget.** The single largest lever, and the one
   parameter that **cannot be chosen freely** — a point both retrieved AVB make in their own words, the
   Cap being set annually "auf der Grundlage von Angeboten mehrerer Finanzinstitute" on the surplus, the
   *Bewertungsreserven* *Sockelbetrag* and market volatility and dividend yield [S2] Ziffer 3.3
   Absatz 2 b). At the shipped pair the research file's own arithmetic gives an expected annual credit
   of about 2,97 % against a 2,50 % budget, with a **65 % chance of a zero year**; risk-neutrally the
   same strip prices at about 1,7 %, *below* the budget. Moving the Cap from 2,5 % to 4,0 % — inside the
   plausible band and with no other change — moves the expected credit by more than the whole of the
   guaranteed interest. The shipped 3,00 % now has one external reference point: Allianz's own worked
   illustration runs at **3,2 %** [S5]. **Any expected return quoted for this product without its
   volatility assumption is meaningless.**
2. **The index path's volatility.** Volatility enters twice and in opposite directions: it makes the cap
   bind more often, lowering the expectation, and it makes the annual floor worth more, raising it. At
   the 5 % annualised volatility of `houseidx_vol5` the cap almost never binds and the payoff approaches
   the index return; at 25 % the expected credit is dominated by the floor. Model points 1 and 3 exist
   to be compared for exactly this reason.
3. **The base `G` of the participation — settled, and the model's reading is the carriers'.** Both
   retrieved AVB strike the participation on the whole *Policenwert* at the start of the *Indexjahr*,
   excluding that year's premiums and *Zuzahlungen*: "Bezugsgröße für die →Indexpartizipation ist der
   →Policenwert zu Beginn des →Indexjahres" [S2] Ziffer 3.3 Absatz 2 e), and [S7] § 3 Ziffer 2 to the
   same effect. `index_base_pp` is that quantity. This was the largest unquantified uncertainty in the
   file; it is no longer one, and the sub-account and *Überschussguthaben* readings are withdrawn.
   What remains a modelling choice is a **narrower** point the AVB expose: R+V takes the value present
   "das gesamte Versicherungsjahr", so a mid-year *Kapitalentnahme* reduces the base pro rata, and
   Allianz excludes the daily surplus attaching to in-year premiums. delib models neither partial
   withdrawals nor in-year surplus — the whole *Beitrag* falls in the first month of the
   *Versicherungsjahr* and the base is struck there — so neither refinement bites here.
4. **The declared surplus rate, held level and held exogenous — and, on the retrieved evidence, held
   low.** It is the option budget, so it scales the whole index result linearly. Assekurata's 2026
   survey puts the average declared *laufender Überschusszins* on *Indexpolicen* at **3,07 %** against
   delib's shipped 2,50 %, and even classic private annuities at 2,62 % [R20]; Stuttgarter's own
   published *sichere Verzinsung* is 2,16 % [S8]. **The shipped rate is about half a point below the
   index-segment average**, which understates every index credit by the same proportion; it is a
   shipped input and is not changed here. Both retrieved AVB also define the budget more widely than
   the model does — the year's **minimum share of the *Bewertungsreserven*** is part of it alongside
   the declared surplus, and at Allianz the surplus enters net of *Verwaltungskosten* ([S2] Ziffer 3.3,
   [S7] § 3 Ziffer 9) — so `opt_budget_pp` is a lower bound on the contractual budget as well. And
   because the feedback from the *Garantieniveau* to the asset mix to the declared rate is not modeled,
   the *Garantieniveau* sensitivity the model reports is **only the maturity-floor effect** and omits
   the budget effect entirely. A user comparing model point 9's 100 % guarantee with the anchor's 90 %
   is seeing half the real difference.
5. **The election path.** Switching model point 1 to `always_safe` turns the contract into a
   *klassische Rentenversicherung* and changes the terminal capital by the whole difference between a
   certain 2,50 % a year and a lottery with a two-in-three chance of nothing. The path is a **[std]**
   assumption with no evidence behind it in either direction.
6. **The mid-year-exit convention — settled, and the model's convention is the carriers'.** Both AVB
   credit the participation only at the start of the following *Indexjahr* and add nothing pro rata for
   the running one; on surrender Allianz adds only a pro-rata *Schlussüberschussanteil* and
   *Bewertungsreserven* *Sockelbetrag*, neither of which is an index credit [S2] Ziffer 9.2, [S7] § 3
   Ziffer 5 [R2]. It remains a real cash-flow difference against the *alternative* convention — a few
   per cent of the cohort leaves each year and each forfeits a credit a pro-rating contract would pay —
   but delib is no longer choosing between two unevidenced readings. It still interacts with the
   surrender-timing incentive — which the **annual** grid resolved in the policyholder's favour by
   construction, and which the monthly grid instead makes visible: the eleven unfavourable months of
   each *Indexjahr* now carry exits, and only a behavioural response to the incentive is missing.
7. **Lapse.** No index-specific rate exists and the GDV publishes one undifferentiated market-wide
   *Stornoquote* (2,56 % in 2023) that cannot be split by product or duration [R19], so the duration
   shape is **[std]**. On a ratcheting contract the late years carry the largest
   capital, so the assumption governs how much of the accumulated guarantee is ever paid at
   *Rentenbeginn* rather than surrendered at a discount.
8. **The *Rentenfaktor*, and the two-index mortality problem behind it.** The reported annuity is a
   **[std]** 25,00 € per 10 000 € against a **[std]** period-table mortality proxy, and the two are **not
   mutually calibrated**. The real basis is DAV 2004 R, a generational table in age and calendar year
   [REG-R49]; a period-table proxy priced at a 40-year-old's annuitisation twenty-seven years out
   understates the liability by a margin that dwarfs every other assumption here. The model therefore
   **reports** the annuity and does not compute one, and the specification says which of the two numbers
   is authoritative: neither.
9. **Charges, and the un-modeled MindZV loop.** Every charge level is **[std]**; the sector
   *Verwaltungskostenquote* runs from under 2 % to over 4 % [REG-R53], and BaFin polices the level
   [R16] [REG-R35]. Because the model does not return 50 % of the cost result to the policyholder
   [REG-R18], changing an expense assumption changes `net_cf` without changing what the policyholder
   receives — the one place where the model's economics are knowingly incomplete.
10. **The three index-specific give-ups that appear nowhere.** The option dealing spread is inside the
    Cap, the house-index level fee and volatility-target drag are inside the index, and the dividend
    yield of a price index is forgone entirely. The model represents all three **only** through the
    level of the Cap or the *Quote* it is given, so a user who raises the Cap without asking what the
    insurer could actually buy has silently removed them.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-indexpolice-r1
[R11]: #delib-indexpolice-r11
[R12]: #delib-indexpolice-r12
[R14]: #delib-indexpolice-r14
[R15]: #delib-indexpolice-r15
[R16]: #delib-indexpolice-r16
[R17]: #delib-indexpolice-r17
[R18]: #delib-indexpolice-r18
[R19]: #delib-indexpolice-r19
[R2]: #delib-indexpolice-r2
[R20]: #delib-indexpolice-r20
[R21]: #delib-indexpolice-r21
[R6]: #delib-indexpolice-r6
[R7]: #delib-indexpolice-r7
[R8]: #delib-indexpolice-r8
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R24]: #delib-reg-r24
[REG-R26]: #delib-reg-r26
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R4]: #delib-reg-r4
[REG-R45]: #delib-reg-r45
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R7]: #delib-reg-r7
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
