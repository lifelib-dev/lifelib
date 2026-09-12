# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) into a reference liability cash-flow projection model on paper. They describe no
single insurer's product. [S#] and [R#] tags resolve in `sources.md`, whose numbering is
carried verbatim from `_research/dependance.md` and is frozen; [REG-R#] tags resolve in the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
R-numbering is separate. **[std]** marks a standardization introduced for the reference
implementation, always with a rationale and, where one exists, the observed range;
[unverified] marks a claim not confirmed against a retrieved document. **Every contractual
parameter value here is identical to `product-spec.md`'s.** The model is **Dep_FR_S** on a
**monthly** grid.

Seven quantities appear here that `product-spec.md` does not carry, because they are
modeling constructs rather than contractual terms and are introduced below as such: the
**APA prevalence curve**, the **severity shares** that turn public GIR prevalence into
insured-state prevalence, the two **state-mortality multiples**, the **aggravation rate**,
the **prevalence-to-incidence identity**, the **cause mix** that weights the three
*carences*, and the **lapse table**.

**The single fact that shapes this model.** Every public French number about dependence
measures **receipt of the *allocation personnalisée d'autonomie*** — an application to a
*département*, granted on the AGGIR grid to GIR 1–4 [R2 arts. R. 232-1, R. 232-4](#frlib-dependance-r2) [R3]. It
is a **prevalence**, not an incidence; it is a **public** classification, not the insurer's;
and insurer definitions are deliberately stricter, the *notice* saying in terms that
"L'Assureur n'est pas lié par les éventuelles décisions des services publics"
[S5 art. 13] [S6 art. 21.1]. DREES notes that APA life expectancy has fallen from 30 to
29.2 months between 2010 and 2022 "traduisant un recours à cette prestation en baisse à âge
donné" [R7] — a behavioural drift in take-up, not a health improvement. Turning that series
into an insured incidence basis is the whole modeling problem of this product, and section
(c) does it explicitly rather than by assertion. **No public French LTC incidence or
continuance table exists**: [R12] specifies the structure of the laws a model needs but its
numerical bases are the insurer's own experience tables and are not disclosed, and no
BCAC-style published reference table for *dépendance* was located [R12 §3.1.3](#frlib-dependance-r12) [REG-R28].

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for a single-policy model
  point of individual *assurance dépendance*: premiums, *rente* outgo, the *capital
  d'équipement*, the premiums refunded when dependence arises inside the *carence*, and
  expenses. Reserves are not computed (see *Valuation and reserve pointers*).
- **Model structure.** A **four-state** chain — `autonomous` → `partial` / `total` → dead
  — with a fifth in-force but paid-up state, `reduced`, reached only by lapse from eight
  years. The *partielle* → *totale* transition is modeled, which is a **departure from the
  only actuarial reference retrieved**: [R12 §3.1.2](#frlib-dependance-r12) sets that transition to zero for want
  of a transition law and prices two separate guarantees instead. The contracts themselves
  do provide for deterioration [S1 §4.3.1.2] [S5 art. 13], so the reference implementation
  carries it and states the cost of the missing law below.
- **Recovery is not modeled.** Contractually the *rente* stops on improvement out of a
  covered state [S1 §4.3.1.2] [S6 art. 26] [S7 §4.2.1] and CNP allows the level to move in
  either direction [S5 art. 13]; [R12 §3.1.1](#frlib-dependance-r12) nonetheless sets the probability of return to
  autonomy to zero, and so does this model. It is a **named input held at zero**, not an
  omission, and its direction of error is stated under *Known modeling pitfalls*.
- **Projection frequency.** Monthly, matching the *rente mensuelle à terme échu*
  [S1 §4.3.1.2] [S5 art. 16] [S6 art. 26] [S7 §4.2.1] and the monthly premium
  [S1 §1.2.2] [S2]. `t` is the policy month and it is **0-based**: `t = 0` is the first
  projected month, the frame is `t = 0, 1, …, proj_len − 1`, `proj_len` is the **number**
  of projected months, and the policy year is the derived label `y(t) = floor(t/12) + 1`,
  so policy year 1 is `t = 0…11`.
- **Timing conventions [std].** Premium received at the **start** of month `t`, and only
  from lives in `pols_auto`; maintenance and assistance expense at the start of month `t`;
  all benefits, refunds and claim expenses at the **end** of month `t`; state transitions
  at end of month. The *revalorisation* of the guarantees, of the premium and of the
  *rentes en service*, and any tariff revision, all fall at the **start** of month
  `t = 12, 24, …`. Contracts revalue on a calendar date (1 January, or 1 April at the
  latest) [S1 §4.3.1.3] [S5 art. 15] [S7 §4.2.3]; replacing that with the policy
  anniversary is a **[std]** simplification worth at most six months of index.
- **Age basis.** Age at entry by *différence de millésimes* [S1 §1.1.2.1], advancing at
  each policy anniversary: `age(t) = entry_age + floor(t / 12)` **[std]**.
- **Claim duration.** `z` = months since the **first** recognition of a covered state, not
  since entry into the current state. The *franchise* clock therefore does not restart on
  deterioration from *partielle* to *totale* **[std]** — no retrieved document states that
  it does, and [S1 §4.3.1.2] makes the higher amount effective from the first day of the
  month following the opening of the right without mentioning a new *franchise*.
- **Currency and horizon.** EUR; *rente*, *capital* and premium in € per month or per
  event. Cover is *viagère* with no age limit [S1 §1.1.5] [S5 art. 8], so the projection
  runs to a terminal age of **110 [std]**: it is
  `proj_len = 12 × (110 − entry_age)` months long, 480 for the base cell, so the last
  projected month is `t = proj_len − 1 = 479`.
- **Contract boundary.** The premium is *viagère* and the tariff is revisable for the
  portfolio [S1 §1.2.3] [S5 art. 22] [S7 §4.4]. The model projects all future premiums and
  benefits inside the boundary; whether a revisable-tariff contract has a Solvabilité II
  contract boundary shorter than that is a valuation question, is not settled by any
  retrieved text, and is flagged rather than answered.
- **Discounting.** None. The model publishes undiscounted cash flows; EIOPA's monthly
  risk-free term structures are the input a market-consistent valuation would apply
  [REG-R5].
- **Rounding.** Intermediates at full double precision; displayed state probabilities to
  six decimals and cash flows to four **[std]**. Rounded monthly rows do not re-add to
  displayed totals; totals are sums of unrounded values.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `policy_id` | str | 1 |
| `entry_age` | int, 40–75 [S1 §1.1.2.1] | 70 **[std]** |
| `sex` | enum {M, F} | F **[std]** — decrements are sex-split; the premium is unisex [R12 §3.2.1](#frlib-dependance-r12) |
| `cover_type` | enum {total_only, total_and_partial} | total_and_partial [S1] [S7] |
| `trigger_grid` | enum {avq5, avq6, aggir} | avq5 [S1 §2.2] |
| `rente_total_monthly` | currency, €/month, 500–3,000 | 1,000 [R8 §2.2](#frlib-dependance-r8) |
| `partial_ratio` | fraction of the total *rente* | 0.50 [S1] [S2] [S7] [S8] [R12 §1.2.1](#frlib-dependance-r12) |
| `capital_option` | bool | true [S1 §1.1.2.2c] |
| `capital_amount` | currency, € | 3,500 [S1 §1.1.2.2c] |
| `premium_monthly` | currency, €/month at issue | 75 [R8 §2.2](#frlib-dependance-r8) |
| `premium_mode` | enum {monthly, quarterly, half_yearly, annual} | monthly [S1 §1.2.2] |
| `carence_accident_months` | int | 0 [S1 §1.1.5] |
| `carence_illness_months` | int | 12 [S1 §1.1.5] |
| `carence_neuro_months` | int | 36 [S1 §1.1.5] |
| `franchise_months` | int | 3 [S1 §4.3.1.2] [S7 §4.2.1] |
| `reduction_qualifying_years` | int | 8 [S1 §1.3] [S2] [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12) |
| `couple_discount` | bool | false **[std]** (spec footnote 11) |
| `status` | enum {autonomous, reduced, partial, total} | autonomous |
| `claim_duration_months` | int (in-claim cells only) | 0 |
| `years_paid` | int (reduced cells only) | 0 |

The **[std]** marks in the Example column are base-cell picks, each explained in
`product-spec.md` footnote 2 (entry age, sex, cover, *rente* and *capital* levels); every
contractual value in the table carries its own citation there. Everything not marked [std]
is contractual and cited in place.

`premium_monthly` is an **input, not a computed quantity**. No French insurer publishes a
general individual LTC rate table; the only published scale found is CNP Banque de France
annexe 1, for a group product on a four-rung severity ladder (2, 3, 4 and 5-or-6 AVQ of 6)
sold across five subscribed coverage levels [S5 arts. 13, 16, 17, annexe 1], and no
retrieved document discloses a technical rate, a loading or a profit-sharing rule. The base cell's
75 €/month is the CCSF's 2013 indicative price for exactly this cover at entry age 70
[R8 §2.2](#frlib-dependance-r8). Its shape is corroborated at two other points on the same list — 35 €/month at
50 and 50 €/month at 60 [R8 §2.2](#frlib-dependance-r8) — and by the CNP scale's age gradient, which rises about
**3.4×** between age 50 and age 74, an average of about 5.2% per year of entry age
[S5 annexe 1]. An in-force portfolio also needs claims-in-payment cells, with
`claim_duration_months` and the *rente* amount in payment as model-point attributes, and
paid-up cells with `years_paid`.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_auto(t)` | Probability autonomous, in force, premium-paying, full guarantee, at the start of month `t`; `pols_auto(0) = 1` | monthly |
| `pols_red(t)` | Probability autonomous, in force, **paid-up** after *mise en réduction*: no premium, reduced *rente totale* only, no *capital*, no assistance, no further *revalorisation* of the guarantee | monthly |
| `pols_part(t, z)` | Probability in *dépendance partielle* at start of month `t`, `z` months since first recognition | monthly, two-dimensional |
| `pols_tot(t, z)` | Probability in *dépendance totale*, same duration index; a separate ledger `pols_totr(t, z)` carries lives that entered from `pols_red` and so hold a reduced *rente* | monthly, two-dimensional |
| `pols_if(t)` | `pols_auto + pols_red + Σ_z pols_part + Σ_z pols_tot + Σ_z pols_totr` | derived |
| `G(y)` | Guaranteed *rente totale* in policy year `y`, before claim | at anniversaries |
| `CAP(y)` | Guaranteed *capital d'équipement* in policy year `y` | at anniversaries |
| `P(y)` | Monthly premium in policy year `y` | at anniversaries |
| `R_T(t, z)`, `R_P(t, z)` | *Rente* in payment for the cohort at duration `z` | at anniversaries |
| `cum_prem(t)` | Premiums actually paid per policy up to and including the start of month `t` — the *contre-assurance* refund base | monthly |
| `n_P(t)`, `n_T(t)`, `n_A(t)` | Entrants into *partielle*, into *totale* direct from autonomy, and aggravations *partielle* → *totale* | monthly |
| `carence_exit(t)` | Memberships terminated because dependence arose inside the *carence* for a cause not yet covered | monthly |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

**Three absences are product facts, not gaps.** There is **no account value and no
surrender value** [S1 §7.3] [S11], so no `cv_pp` exists and lapse before eight years
carries no cash flow at all. There is **no death benefit** on the composite — the optional
*Capital décès* is out of scope [S1 §1.1.4.1] — so `claims_death` does not exist. And there
is **no maturity**: the cover is *viagère* [S1 §1.1.5] [S5 art. 8].

`pols_red` is the one state a naive model omits, and omitting it is a first-order error:
lapse from year 8 does **not** release the liability, it converts it into a smaller one
that keeps running for life.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; from the spec)

| Input | Value | Basis |
|---|---|---|
| *Rente totale* | `G(1)` = 1,000 €/month, monthly in arrears while the state persists | [S1 §4.3.1.2] [S5 art. 16]; amount **[std]**, price-paired [R8 §2.2](#frlib-dependance-r8) |
| *Rente partielle* | 50% of the *rente totale*; the two are mutually exclusive | [S1] [S2] [S7] [S8] [R12 §1.2.1](#frlib-dependance-r12) |
| *Capital d'équipement* | 3,500 €, once per membership, on first entry into either state, no *franchise*; extinguished on payment | [S1 §1.1.2.2c, §4.3.2.1] [S2] [S5 art. 17]; no-*franchise* pick **[std]** [S10] |
| *Carence* | 0 / 12 / 36 months by cause; a claim inside it **terminates the membership and refunds all premiums paid** | [S1 §1.1.5, §1.1.4.2c] [S2] [S3] [S5 art. 7] [S7 §3.2]; *contre-assurance* [R12 §3.2.1](#frlib-dependance-r12) |
| *Franchise* | 3 months absolute from recognition, so the cohort recognised at end of month `s` is first paid at end of month `s + 4` | [S1 §4.3.1.2] [S7 §4.2.1] [S8]; monthly reading **[std]**, corroborated by [S2] |
| Premium | `P(1)` = 75 €/month, in advance, payable **for life** until recognition | [R8 §2.2](#frlib-dependance-r8); *viagère* form [S1 §1.2.1] [S5 art. 21] [S7 §4.4] |
| Premium *exonération* | From the premium due date following **recognition** — not from the start of *rente* payment | [S1 §1.2.4] [S4] [S5 art. 21] [S6 art. 18] |
| Reduction | From 8 full consecutive years of premiums; reduced *rente totale* only, no *capital*, no further *revalorisation*, assistance ends | [S1 §1.3] [S2] [S5 art. 24.2] [S7 §4.6] [R12 §1.2.1](#frlib-dependance-r12); composite **[std]** (spec footnote 12) |
| Reduction scale `c(n)` | The CNP Banque de France *barème*, 25% at 8 years rising to 70% at 30 | [S5 annexe 2]; re-based to 8 years **[std]** (spec footnote 13) |
| Surrender value | None; lapse before 8 years pays nothing | [S1 §7.3] [S11] |

Footnotes to the **[std]** entries in this table, none of which is a free choice:

1. `G(1)` = 1,000 €/month is a base-cell pick inside the sourced 500–3,000 € band
   [S1 §1.1.2.2a], chosen because it is the cover for which the only age-graded French price
   point exists [R8 §2.2](#frlib-dependance-r8) (spec footnote 2). The observed market range across insurers is
   200–4,000 €/month (spec footnote 6).
2. The *capital d'équipement* is paid with **no *franchise***, which only Generali states in
   terms [S10]; no other retrieved document separates the *capital*'s *franchise* from the
   *rente*'s (spec footnote 9). The choice moves one one-off payment by three months.
3. The **monthly reading of the three-month *franchise*** — three instalments dropped, the
   cohort recognised at end of month `s` first paid at end of month `s + 4` — is a
   standardization of "le 91e jour" onto a monthly grid [S1 §4.3.1.2] [S7 §4.2.1]. It is
   corroborated rather than assumed: Antarius restores exactly three instalments at the
   first payment [S2]. The alternative reading, paying at `s + 3`, would recover one
   instalment per claim and raise lifetime *rente* cost by roughly a third of the 7.09% the
   whole *franchise* is worth (see *Key sensitivities*).
4. The reduction composite — *totale* only, no *capital*, no further *revalorisation* — and
   the re-basing of the CNP *barème* from a 5-year to an 8-year qualifying period are spec
   footnotes 12 and 13; the observed range of qualifying periods is 5 to 8 years across the
   retrieved contracts, and the CNP scale is the only one published.

### (b) Insurer-discretionary current elements

This class is **not** thin on this product — it is where the economics live, and every item
in it is undisclosed.

| Input | Snapshot value | Basis |
|---|---|---|
| *Revalorisation des garanties* `g_G` | 1.0% per policy year, applied to `G`, to `CAP` **and to the premium in the same proportion** | mechanics [S1 §1.2.3] [S5 art. 21] [S7 §3.4]; rate **[std]** (1) |
| *Revalorisation des rentes en service* `g_S` | 1.5% per policy year, applied to every *rente* in payment regardless of how long it has been in payment | mechanics [S1 §4.3.1.3] [S5 art. 15] [S7 §4.2.3]; rate **[std]** (1) |
| Tariff revision `r(y)` | 0% in policy years 1–5, 1.5% per year from year 6; hard cap 10% per year excluding *revalorisation* | cap [S7 §4.4]; path **[std]** (2) |
| *Revalorisation* of a reduced guarantee | None | [S7 §4.6] |
| Technical rate, loadings, profit-sharing | Not disclosed in any retrieved document; not modeled | [R12 §3.2.1](#frlib-dependance-r12) parameterises `r`, `g`, `θ` symbolically without values |

1. Two rates, deliberately different. Setting `g_G = g_S` makes the amount in payment
   depend only on the current policy year and collapses two ledgers into one — which hides
   a capability the contract requires, because the two indexations are governed by
   different clauses and, at CNP and Suravenir, by different external references (civil and
   military pension rates, or the AGIRC point) [S5 arts. 15, 21] [S7 §3.4, §4.2.3]. There
   is **no observed range**: no retrieved document states a rate actually served. The CCSF
   warns that a *rente* promised fifteen or twenty years ahead can be materially eroded at
   2% average inflation [R8 §3.3](#frlib-dependance-r8), which is the direction of the risk when `g_S` is below
   inflation, as it is here.
2. **A real tariff revision is a management action, not a projected assumption.** The
   column exists so the capability is testable; the base path is arbitrary inside the 0–10%
   band [S7 §4.4]. See spec footnote 10.

### (c) Behavioral / experience assumptions (modeler's view)

**Healthy-life mortality [std].** No French mortality rate was quoted in the research file,
and the homologated tables — TH 00-02 / TF 00-02 for non-annuity business [REG-R22], TGH05
/ TGF05 for annuities [REG-R21] — are cited by name and arrêté but not reproduced by this
library [REG-R23]. What is shipped instead is a **[std]** proxy into which **no retrieved
datum enters**. INSEE publishes the only freely redistributable French mortality series, and
it is what a production implementation would graduate here [REG-R24]; this table is not read
off it. It is a two-parameter Gompertz force,

    mu_H(x) = B x c^x,    B = 5.2321459244e-06,  c = 1.11704543
    mort_rate(x) = 1 - exp(-mu_H(x))

fitted to the two **[std]** anchors `mort_rate(60) = 0.00400` and `mort_rate(90) = 0.10500`
— shaped like a French female population table, with no sourced value behind either anchor.
The shipped `mort_table.csv` records that construction in a `provenance` column on every
row — the formula, both anchors, and that the table is **not** a copy of any homologated
table. Resulting rates: 0.01205 at 70, 0.02087
at 75, 0.03601 at 80, 0.06179 at 85, 0.10500 at 90, 0.17546 at 95, 0.28506 at 100. Above
age 109 the rate is forced to 1 **[std]**.

**State mortality, and why it is not flat.** A dependent life's mortality is far heavier
than a healthy life's at the same age, and this is the largest single lever on the
liability. No impaired-life table for either French dependence state exists in any retrieved
source. The model applies proportional hazards on the force:

    mu_P(x) = k_P x mu_H(x),   k_P = 1.75  [std]
    mu_T(x) = k_T x mu_H(x),   k_T = 4.27  [std, calibrated]

`k_T` is **calibrated, not guessed**: the CCSF reports a mean duration of receipt of the
allocation for heavy dependents (GIR 1–2) of about **three years**, with mean age at onset
of total dependence about 78 for men and **84 for women** [R9 §2](#frlib-dependance-r9). Setting `k_T = 4.27`
makes the model's own expected sojourn in *dépendance totale*, entered at exact age 84,
equal **2.9989 years**. `k_P = 1.75` has **no such anchor** and no observed range: it must
exceed 1, because GIR 3–4 lives carry excess mortality, and sit well below `k_T`; at 1.75
the expected sojourn in *dépendance partielle* entered at age 82, ending in death or
aggravation, is **3.14 years**, the same order of magnitude as the 29.2-month mean duration
of APA receipt DREES reports across all GIRs [R7] and the 2.3–3.2-year expected APA
durations among beneficiaries in [REG-R25]. Resulting annual probabilities at 85: healthy
0.06179, *partielle* 0.10562, *totale* 0.23841.

**Aggravation *partielle* → *totale* [std].** `i_A = 0.20` per year, flat in age. There is
**no public transition law**: [R12 §3.1.2](#frlib-dependance-r12) models no such transition at all. The value is
set so that the sojourn in *partielle* is about three years (above). Its coupling with
incidence is set out under the identity below and is the least obvious property of this
model.

**Prevalence — the public curve [std].** What is published is APA **prevalence** by age and
sex. From DREES at end 2023 [R7]: 7.2% of people aged 60 or over receive APA, 9.1% of women
against 4.8% of men, 70% of beneficiaries being women; the rate is **2.3%** up to age 79,
**17%** between 80 and 89 (20% of women, 13% of men), **35%** at 85 or over, and about half
the population from 90 (54% of women, 40% of men); departmental dispersion of the 60+ rate
runs 3.3% to 11.3%. CNSA confirms the same order at December 2022 — 1.3 million
beneficiaries, 7.2% of an estimated 18.4 million people aged 60 and over [REG-R26]. The
model fits a logistic in attained age to the two **female** rates, at representative ages
84.5 (the midpoint of the 80–89 band) and 93 (an approximate mean age of the 90-and-over
group), both **[std]** picks:

    prev(x) = prev_ceil / (1 + exp(-beta x (x - x_mid)))
    prev_ceil = 0.90 [std],  beta = 0.195086,  x_mid = 90.921605

so `prev(84.5) = 0.20` and `prev(93) = 0.54` by construction, and `prev(70) = 0.014942`,
`prev(80) = 0.095538`, `prev(90) = 0.409655`, `prev(100) = 0.769131` by extrapolation. As
in every logistic fit of this kind the curve has **three parameters and two anchors**, and
the unidentified one is `prev_ceil`, which governs the tail — the region where the claims
are. Two checks against rates the fit did *not* use, weighting each age by survivorship on
the [std] mortality above: the mean of `prev` over ages 60–79 comes out at **2.15%** against
the sourced 2.3% [R7], and over 85 and above at **41.7%** against the sourced 35% [R7]
(which is an all-sex rate, so a female-anchored curve should sit above it). Over the whole
60+ range the curve gives **11.0%** against the sourced 9.1% for women [R7] — an overstate
of about a fifth, because survivorship weighting from age 60 is not the real age structure
of the French 60+ population, which is younger. **APA is not available below age 60**
[R2 art. R. 232-1](#frlib-dependance-r2), so the curve has no anchor at all under 60 and every issue age below 60
in the 40–75 band runs on pure extrapolation.

**From public prevalence to insured prevalence [std].** Public prevalence is APA take-up on
GIR 1–4. Insurer definitions are stricter, and the *notice* says so [S5 art. 13]
[S6 art. 21.1]. Two sourced anchors bound the haircut. First, the GIR composition of APA
beneficiaries at end 2023 — at home 2% / 18% / 22% / 58% and in establishments 13% / 44% /
19% / 24%, on 815,800 and 549,000 beneficiaries [R7] — gives a weighted **GIR 1–2 share of
34.9%** and a GIR 3–4 share of **65.1%**. Second, the market's own count: **44,200** *rentes*
in payment on sole-and-principal-guarantee contracts against about **1.39 million** people
covered under such contracts (58% of the 2.4 million covered by insurance undertakings)
gives an **insured "in *rente*" prevalence of about 3.2%** [R10 §2.3](#frlib-dependance-r10) [R13 p6](#frlib-dependance-r13) [REG-R28],
against an APA prevalence of 7.2% of the 60-and-over population [R7] [REG-R26] — a ratio of
about **0.44**, on populations whose age structures are not published and are certainly not
the same. The model therefore sets

    prev_T(x) = s_T x prev(x),   s_T = 0.30  [std]
    prev_P(x) = s_P x prev(x),   s_P = 0.15  [std]

with `s_T + s_P = 0.45` against the 0.44 the market count implies. `s_T = 0.30` sits just
below the sourced GIR 1–2 share of 34.9%, which is the direction "the insurer is not bound
by the public decision" points. `s_P = 0.15` sits far below the GIR 3–4 share of 65.1%,
because a 3-of-5-AVQ *partielle* trigger [S1 §2.2] is far stricter than GIR 3–4 — and the
one contract that requires both grids at once equates its 3-of-5 tier with GIR **1–3**, not
GIR 3–4 [S1 §2.2]. Holding the shares constant across ages is a standardization with a known
direction of error: severity mix worsens with age (57% of establishment beneficiaries are
GIR 1–2 against 20% at home [R7]), so the model **understates** *totale* prevalence at old
ages and overstates it at young ones. For `trigger_grid = avq6` the shares should be scaled
**down** and for `aggir` **up**, by amounts no retrieved document supports; the shipped
`severity_share_table.csv` carries all three rows and the two non-base rows are **[std]**
with no anchor whatever.

**The prevalence-to-incidence identity.** With `pi_P`, `pi_T`, `pi_H = 1 − pi_P − pi_T` the
proportions of the *living* population in each state, `i_P`, `i_T` the forces of entry from
autonomy, `i_A` the force of aggravation and `mu_H`, `mu_P`, `mu_T` the forces of mortality,
differentiating along the age axis gives, with `mubar = mu_H·pi_H + mu_P·pi_P + mu_T·pi_T`:

    i_P(x) = [ pi_P'(x) + (i_A + mu_P) x pi_P - pi_P x mubar ] / pi_H
    i_T(x) = [ pi_T'(x) - i_A x pi_P + mu_T x pi_T - pi_T x mubar ] / pi_H

with `pi_G' = s_G · beta · prev · (1 − prev/prev_ceil)`. This is an identity, not an
approximation, and it has three properties an implementation must respect. **The mortality
terms are not refinements**: a rising prevalence understates incidence because the
dependent population is simultaneously being drained by its own excess mortality, so
dropping `mu_T · pi_T` understates `i_T`. **`i_A` and `i_T` are not independent inputs**:
raising the aggravation force lowers the direct-to-*totale* incidence, because the stock of
*totale* lives is pinned by the assumed prevalence. And **`i_P` can go negative at extreme
ages**, where the prevalence slope flattens while excess mortality does not; the model
floors both rates at zero **[std]**, which does not bind on the female basis inside the
projection and binds at attained age 109 on the male one.

Resulting annual forces on the [std] basis, and the monthly probabilities
`i_m = 1 − exp(−i/12)`:

| Attained age | 70 | 75 | 80 | 85 | 90 | 95 | 100 |
|---|---|---|---|---|---|---|---|
| `i_P` | 0.000904 | 0.002365 | 0.005961 | 0.013650 | 0.025599 | 0.035422 | 0.034902 |
| `i_T` | 0.000593 | 0.001823 | 0.005704 | 0.017325 | 0.048116 | 0.118892 | 0.262330 |

The gradient from 70 to 90 is a factor of 28 for `i_P` and **81** for `i_T`, and `i_T`
overtakes `i_P` between ages 80 and 85 — the severity mix worsening with age, arriving here
through the mortality terms of the identity rather than through the constant severity
shares, which cannot produce it.

**The stationary-population assumption [std].** The cross-sectional APA rate by age is read
as the prevalence path a cohort will follow. It is not: the CCSF projects 4 million seniors
in loss of autonomy in 2050, 16.4% of the 60+ against 15.3% in 2015, with severe loss of
autonomy at 4.3% against 3.7% [R9], and take-up at a given age has been falling [R7]. Two
trends in opposite directions, neither modeled.

**Cause mix for the *carence* [std].** accident 10% / other illness 55% / neurological or
psychiatric 35% (spec footnote 8), giving a *carence* factor `S(t)` of **0.10** in policy
year 1, **0.65** in years 2 and 3, and **1.00** thereafter — the `S1 ≤ S2 ≤ S3 ≤ S4 = 100%`
shape [R12 §3.2.1](#frlib-dependance-r12) asks for. No observed range.

**Lapse [std].** No French LTC persistency study is public. The table is anchored on one
market fact: individual memberships fell **9.9%** in 2024 on **28,400** new subscribers of
which 82% individual [R10 §2.3](#frlib-dependance-r10) [REG-R28], so gross exits from the individual book —
deaths, claim entries and lapses together — ran at roughly 11% of the opening portfolio.
A lapse table of 3%–8% leaves the balance for mortality and incidence.

| Policy year | 1 | 2 | 3–5 | 6–10 | 11+ |
|---|---|---|---|---|---|
| `lapse_rate` **[std]** | 8% | 6% | 5% | 4% | 3% |

`lapse_rate_mth(t) = 1 − (1 − lapse_rate(y))^(1/12)`. Lapse applies to `pols_auto`
**only**: lives in a recognised state pay no premium [S1 §1.2.4] and lives in `pols_red`
pay none either, so neither can lapse for non-payment, and with no surrender value there is
nothing to surrender for [S1 §7.3].

**Expenses (all levels [std]).**

| Input | Value | Note |
|---|---|---|
| Acquisition | 150 € per policy at `t = 0` | **[std]** |
| Maintenance | 3.00 € per policy per month on `pols_if`, inflating 1.5% p.a. at each anniversary | **[std]** |
| Assistance | 1.20 € per policy per month on `pols_if − pols_red`, inflating 1.5% p.a. | **[std]**; the base excludes reduced lives because *mise en réduction* ends the assistance benefits [S1 §1.3] [S5 art. 24.2] |
| Claim adjudication | 250 € per entrant into either state | **[std]**; the AMED file, the *médecin-conseil* ruling within 45 working days, and the medical arbitration procedure [S5 arts. 19–20] [S6 arts. 23–24] |
| *Rente* handling | 10 € per instalment paid | **[std]**; annual proof of life and of the persisting state [S1 §4.3.1.2] [S6 art. 23] |
| Expense inflation | 1.5% p.a. | **[std]** |

**There is no observed range for any expense level**: no retrieved document — *notice*,
IPID, product page or dissertation — discloses an expense assumption, a loading or a
commission rate for this product, and [R12 §3.2.1](#frlib-dependance-r12) parameterises the loadings `r`, `g` and
`θ` symbolically without values. The Note column above is each row's whole rationale. Only
two structural facts are sourced and they are respected: assistance ends on *mise en
réduction* [S1 §1.3] [S5 art. 24.2], so its base excludes `pols_red`; and claim adjudication
is a real, medically supervised process with a 45-working-day deadline and an arbitration
route [S5 arts. 19–20] [S6 arts. 23–24], so it carries a per-claim cost an order of
magnitude above the per-instalment one.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy month, 0-based: `t = 0, 1, …, proj_len − 1`; `y(t) = floor(t/12) + 1`; `age(t) = entry_age + floor(t/12)` |
| `G(y)`, `CAP(y)`, `P(y)` | guaranteed *rente totale*, *capital*, monthly premium in policy year `y`; `G(1) = 1,000`, `CAP(1) = 3,500`, `P(1) = 75` |
| `g_G`, `g_S`, `r(y)` | *revalorisation* of guarantees, of *rentes en service*, tariff revision: 0.010 / 0.015 / 0 then 0.015 **[std]** |
| `rho` | partial/total *rente* ratio, 0.50 |
| `S(t)` | *carence* factor: 0.10, 0.65, 1.00 **[std]** |
| `fr` | *franchise* in months, 3; a cohort is paid when `z ≥ fr + 1 = 4` |
| `q_H(t)`, `q_P(t)`, `q_T(t)` | monthly mortality of autonomous, *partielle*, *totale* lives: `1 − (1 − mort_rate(age))^(k/12)` with `k` = 1, `k_P`, `k_T` |
| `i_Pm(t)`, `i_Tm(t)`, `i_Am` | monthly entry and aggravation probabilities, `1 − exp(−i/12)` |
| `w(t)` | monthly lapse, applied to `pols_auto` only |
| `c(n)` | reduction coefficient at `n` completed years of premiums; 0 below 8 |
| `e(y)`, `a(y)`, `ec_adj`, `ec_ren` | maintenance, assistance, adjudication and *rente*-handling expense **[std]** |

**Dimensional check.** `prev`, `pi_P`, `pi_T` are dimensionless **proportions of a living
population**; `i_P`, `i_T`, `i_A`, `mu` are **rates per year**, and `beta` carries units of
1/year, which is why `pi_G' = s_G · beta · prev · (1 − prev/prev_ceil)` is a rate per year
and can be added to `pi_G · mu`, also a rate per year. `G`, `P` are € per month, `CAP` € per
event, so `G × Σ_z pols_tot` and `CAP × (n_P + n_T)` are both € per policy-month. The error
this check catches is the one that dominates this product: multiplying a published APA
prevalence — 7.2% of the 60-and-over population [R7] — by a *rente* amount as though it
were an annual claim frequency.

### The four-state chain

Write `auto = pols_auto`, `red = pols_red`. At end of month `t`, from the autonomous state,
in the order **mortality, then lapse, then incidence among the survivors** **[std]**:

    surv(t)  = auto(t) x (1 - q_H(t))
    lapse(t) = surv(t) x w(t)
    base(t)  = surv(t) - lapse(t)
    n_P(t)   = base(t) x i_Pm(t) x S(t)
    n_T(t)   = base(t) x i_Tm(t) x S(t)
    carence_exit(t) = base(t) x (i_Pm(t) + i_Tm(t)) x (1 - S(t))
    auto(t+1) = base(t) x (1 - i_Pm(t) - i_Tm(t))

so that the *carence* removes exactly the blocked fraction of incidence from the in-force
ledger and nothing else — `auto(t+1)` does not depend on `S(t)`, which is the arithmetic
statement of the fact that a *carence* claim ends the membership rather than being deferred.

From the reduced state, which carries **no partial cover and no *carence*** (eight years of
premiums have been paid):

    surv_r(t) = red(t) x (1 - q_H(t))
    n_Tr(t)   = surv_r(t) x i_Tm(t)
    red(t+1)  = surv_r(t) - n_Tr(t) + lapse(t) x 1{(t + 1) >= 12 x reduction_qualifying_years}

with the entering *rente* frozen at `G(y) × c(n)` at the reduction date and never revalued
before claim [S7 §4.6]. Implementations that cannot carry a per-reduction-cohort amount may
track `red` and the probability-weighted mean frozen *rente* instead; that is exact in
expectation because incidence does not depend on the amount.

The indicator counts the instalments already paid: with `t` 0-based, the lapse at the end of
month `t` becomes a *mise en réduction* once `t + 1` premiums are behind it, so the first
such month is `t = 12 × 8 − 1 = 95` on the base cell.

From the two dependent states, per duration cohort `z`, with the aggravated lives paid the
**partial** *rente* for the month in which they aggravate — the higher amount takes effect
from the first day of the following month [S1 §4.3.1.2]:

    part_s(t, z) = pols_part(t, z) x (1 - q_P(t))
    n_A(t, z)    = part_s(t, z) x i_Am
    tot_s(t, z)  = pols_tot(t, z) x (1 - q_T(t))
    pols_part(t+1, z+1) = part_s(t, z) - n_A(t, z)
    pols_tot(t+1, z+1)  = tot_s(t, z) + n_A(t, z)
    pols_part(t+1, 1) = n_P(t)     pols_tot(t+1, 1) = n_T(t)     pols_totr(t+1, 1) = n_Tr(t)

### Benefits

    claims_rente(t)   = rho x G_pay(t) x SUM over z >= 4 of part_s(t, z)
                      +       G_pay(t) x SUM over z >= 4 of tot_s(t, z)
                      +                  SUM over z >= 4 of Rred(z) x totr_s(t, z)
    claims_capital(t) = CAP(y) x ( n_P(t) + n_T(t) )
    refunds_carence(t) = carence_exit(t) x cum_prem(t)

`G_pay(t)` is the *rente* in payment for a cohort recognised in policy year `y_e`, namely
`G(y_e) × (1 + g_S)^(y − y_e)`; the reduced ledger carries its own frozen amounts `Rred`.
The *capital* is paid on entry from `pols_auto` only — reduced memberships lose the option
[R12 §1.2.1](#frlib-dependance-r12) — and never twice, so aggravation `n_A` produces no *capital*.

### Monthly processing order [std]

For `t = 0, 1, …, proj_len − 1`:

1. **Anniversary (start of month, `t = 12, 24, …`).** `G(y) = G(y−1) × (1 + g_G)`;
   `CAP(y) = CAP(y−1) × (1 + g_G)`; `P(y) = P(y−1) × (1 + g_G) × (1 + r(y))`; every *rente*
   in payment × `(1 + g_S)`. Reduced guarantees are **not** touched [S7 §4.6].
2. **Premium (start of month).** `premiums(t) = P(y) × pols_auto(t)` — **not**
   `× pols_if(t)`. Accumulate `cum_prem(t) += P(y)`.
3. **Expenses (start of month).** `e(y) × pols_if(t) + a(y) × (pols_if(t) − pols_red(t))`,
   plus acquisition at `t = 0`.
4. **Look up the age basis.** `age(t)`, hence `mort_rate`, `q_H`, `q_P`, `q_T`, `prev`,
   `i_P`, `i_T`, and hence `i_Pm`, `i_Tm`; `w(t)` from the policy year; `S(t)` from `t`.
5. **End of month — claims.** `claims_rente(t)` on the surviving cohorts with `z ≥ 4`;
   `claims_capital(t)` on `n_P(t) + n_T(t)`; `refunds_carence(t)`; claim expenses
   `ec_adj × (n_P + n_T + n_Tr) + ec_ren × (number of instalments paid)`.
6. **End of month — decrements and ledger roll**, per the recursions above.

### Net cash flow

    net_cf(t) = premiums(t) - claims_rente(t) - claims_capital(t)
              - refunds_carence(t) - expenses(t) - claim_expenses(t)

`net_cf` is **income-positive**. `claims_lapse(t)` is identically zero — there is no
surrender value [S1 §7.3] — and that zero is a product fact worth publishing.
`refunds_carence` is **not** a claim: it is a return of premium, and it belongs on its own
line because it is the only cash flow that runs *backwards* through the *carence*.

### Known modeling pitfalls

- **Flat mortality across states is the biggest single error available here.** Applying
  healthy-life mortality to dependent lives, while leaving the incidence basis unchanged,
  raises lifetime claims on the worked configuration by **+159.7%**. A GIR 1–2 life at 84
  dies at an annual rate of 0.216 on this basis against 0.055 for a healthy life of the same
  age. No impaired-life table exists in any retrieved source [R12 §3.1.3](#frlib-dependance-r12), which is exactly
  why the multiple is easy to leave at 1 and catastrophic to leave at 1.
- **Ignoring the *mise en réduction* turns every lapse into a full release of liability.**
  A paid-up membership keeps a reduced *rente totale* for life [S1 §1.3] [S2] [S7 §4.6]
  [R12 §1.2.1](#frlib-dependance-r12). Treating lapse from year 8 as an exit understates lifetime claims on the
  worked configuration by **4.57%**, and the ledger it drops peaks at **8.27%** of the
  original policy at month 194 (attained age 86) — the single largest state in the model
  after `pols_auto` at that duration. It is the second decrement, not the absence of one.
- ***Carence* and *franchise* are different things and a model must implement both.** The
  *carence* runs from **inception**, is cause-specific, blocks the benefit **and terminates
  the membership with a full refund of premiums** [S1 §1.1.4.2c] [S3] [S5 art. 7]
  [S7 §3.2]. The *franchise* runs from **recognition**, is three months, and only delays
  payment [S1 §4.3.1.2] [S7 §4.2.1]. Removing the *carence* raises lifetime claims by
  **+3.99%**, removing the *franchise* by **+7.09%** — different sizes and different signs
  of error if either is applied in the other's place. In policy year 1 of the worked
  configuration `refunds_carence` is **0.6141 €**, three quarters of the year's *rente* and
  *capital* claims combined (0.8071 €): during the *carence* the largest benefit-side cash
  flow is a premium refund.
- **The *franchise* is not a premium holiday.** *Exonération* runs from **recognition**
  [S1 §1.2.4] [S4] [S5 art. 21] [S6 art. 18], so a life in the three-month *franchise* pays
  no premium and receives no *rente*. Carrying the *franchise* the way an income-protection
  deferred period is carried — premium-paying, benefit-free — overstates premium income.
- **`i_A` and `i_T` are not independent.** The prevalence identity ties them: consistently
  varying `i_A` from 0 to 0.20 to 0.40 moves lifetime claims by only **+0.54% / 0 / −0.52%**,
  because the stock of *totale* lives is pinned by `prev_T`. An implementation that adds an
  aggravation rate **without re-deriving `i_T`** double-counts entries into *totale* and
  raises claims by **+0.84%** while putting the lives in the wrong state — which matters
  more than the total, because *partielle* pays half.
- **Premium income rides on `pols_auto`, never on `pols_if`.** Lives in a recognised state
  are exonerated [S1 §1.2.4] and reduced lives are paid up [S1 §1.3], so both bands pay
  nothing. Charging premium to the whole in-force block overstates premium income by the
  whole of the reduced ledger plus the whole of the claim ledger.
- **A *carence* claim is a decrement with a cash flow, not a suppressed claim.** Modelling
  the *carence* as a multiplier on incidence alone leaves the terminated membership in force
  and omits the refund [R12 §3.2.1](#frlib-dependance-r12). Both errors run the same way: they overstate the
  liability at the front end and the premium income behind it.
- **The *capital d'équipement* is paid once per membership, not once per state.** A life
  that takes it on entering *partielle* takes nothing further on aggravating
  [S1 §4.3.2.1] [S2] [S4] [S5 art. 17]. Paying it again on `n_A` inflates capital claims by
  the whole aggravation flow.
- **Two indexations, two ledgers.** `g_G` moves the guarantee and the premium; `g_S` moves
  the *rente* in payment; the reduced guarantee moves with neither [S1 §1.2.3] [S5 art. 21]
  [S7 §3.4, §4.6]. Collapsing them into one rate happens to work only when `g_G = g_S`, and
  the base configuration sets them different so that a test can tell.
- **The duration index runs from first recognition.** A cohort that aggravates keeps its
  `z`, so it does not serve a second *franchise* **[std]**. Restarting `z` on aggravation
  drops three instalments per aggravated life.
- **APA prevalence is a prevalence, and it is public.** It is not an incidence, and it is
  not the insurer's definition [S5 art. 13] [S6 art. 21.1]. Both conversions — the two-term
  identity and the severity shares — are explicit **[std]** steps, and quoting a model
  incidence rate as though it carried the [R7] provenance of the two prevalence anchors
  misrepresents where the evidence stops.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no French LTC
policyholder-behaviour study was retrieved.

- **Lapse stops at recognition, and again at reduction.** Once the state is recognised the
  premium is exonerated [S1 §1.2.4] [S5 art. 21], so there is no premium to miss; once the
  membership is reduced there is no premium either [S1 §1.3]. `w(t)` therefore applies to
  `pols_auto` alone. On the worked configuration the reduced and dependent bands together
  are **44.6%** of the in-force block at attained age 90 — `pols_auto` 0.133256, `pols_red`
  0.070326, `pols_part` 0.010324, `pols_tot` 0.020960 and `pols_totr` 0.005782 out of
  `pols_if` 0.240648 — so at that age fewer than three in five surviving memberships are
  still paying anything. The two *totale* ledgers are separate columns in `result_cf()` and
  must be added by hand: 0.020960 + 0.005782 = 0.026742 is the whole *totale* band, and it is
  the reduced-entry ledger `pols_totr` that a naive three-state model loses entirely.
- **Lapse is genuinely a decision to walk away from everything.** With no surrender value
  [S1 §7.3] and a *fonds perdu* design [S11], a lapse before eight years destroys the whole
  accumulated value. That is the CCSF's consumer complaint [R8 §4.2](#frlib-dependance-r8) and it is also the
  reason the [std] lapse table is set below what one would use on a savings contract.
- **Premium-shock lapse [std] (optional module, off in the base run).** The member may
  refuse a tariff revision by resiliating within two months of notification, with a possible
  *mise en réduction* at the same date [S1 §1.2.3]. The module multiplies lapse in a revision
  year by `M_rev(y) = 1 + 3 × max(0, r(y) − 0.02)`, so a revision at the 10% cap [S7 §4.4]
  gives `M_rev = 1.24`. It is off in the base run because `r(y) ≤ 0.015` there, and it is
  the only place a projected repricing feeds back into the block.
- **Anti-selection sits at the front door.** Underwriting is two-stage and the
  *médecin-conseil* sets the terms [S5 art. 3] [S7 §2.2]; increases in cover are
  re-underwritten and restart the *carence* [S1 §1.1.3] [S7 §3.3]; and the *carence* itself
  is a selection device with the sharpest possible teeth — a claim inside it voids the
  membership entirely [S1 §1.1.4.2c]. No selection loading is applied at issue.
- **Cover changes are held at zero.** Increases and decreases are contractually available
  [S1 §1.1.3] [S7 §3.3] [R12 §1.2.1](#frlib-dependance-r12) but they change the guarantee, the premium and the
  *carence* together, which is a new model point rather than a decrement.
- **Claim behaviour is not policyholder behaviour here.** The insured is often no longer
  able to claim, which is why every contract and the CCSF urge that relatives be told the
  contract exists [S7 "Quelques conseils"] [R8 §4.4](#frlib-dependance-r8). Late notification is real — the
  recognition date cannot precede the date the insurer received the claim [S6 arts. 23–24] —
  and the model does **not** carry it, so its claim dates are the earliest defensible ones.

---

## Worked example

**Configuration.** Female, entry age 70 (*différence de millésimes*), *formule* Dépendance
Totale et Partielle on the 5-act AVQ grid [S1 §2.2]; `rente_total_monthly` = 1,000 €,
`partial_ratio` = 0.50, `capital_amount` = 3,500 €, `premium_monthly` = 75 € [R8 §2.2](#frlib-dependance-r8);
*carence* 0 / 12 / 36 months by cause; *franchise* 3 months; reduction from 8 years;
`proj_len = 12 × (110 − 70) = 480` months, so the last projected month is `t = 479`.
Undiscounted. All sixteen rows below sit in policy years 1 and 2, so two sets of rates
drive them.

Assumption values used, every one of them:

- **Mortality [std].** `mort_rate(70) = 0.0120506`, `mort_rate(71) = 0.0134515` from the
  Gompertz proxy. Monthly: `q_H = 0.0010098056` at 70 and `0.0011279321` at 71;
  `q_P = 1 − (1 − q)^(1.75/12)` = `0.0017664906` and `0.0019730461`;
  `q_T = 1 − (1 − q)^(4.27/12)` = `0.0043047564` and `0.0048073955`.
- **Lapse [std].** Policy year 1, 8%: `w = 1 − 0.92^(1/12) = 0.0069243826`. Policy year 2,
  6%: `w = 0.0051430128`.
- **Prevalence [std].** `prev(70) = 0.01494159`, `prev(71) = 0.01809552`, from the logistic
  pinned to the sourced female APA rates at 84.5 and 93 [R7].
- **Severity shares [std].** `s_P = 0.15`, `s_T = 0.30`, so at age 70
  `pi_P = 0.002241239`, `pi_T = 0.004482477`, `pi_H = 0.993276284`.
- **Incidence**, from the two-term identity with `k_P = 1.75`, `k_T = 4.27`, `i_A = 0.20`
  **[std]**: at 70, `mubar = 0.012321875` against `mu_H = 0.012123789`, giving
  `i_P = 0.000904237` and `i_T = 0.000592504`, hence `i_Pm = 0.0000753503` and
  `i_Tm = 0.0000493741`; at 71, `i_Pm = 0.0000914562` and `i_Tm = 0.0000616541`.
  `i_Am = 1 − exp(−0.20/12) = 0.0165285462`.
- **Carence [std].** `S = 0.10` for `t = 0…11`, `S = 0.65` for `t = 12…35`.
- **Revalorisation [std].** At `t = 12`: `G = 1,010.00`, `CAP = 3,535.00`,
  `P = 75 × 1.01 × 1.00 = 75.75`; *rentes* in payment × 1.015, so a year-1 cohort is paid
  **1,015.00** (total) or **507.50** (partial) from `t = 12`.
- **Expenses [std].** Acquisition 150 € at `t = 0`; maintenance 3.00 €/month and assistance
  1.20 €/month in policy year 1, both × 1.015 in year 2; adjudication 250 € per entrant;
  *rente* handling 10 € per instalment.

`pols_red(t) = 0` throughout the window — the first reduction is at `t = 95` — and the
`expenses` column below is the **combined** expense of the month: maintenance, assistance,
claim adjudication, *rente* handling, and acquisition at `t = 0`. The model publishes
`expenses` and `claim_expenses` as two columns of `result_cf()`.

| t | `pols_auto` | `pols_part` | `pols_tot` | `premiums` | `claims_rente` | `claims_capital` | `refunds_carence` | `expenses` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 0.000000 | 0.000000 | 75.0000 | 0.0000 | 0.0433 | 0.0084 | 154.2031 | −79.2548 |
| 1 | 0.991949 | 0.000007 | 0.000005 | 74.3962 | 0.0000 | 0.0430 | 0.0166 | 4.1693 | 70.1673 |
| 2 | 0.983963 | 0.000015 | 0.000010 | 73.7972 | 0.0000 | 0.0426 | 0.0247 | 4.1358 | 69.5942 |
| 3 | 0.976041 | 0.000022 | 0.000015 | 73.2031 | 0.0000 | 0.0423 | 0.0326 | 4.1025 | 69.0257 |
| 4 | 0.968183 | 0.000029 | 0.000020 | 72.6137 | 0.0087 | 0.0419 | 0.0404 | 4.0697 | 68.4530 |
| 5 | 0.960388 | 0.000035 | 0.000025 | 72.0291 | 0.0174 | 0.0416 | 0.0481 | 4.0371 | 67.8849 |
| 6 | 0.952656 | 0.000042 | 0.000030 | 71.4492 | 0.0260 | 0.0413 | 0.0557 | 4.0048 | 67.3215 |
| 7 | 0.944987 | 0.000048 | 0.000035 | 70.8740 | 0.0346 | 0.0409 | 0.0631 | 3.9727 | 66.7627 |
| 8 | 0.937379 | 0.000055 | 0.000041 | 70.3034 | 0.0431 | 0.0406 | 0.0705 | 3.9409 | 66.2083 |
| 9 | 0.929832 | 0.000061 | 0.000046 | 69.7374 | 0.0516 | 0.0403 | 0.0777 | 3.9093 | 65.6585 |
| 10 | 0.922346 | 0.000066 | 0.000051 | 69.1759 | 0.0600 | 0.0399 | 0.0847 | 3.8780 | 65.1132 |
| 11 | 0.914920 | 0.000072 | 0.000057 | 68.6190 | 0.0684 | 0.0396 | 0.0917 | 3.8470 | 64.5723 |
| 12 | 0.907554 | 0.000078 | 0.000062 | 68.7472 | 0.0779 | 0.3173 | 0.0472 | 3.8930 | 64.4119 |
| 13 | 0.901730 | 0.000130 | 0.000099 | 68.3060 | 0.0863 | 0.3152 | 0.0505 | 3.8685 | 63.9855 |
| 14 | 0.895943 | 0.000181 | 0.000137 | 67.8677 | 0.0947 | 0.3132 | 0.0538 | 3.8442 | 63.5619 |
| 15 | 0.890194 | 0.000230 | 0.000175 | 67.4322 | 0.1029 | 0.3112 | 0.0570 | 3.8200 | 63.1410 |

Policy year 1 in aggregate (`t = 0…11`, all at age 70, all in policy year 1 — the strongest
single test target in this file, because it exercises the whole annual cycle on one set of
rates), with `pols_auto(12) = 0.907554`, `pols_part(12) = 0.000078`, `pols_tot(12) =
0.000062` and `pols_if(12) = 0.907694`:

| Line | Policy year 1 total |
|---|---|
| `premiums` | 861.1983 |
| `claims_rente` | 0.3098 |
| `claims_capital` | 0.4973 |
| `refunds_carence` | 0.6141 |
| `expenses` (acquisition + maintenance + assistance) | 198.2304 |
| `claim_expenses` | 0.0398 |
| `net_cf` | **661.5068** |

(The totals are sums of unrounded monthly values; the twelve displayed rows do not re-add to
them, and the year-1 `net_cf` differs by €0.0001 from the difference of the six rounded
lines above it.)

**Checks.** Three of these numbers, re-derived a different way.

*Month 0, end to end.* `pols_auto(0) = 1`, so `premiums(0) = 75 × 1 = 75.0000`. Survivors
of mortality: `1 × (1 − 0.0010098056) = 0.9989901944`. Lapses:
`0.9989901944 × 0.0069243826 = 0.0069173903`, leaving `base(0) = 0.9920728040`. Entrants:
`n_P = 0.9920728040 × 0.0000753503 × 0.10 = 0.0000074753`;
`n_T = 0.9920728040 × 0.0000493741 × 0.10 = 0.0000048983`; blocked by the *carence*,
`carence_exit = 0.9920728040 × (0.0000753503 + 0.0000493741) × 0.90 = 0.0001113621`. So
`claims_capital(0) = 3,500 × (0.0000074753 + 0.0000048983) = 0.0433`,
`refunds_carence(0) = 0.0001113621 × 75 = 0.0084`, claim expense
`250 × 0.0000123736 = 0.0031`, and `expenses(0) = 150 (acquisition) + 3.00 (maintenance) +
1.20 (assistance) + 0.0031 (claim) = 154.2031`. Hence
`net_cf(0) = 75.0000 − 0.0433 − 0.0084 − 154.2031 = −79.2548`. Roll forward:
`pols_auto(1) = 0.9920728040 × (1 − 0.0000753503 − 0.0000493741) = 0.9919490683`, printed
0.991949. Note the *carence* does not appear in that last line — the blocked lives leave the
in-force ledger exactly as the covered ones do.

*Month 4, the first *rente* instalment.* The cohorts recognised at the end of month 0 are
the only ones old enough to be paid: seeded at `z = 1` at the start of month 1, they reach
`z = 4` at the start of month 4 and are paid at its end. The partial cohort survives three
months of mortality **and** aggravation and a fourth month of mortality:
`0.0000074753 × [(1 − 0.0017664906)(1 − 0.0165285462)]^3 × (1 − 0.0017664906) =
0.000007060611`. The total ledger at `z = 4` holds the direct entrants plus the three months
of aggravated lives, and comes to `0.000005174632`. So
`claims_rente(4) = 500 × 0.000007060611 + 1,000 × 0.000005174632 = 0.0087`, against 0.0000
at `t = 3` — the *franchise* is exactly three dropped instalments, and the model pays the
fourth. Nothing else in the month-4 row moves: the *rente*-handling expense adds
`10 × 0.000012235 = 0.0001` to the expense column.

*Month 12, the *carence* step.* `base(12) = 0.90755402 × (1 − 0.0011279321) ×
(1 − 0.0051430128) = 0.90186807`. Entrants
`= 0.90186807 × (0.0000914562 + 0.0000616541) × 0.65 = 0.000089755`, so
`claims_capital(12) = 3,535.00 × 0.000089755 = 0.3173` — the jump of **8.0076×** on month 11
decomposes exactly as 6.5 × 1.227589 × 1.01 × 0.993611: the *carence* widening (0.65 / 0.10),
the age step 70 → 71 in the incidence identity, the *revalorisation* of the *capital*, and
the in-force run-off. In the same month the refund falls the other way:
`refunds_carence(12) = 0.90186807 × 0.0001531103 × 0.35 × 975.75 = 0.0472`, where
`975.75 = 12 × 75 + 75.75` is the premium actually paid to that point — down from 0.0917 a
month earlier even though incidence has risen, because only 35% of causes are still blocked.

*The `k_T` calibration.* Running the *totale* ledger alone from exact age 84 with
`q_T = 1 − (1 − mort_rate(x))^(4.27/12)` and no other decrement gives an expected sojourn of
**2.9989 years**, against the "about three years" the CCSF reports for heavy dependents
[R9 §2](#frlib-dependance-r9). At `k_T = 2.75` the same calculation gives 4.19 years and at `k_T = 3.50`, 3.50
years — the sojourn is far more sensitive to `k_T` than a first look suggests, which is why
this is a calibration rather than a pick.

**Lifetime totals for the same configuration** (undiscounted, per policy issued, over all
480 months): `premiums` 10,867.00; `claims_rente` 5,885.08; `claims_capital` 632.92;
`refunds_carence` 2.86; `expenses` 828.71; `claim_expenses` 113.18; `net_cf` 3,404.24. Claims
are **60.0%** of premiums and **65.0%** of them fall at attained age 85 or over. The reduced
ledger peaks at **0.082685** of the original policy at `t = 194` (attained age 86), and
total expected entrants into a covered state over the lifetime are **0.198** per policy
issued, receiving **6.368** *rente* instalments between them.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows. Every valuation layer below
consumes them and is cited, never reproduced.

- **Solvabilité II.** Technical provisions are a best estimate — the probability-weighted
  average of future cash flows discounted at the relevant risk-free term structure — plus a
  risk margin [REG-R4] [REG-R1] [REG-R2]. The cash flows above are exactly the input; the
  curve comes from EIOPA's monthly publication [REG-R5]. LTC sits in the **Health-SLT**
  underwriting module, life techniques applying because of the long-term commitment
  [R12 §1.1.2.1](#frlib-dependance-r12), and [R12 ch. 4](#frlib-dependance-r12) projects the SCR through incidence and longevity shocks
  combined with the contractual right to revise premiums — which is the point at which the
  tariff-revision column of section (b) stops being decoration.
- **French statutory provisions.** Art. R. 343-3 enumerates the eleven technical provisions,
  each engagement provisionable under exactly one of them, item 1 being the *provision
  mathématique* computed *including future management costs* [REG-R6]. This product
  generates a **provision pour risques croissants** on autonomous insureds — present value
  of future commitments less present value of future premiums, allowing for the
  waiting-period incidence reduction and for the counter-insurance of refunded premiums,
  computed separately for the *rente* and the *capital* — and a **provision mathématique
  des rentes** on *rentes* in payment [R12 §3.2.2](#frlib-dependance-r12). A *provision d'aggravation* for partial
  dependents who may become total exists in principle and is not used under [R12]'s
  two-guarantee model; this model produces the flow it would provide for. **The Code des
  assurances article governing the PRC was not retrieved** [R18], so none of this is cited
  to the code.
- **Mortality tables.** A tariff must use homologated tables by sex or the undertaking's own
  tables certified by an independent actuary [REG-R23]; TGH05 / TGF05 for annuities
  [REG-R21], TH 00-02 / TF 00-02 otherwise [REG-R22]. The technical-rate ceiling for a
  periodic-premium contract is the lower of 3.5% and 60% of the semi-annual average rate of
  French State borrowings [REG-R17]. None of these is used in the projection, which is
  undiscounted.
- **Reinsurance.** Quota-share treaties are usual on this risk; the Sogecap product cedes
  70% [R12 §1.2.1](#frlib-dependance-r12). The model is gross of reinsurance.
- **Professional standards.** Institut des actuaires NPA 2, *Modèles actuariels*, applies to
  any actuarial model under a principle of proportionality and covers pricing and the
  technical studies attached to new products [REG-R44]. **NPA 4, on best-estimate
  provisions in life, was not retrieved** and is [unverified] in this library.
- **IFRS 17.** Fulfilment cash flows plus a contractual service margin, effective for
  reporting periods beginning on or after 1 January 2023 [REG-R45]; the same projection
  feeds it with its own discounting and risk adjustment.

---

## Key sensitivities and model risks

In rough order of leverage on this block. Percentages are changes in undiscounted lifetime
claims (`claims_rente + claims_capital`) on the worked configuration.

1. **State mortality.** Flattening it — healthy mortality applied to dependent lives, the
   incidence basis unchanged — moves claims by **+159.7%**. Lightening `k_T` from 4.27 to
   2.75 moves them by **+9.05%** and lifts premiums 2.0%, because the identity also lowers
   `i_T`. `k_P` from 1.75 to 1.0 moves claims **+2.08%**. There is no impaired-life table
   for either state in any retrieved source, and the only anchor is a mean duration of about
   three years for heavy dependents [R9 §2](#frlib-dependance-r9).
2. **Lapse.** Turning lapse off raises claims **+78.1%** and premiums **+56.8%**. On a
   product whose claims are concentrated fifteen years out, persistency is a first-order
   assumption, and the only public anchor is a portfolio that shrank 9.9% in 2024 on 28,400
   new subscribers [R10 §2.3](#frlib-dependance-r10) [REG-R28].
3. **The severity shares.** Raising `s_T` and `s_P` by a tenth relative moves claims
   **+8.06%**; raising `s_T` alone from 0.30 to 0.35 moves them **+10.39%** and cuts
   premiums 1.2%. They are the whole of the public-to-insured translation and they are
   **[std]** against two indirect anchors — the GIR 1–2 share of APA beneficiaries [R7] and
   the market's ratio of *rentes* in payment to lives covered [R10 §2.3](#frlib-dependance-r10).
4. **The prevalence tail.** The logistic is pinned at ages 84.5 and 93 and unpinned above
   93, and **65.0%** of lifetime claims fall at attained age 85 or over. `prev_ceil = 0.90`
   is a **[std]** choice with no sourced value behind it and it is the parameter that sets
   the tail. What would fix it is not a better fit but finer data: DREES publishes the 60+
   rate by department and by broad age band [R7] but no five-year-band series was retrieved.
5. **The *franchise* and the *carence*.** Removing the *franchise* moves claims **+7.09%**,
   removing the *carence* **+3.99%**. Both are contractual and both are cheap to get wrong
   in the other's place.
6. **Revalorisation.** `g_S` compounds over a *rente* that runs for life and is the
   inflation exposure the CCSF warns about [R8 §3.3](#frlib-dependance-r8); `g_G` moves the guarantee and the
   premium together and is close to neutral on the margin. Neither rate is contractual and
   neither is published.
7. **The tariff-revision path.** Zero in the base run for the first five years by
   construction. It is the insurer's one real management lever on this product and it is
   capped at 10% a year at exactly one insurer [S7 §4.4]; treating a projected revision as
   an assumption rather than an action is the modelling error to avoid, and the
   premium-shock lapse module is off precisely because turning it on is a joint statement
   about insurer and policyholder behaviour.
8. **The aggravation rate, which is nearly neutral and easy to misread.** Consistently
   varying `i_A` over 0 → 0.20 → 0.40 moves lifetime claims by **+0.54% / 0 / −0.52%**;
   applying it *without* re-deriving `i_T` moves them **+0.84%** and misallocates lives
   between a 1,000 €/month benefit and a 500 €/month one. [R12 §3.1.2](#frlib-dependance-r12) avoids the question
   by not modelling the transition at all; this model faces it and the price is that the
   number has no external anchor.
9. **Recovery, held at zero.** The contracts provide for improvement out of a covered state
   [S1 §4.3.1.2] [S5 art. 13] [S6 art. 26] [S7 §4.2.1] and this model, like [R12 §3.1.1](#frlib-dependance-r12),
   ignores it. The error is one-directional: claims are overstated, and by an amount no
   retrieved source quantifies.
10. **The supervisor's view is missing.** No ACPR material on this product could be
    retrieved (see `product-spec.md`, *Regulatory context*), so nothing here is calibrated
    against, or checked by, a supervisory finding on pricing adequacy or provisioning
    practice.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R12]: #frlib-dependance-r12
[R18]: #frlib-dependance-r18
[R3]: #frlib-dependance-r3
[R7]: #frlib-dependance-r7
[R9]: #frlib-dependance-r9
[REG-R1]: #frlib-reg-r1
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R25]: #frlib-reg-r25
[REG-R26]: #frlib-reg-r26
[REG-R28]: #frlib-reg-r28
[REG-R4]: #frlib-reg-r4
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
