# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify the reference liability cash-flow projection model
**ADE_FR_S** for the standardized composite product defined in `product-spec.md` (same
directory). This is not any single insurer's product. [S#]/[R#] tags refer to the source
list in `sources.md`, whose numbering is carried verbatim from
`_research/assurance-emprunteur.md`; [REG-R#] tags refer to the cross-product reference
library `references/regulatory-and-actuarial-references.md` (its own frozen R1–R49
numbering). **[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter values are
identical to those in `product-spec.md`. Every name that becomes a `cells` or a CSV column
is English `lower_snake_case`; French terms of art are kept in French.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — premiums, benefit outgo
  and expenses — for a single-policy model point of French *assurance emprunteur* on a
  **monthly** grid. Reserves are not computed (see Valuation and reserve pointers).
- **What this model inherits, and where it deviates.** The death leg is the
  `temporaire_deces` chassis (`TD_FR_S`, `products/temporaire_deces/technical-notes.md`):
  the same non-annuity mortality basis — TH 00-02 / TF 00-02 with the annexed *décalage
  d'âge* [REG-R22] [REG-R23], never shipped, replaced by an INSEE-derived **[std]** proxy
  [REG-R24] — the same annual-to-monthly conversion, the same "no surrender value, so lapse
  generates no cash flow" rule, and the same income-positive `net_cf` sign convention. Four
  deviations define ADE: (i) the sum insured is not a level *capital garanti* but the
  **capital restant dû** of an amortising loan, recomputed every month from the loan's own
  parameters; (ii) the monthly grid the chassis also runs on is here forced by the product
  rather than chosen for resolution, because the benefit dominating the incapacity side is a
  monthly *échéance* and the *franchise* is counted in days; (iii) the state space is
  **healthy / ITT / IPT / dead**, the
  `income_protection` three-state chassis (`IP_UK_S`) with a fourth state and a
  duration-triggered forced transition; (iv) every guarantee carries **its own cover-end
  age**, so the decrements switch off at different times and the premium does not.
- **One head, one loan, deterministic amortisation.** A model point is **one insured life**
  with a *quotité*, on **one** fixed-rate amortising loan whose schedule the model computes.
  The states are `healthy`, `itt` (indexed by claim duration `z`), `ipt` and `dead`, with
  *résiliation* and PTIA as additional exits from `healthy`. Deliberately excluded, with
  reasons: **multi-head aggregation**, because the anti-duplication rule and the *quotité*
  interaction are a portfolio-level constraint, not a per-life cash flow [S1] [S9] [S12];
  ***perte d'emploi***, a separate module with its own *carence*, *franchise*, eligibility
  test, duration cap and decrement that no retrieved source quantifies [S1] [S8]; and **IPP
  and every partial benefit below the 66 % IPT threshold**, because the benefit shape is not
  agreed across the market — a linear ramp (N − 33)/33 at two insurers [S1] [S11] against a
  flat 50 % at three others [S5] [S9] [S10] — so one reference number would misrepresent half
  of it. *Mi-temps thérapeutique*, *garantie aide à la famille*, *invalidité AERAS* and the
  exclusion buy-backs are excluded on the same grounds.
- **Time index [std].** `t` is the **0-based policy month**: `t = 0` is the contract's first
  month, the frame is `t = 0..proj_len − 1` with `proj_len = loan_term_months` (240 in the
  base cell, so the last projected month is `t = 239`), and the contractual policy year is
  the 1-based label `y = floor(t/12) + 1`, derived from `t` and never indexed by. Month `t`
  runs from time `t` to time `t + 1`. The quantities carried at a **time point** keep their
  own 0-based index `k`, `k = 0` at adhesion: the loan balance `crd(k)`, with
  `crd(0) = capital_initial` and `crd(T) = 0`, and the state probabilities `l_h(k)`,
  `l_itt(k, z)` and `l_ipt(k)`, with `l_h(0) = 1`. Month `t` therefore **opens** on `crd(t)`
  and `l_h(t)` and **closes** on `crd(t + 1)` and `l_h(t + 1)`.
- **Timing and horizon [std].** All cover ends at the loan's contractual expiry [S1] [S9].
  Premiums arrive at the **beginning of the policy month** (BOM) from lives in `healthy`;
  the *échéance* falls at **end of month** (EOM), so `crd(t + 1)` is the principal
  outstanding immediately after the month-`t` instalment; transitions occur at EOM. Claim
  benefit for month `t` is paid at EOM to lives in a paying state at BOM `t` that have
  neither recovered nor died during the month — monthly in arrears, so a claim incepting at
  EOM `t` is first paid at EOM `t+1`. Death and PTIA benefits are paid at EOM `t` against
  `crd(t + 1)`, the instalment falling on the day of death being deemed due [S9].
- **Age and duration [std].** `age(t) = entry_age + floor(t/12)`; one insurer computes
  age by difference of calendar years [S3] and two set the rate by age at adhesion
  [S9] [S11], so the annual step is a pure convention. `z` is months since **claim payment
  inception**, i.e. since the end of the *franchise*, running `z = 1..itt_max_months` on a
  clock of its own that the policy-month index never touches; the 1 095-day cap
  [S1] [S11] [S12] gives `itt_max_months = 36`.
- **Units.** EUR. `capital_initial`, `crd` and death benefits are amounts; `echeance`, `prem`
  and monthly benefits are EUR per month; rates are probabilities per period unless labelled
  "per mille". Model points are projected on an expected basis; an in-force portfolio needs
  claims-in-payment cells carrying `status` and `claim_duration_months`.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `entry_age` | int | 52 **[std]** (spec footnote 1) |
| `sex` | enum {M, F} | M **[std]** (spec footnote 1); tariffs are sex-rated except where unisex [S3] |
| `capital_initial` | currency | 200,000 **[std]** (spec footnote 1); definition [S9] |
| `loan_rate_annual` | float (*taux nominal*; monthly rate = /12) | 0.0300 **[std]** (spec footnote 2) |
| `loan_term_months` | int | 240 **[std]** (spec footnote 1); band 1–35 years [S1] [S9] |
| `quotite` | float, 0 < q ≤ 1, 1 % steps | 1.00 **[std]** (spec footnote 1); 1 % steps [S9], ≤100 % per head [S1] [S5] [S9] [S11] |
| `premium_basis` | enum {capital_initial, capital_restant_du} | capital_initial [S9] [S11] [S13]; alternative [S2] [S7] [S8] [S10] |
| `premium_rate_annual` | float (used when `premium_basis = capital_initial`) | 0.0084 **[std]** (spec footnote 7) |
| `indemnity_basis` | enum {forfaitaire, indemnitaire} | forfaitaire [S1] [S3] [S6] [S11]; alternative [S10] |
| `income_loss_ratio` | float ≤ 1 (used when `indemnity_basis = indemnitaire`) | 1.00 **[std]** (9) |
| `franchise_days` | enum {30, 60, 90, 120, 180} | 90 [S9]; pick **[std]** (spec footnote 4) |
| `itt_max_days` | int | 1095 [S1] [S11] [S12] |
| `ipt_benefit_basis` | enum {echeance, crd} | echeance [S5] [S9] [S11]; alternative [S1] [S2] [S7] |
| `deces_end_age` | int | 85 [S9] [S11] |
| `ptia_end_age` | int | 70 [S9] [S11] |
| `itt_ipt_end_age` | int | 70 [S9] |
| `status` | enum {healthy, itt, ipt} | healthy |
| `claim_duration_months` | int (in-claim cells only) | 0 |

Occupation class and smoker status are **not** attributes. They are real tariff drivers
[S1] [S11], but no public French table is graded by them and no rate card was retrieved;
adding a column the shipped rate tables cannot serve would produce model points that do not
project.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `crd(k)` | Capital restant dû at time `k`, i.e. after the `k`-th instalment | at each instalment, deterministic |
| `echeance` | Level monthly loan instalment, capital and interest | once, at issue |
| `prem_pp(t)` | Monthly premium per policy in force | at each policy anniversary |
| `l_h(k)` | Probability in `healthy` at time `k` (alive, no claim in payment); `l_h(0) = 1` | monthly |
| `l_itt(k, z)` | Probability in ITT payment at time `k` at claim duration `z` | monthly, two-dimensional |
| `l_itt(k)` | Total ITT probability = Σ_z `l_itt(k, z)` | derived |
| `l_ipt(k)` | Probability in IPT payment at time `k` | monthly |
| `n_itt(t)` | New ITT claim-payment inceptions in month `t` (seeds `z = 1`) | monthly |
| `rec_itt(t)`, `trn_ipt(t)`, `dth_itt(t)` | Exits from ITT: recoveries, transitions to IPT, deaths in claim | monthly |
| `cap_itt(t)` | ITT mass reaching the 1 095-day assessment at EOM `t` | monthly |
| `dth_h(t)`, `ptia_h(t)`, `lapses(t)` | Exits from `healthy`: deaths, PTIA claims, *résiliations* | monthly |
| `dth_ipt(t)` | Deaths in IPT | monthly |

There is no account value, no surrender value and no unit fund: the state is the insured
population plus the deterministic loan schedule. `l_h(t) + l_itt(t) + l_ipt(t) +
Σ_{s < t} (dth_h + ptia_h + lapses + dth_itt + dth_ipt)(s) = 1` for every `t` — the states
at time `t` plus everything that has left in months `0 .. t − 1`. That identity is
`check_states()`.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; from the spec)

| Input | Value | Basis |
|---|---|---|
| Loan spine | `echeance` and `crd(k)` computed from `capital_initial`, `loan_rate_annual`, `loan_term_months` | read from the *échéancier* contractually [S1] [S5] [S9]; computed here **[std]** (spec footnote 3) |
| Décès / PTIA benefit | `crd(t + 1) × quotite`, the balance at the end of month `t` | [S1] [S5] [S9] [S10] [S11] |
| ITT / IPT benefit | `echeance × quotite`, monthly | [S1] [S9] [S11] |
| *Franchise* | 90 days, embedded in the inception basis | [S9]; pick **[std]** (spec footnote 4) |
| ITT duration cap | 1 095 days = 36 months, then a forced consolidation assessment | [S1] [S11] [S12]; consolidation ≤3 years [S10] |
| IPT threshold | Combined invalidity ≥ 66 % on the *barème croisé* | [S1] [S5] [S9] [S10] [S11] [S12] |
| Cover-end ages | Décès 85, PTIA 70, ITT/IPT 70 | Décès 85 and PTIA 70 [S9] [S11]; ITT/IPT 70 [S9] alone — MAIF ends ITT/IPT/IPP at 67 [S11]; ranges in the spec |
| Premium waiver in claim | No premium from lives in `itt` or `ipt` | [S5] [S11]; advance-and-refund elsewhere [S9] |
| Premium levelling | The premium does **not** fall when the PTIA/ITT/IPT guarantees cease | [S13] |
| Résiliation | Cancellation at any time from signature of the loan offer; no surrender value | [R1] [R3] [REG-R35] |
| Expiry | All cover and any claim in payment cease at the loan's contractual expiry | [S1] [S9] |

### (b) Insurer-discretionary current elements

Thin by construction: no *participation aux bénéfices* is credited to the individual
contract, there is no bonus and no account value, and the net-of-tax premium is guaranteed
for the whole term [S1] [S11]. What discretion exists is recorded, not projected. **Premium
revision** — one insurer revises *downward* on a risk-reducing change of life habits and may
revise the *perte d'emploi* rate only, at renewal, with three months' notice [S1]; two others
pass on tax changes [S5] [S11]; base model: no revision **[std]**. **Underwriting outcome** —
standard terms, a *surprime* and/or guarantee restrictions, or refusal [S1]; the model
projects a standard-terms life only **[std]**, the *surprime* being a rate multiplier rather
than a mechanic. One published scale does exist — the AERAS *grille de référence* states a
**capped surcharge per guarantee** for its list II pathologies [R17] — but the grid itself
was **not retrieved** here (spec, Underwriting) and its rates must not be invented; no
insurer's standard-risk rate card is public at all, so there is no base rate to multiply.
**Claim adjudication** — declines are material, 2.5 %–4.4 % on death/PTIA and 7.7 %–16.3 % on
incapacity/invalidity for external alternative contracts against 2.5 %–3.8 % and
10.2 %–12.8 % for bank group contracts [R12]; the base admits **every** claim **[std]**, and
a portfolio calibration should scale `ben_itt` and `ben_ipt` by an admission ratio. The 2025
*garantie aide à la famille* is a market undertaking, not a priced element, and is out of
scope [S9] [R12].

### (c) Behavioral / experience assumptions (modeler's view)

**No decrement, incidence or termination table for this product was retrieved.** Nothing in
the corpus gives a mortality basis, an ITT inception rate, a recovery rate or an ITT → IPT
transition rate: insurer rate cards are proprietary, the CCSF publishes tariff levels only
as chart series [R12], and the homologated mortality tables are cited by name but are not
redistributable [REG-R22] [REG-R23]. **Every rate below is therefore [std].** The tables are
shaped like the quantities a real basis would carry, so licensed tables drop in without
changing the recursions.

| Input | Reference basis | Basis tags |
|---|---|---|
| Healthy-life mortality `mort_rate(a)` | [std] proxy table below (male); female = 0.60 × male | values **[std]** (1); table names [REG-R22] [REG-R23]; data [REG-R24] |
| PTIA incidence `ptia_rate(a)` | 0.10 × `mort_rate(a)` | ratio **[std]** (2) |
| ITT inception `itt_inception_rate(a)` | [std] proxy table below × `franchise_factor` × `sex_factor` | values **[std]** (3) |
| ITT termination by duration | [std] proxy table below: recovery / IPT transition / death in claim | values **[std]** (4) |
| 1 095-day assessment split `ipt_share_at_cap` | 0.35 to IPT, 0.65 back to `healthy` | value **[std]** (4) |
| Mortality in IPT `ipt_mort_factor` | 3.0 × `mort_rate(a)` | value **[std]** (5) |
| *Résiliation* `lapse_rate(y)` | [std] table below, by policy year | values **[std]** (6) |
| CRD-basis premium scale | [std] table below, annual rate on the CRD by attained age | values **[std]** (7) |
| Maintenance expense | EUR 30 per policy per year, inflating 1.8 %/yr | **[std]** (8) |
| Claim management expense | EUR 250 per year per claim in payment, inflating 1.8 %/yr | **[std]** (8) |
| `income_loss_ratio` (indemnitaire only) | 1.00 in base | **[std]** (9) |
| Claim admission ratio | 1.00 in base | **[std]** (10); observed declines [R12] |
| Discount | EIOPA risk-free term structure for valuation [REG-R5]; flat 2.5 %/yr in the worked example | rate **[std]** (11) |

1. INSEE population mortality is the only freely redistributable French series and is the
   data source behind every decrement CSV this library ships [REG-R24]. It is heavier than
   medically-selected insured experience, so the proxy overstates death cost for a
   standard-risk book and understates it for a Lemoine-waiver book written with no medical
   selection at all. The 0.60 female factor is a pick; one insurer is unisex instead [S3].
2. **No public French PTIA incidence rate exists.** PTIA pays the same benefit as Décès and
   is a subset of severe morbidity, so it is a fixed fraction of the death rate. The ratio
   matters mainly through the different cover-end ages: above `ptia_end_age` the PTIA
   decrement is off while Décès continues.
3. Shaped as a **claim-payment** inception rate specific to the *franchise*, as a real basis
   would be published per deferred period. `franchise_factor` = 1.60 / 1.25 / 1.00 / 0.85 /
   0.65 for 30 / 60 / 90 / 120 / 180 days and `sex_factor` = 1.00 male / 1.30 female, both
   **[std]** placeholders; the menu itself is sourced [S9].
4. Falling recovery and rising IPT transition with duration is the qualitative structure of
   any disability termination basis: short claims mostly recover, long claims mostly
   consolidate. The 0.35 split at the cap stands in for the medical assessment against the
   66 % *barème croisé* threshold [S1] [S9]; nothing public quantifies what fraction of
   three-year ITT claims clears 66 %.
5. Claimant mortality above healthy-life mortality is universal in disability experience;
   the ×3.0 factor has no French anchor.
6. **The behavioural heart of the product** — see Policyholder behavior modeling.
7. A rate on the outstanding balance re-read annually with the attained age
   [S2] [S5] [S7] [S8], calibrated so its present value over the base cell matches the level
   0.84 % scale to 0.11 % (Checks) and the margin over the [std] benefit basis is about 10 %.
8. No French ADE expense study was retrieved. EUR 30/policy/year is about 1.8 % of the base
   cell's annual premium; the claim expense reflects that an incapacity claim is medically
   managed, unlike a death claim. Both are placeholders.
9. *Indemnitaire* contracts cap the benefit at the actual income loss, *revenu de référence*
   less *revenu de remplacement* [S10]. Modeling that properly needs a distribution of
   employer sick pay and *prévoyance* cover across the book, which nothing retrieved
   supplies. At 1.00 the *indemnitaire* cell equals the *forfaitaire* cell, which is the
   honest base — the model exposes the lever rather than inventing its value.
10. Claims are admitted in full because the model has no way to distinguish an admitted claim
    from a declined one: the only public French figures are portfolio decline *rates* by
    guarantee and contract type [R12], with no split between late notice, cover-age breach and
    medical dispute. A portfolio calibration should set the ratio from its own claims register.
11. No numeric EIOPA curve value was extracted anywhere in this library, so the worked
    example's discount rate is a flat modeling convention [REG-R5]; it affects only the present
    values quoted in Checks, never the projected cash flows.

**[std] proxy healthy-life mortality** (annual, per mille, male; linear interpolation
between pivot ages; female = 0.60 × male):

| Age a | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 70 | 75 | 80 | 85 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `mort_rate` ‰ | 0.6 | 0.8 | 1.2 | 2.0 | 3.2 | 5.0 | 7.6 | 11.5 | 17.5 | 27.0 | 45.0 | 78.0 |

**[std] proxy ITT claim-payment inception rates** (annual, per mille of lives in `healthy`;
male, *franchise* 90 days; linear interpolation between pivot ages):

| Age a | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 69 |
|---|---|---|---|---|---|---|---|---|---|
| `itt_inception_rate` ‰ | 2.0 | 2.8 | 4.0 | 6.0 | 9.0 | 13.5 | 20.0 | 28.0 | 36.0 |

**[std] proxy ITT termination rates** (annual, by claim duration year since payment
inception; the three exits compete in the stated order):

| Claim duration year (months z) | 1 (1–12) | 2 (13–24) | 3 (25–36) |
|---|---|---|---|
| Recovery `itt_recovery_rate` | 0.55 | 0.30 | 0.15 |
| Transition to IPT `itt_to_ipt_rate` | 0.02 | 0.06 | 0.12 |
| Death in claim `itt_mort_rate` | 0.02 | 0.03 | 0.04 |

**[std] résiliation table** (annual rates from `healthy`; lives in `itt` or `ipt` do not
lapse — premiums are waived and the benefit is in payment **[std]**):

| Policy year y | 1 | 2 | 3 | 4–5 | 6+ |
|---|---|---|---|---|---|
| `lapse_rate` | 4 % | 12 % | 12 % | 10 % | 7 % |

**[std] CRD-basis premium scale** (annual rate applied to the CRD at the policy
anniversary, by attained age; linear interpolation; used only when
`premium_basis = capital_restant_du`):

| Age a | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 65 | 70 |
|---|---|---|---|---|---|---|---|---|---|
| Rate | 0.14 % | 0.18 % | 0.26 % | 0.40 % | 0.62 % | 0.95 % | 1.45 % | 2.10 % | 2.90 % |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy month, 0-based: `t = 0..T − 1`, `T = loan_term_months` (240 in the base cell) |
| `k` | a time point, 0-based: `k = 0` at adhesion, `k = t` opens month `t` and `k = t + 1` closes it |
| `y`, `a` | policy year `floor(t/12) + 1`; attained age `entry_age + y − 1` |
| `i` | monthly loan rate = `loan_rate_annual / 12` = 0.0025 |
| `ech` | *échéance* = `capital_initial × i / (1 − (1 + i)^(−T))` = 1 109.1952 |
| `crd(k)` | `ech × (1 − (1 + i)^(−(T − k))) / i`, `k = 0..T`; `crd(0) = capital_initial`, `crd(T) = 0` |
| `Q` | `quotite` (1.00 base) |
| `IR` | indemnity ratio: 1.00 if `indemnity_basis = forfaitaire`, else `income_loss_ratio` |
| `mth(r)` | annual-to-monthly conversion = `1 − (1 − r)^(1/12)` **[std]** (12) |
| `q_h`, `q_ptia` | monthly `mth(mort_rate(a))`, `mth(ptia_rate(a))` |
| `w` | monthly `mth(lapse_rate(y))` |
| `ι` | monthly `mth(itt_inception_rate(a) × franchise_factor × sex_factor)` |
| `ρ(z)`, `τ(z)`, `q_s(z)` | monthly recovery, IPT-transition and death-in-claim rates at duration `z` |
| `s_itt(z)` | monthly ITT persistency = `(1 − ρ(z)) × (1 − τ(z)) × (1 − q_s(z))` |
| `q_ipt` | monthly `mth(min(ipt_mort_factor × mort_rate(a), 1))` |
| `D(t)`, `P(t)`, `I(t)` | guarantee-in-force indicators for Décès, PTIA, ITT/IPT |
| `e_m(y)`, `ec_m(y)` | monthly maintenance and claim expense = `30/12` and `250/12`, × `1.018^(y−1)` |
| `v(t)` | discount factor for month `t`, whose flows fall at time `t + 1` (valuation: EIOPA curve [REG-R5]; worked example `1.025^(−(t+1)/12)`, footnote (11)) |

Dimensional check: `q_h`, `q_ptia`, `w`, `ι`, `ρ`, `τ`, `q_s`, `q_ipt` are monthly
probabilities; `crd` and death benefits are EUR; `ech`, `prem` and monthly benefits are EUR
per month; every cash flow below is EUR per month per policy issued.

12. Every annual rate in the tables above is converted with the same uniform-force
    approximation `1 − (1 − r)^(1/12)`, which makes each monthly rate strictly below its
    annual rate and keeps the twelve monthly survival factors multiplying back to the annual
    one. No retrieved source states a conversion convention for any French decrement.

### The loan spine and the guarantee indicators

`crd` is computed, never read from a table. Two equivalent forms, both of which the model
must satisfy to floating-point tolerance — that is `check_crd()`:

    crd(k) = ech x (1 - (1 + i)^(-(T - k))) / i
    crd(k) = crd(k - 1) x (1 + i) - ech        with crd(T) = 0 exactly

`crd` is the **only** thing linking the loan to the insurance: the death benefit in month
`t` is `crd(t + 1) × Q`, the disability benefit is `ech × Q`. The guarantee indicators are

    D(t) = 1 if a < deces_end_age else 0       (85 base cell -> in force for all t)
    P(t) = 1 if a < ptia_end_age  else 0       (70 base cell -> t <= 215)
    I(t) = 1 if a < itt_ipt_end_age else 0     (70 base cell -> t <= 215)

At the first month where `I(t) = 0`, **at BOM and before any transition**, all `l_itt` and
`l_ipt` mass moves into `l_h`: cover has ended, benefit stops, and those lives remain alive,
death-covered and premium-paying [S13]. `ι` is zero from that month.

### Premium

    prem(t) = prem_pp(y) x l_h(t)                                           (BOM)

re-read at each policy anniversary (`t ≡ 0 mod 12`), lives in `itt`/`ipt` paying nothing
(waiver [S5] [S11]) and `prem_pp` never falling when `P(t)` or `I(t)` does [S13]:

    premium_basis = capital_initial    : prem_pp(y) = capital_initial x Q x premium_rate_annual / 12
    premium_basis = capital_restant_du : prem_pp(y) = crd(12 x (y - 1)) x Q x crd_rate(a) / 12

### Transitions (EOM)

Out of `healthy`, in the order death, PTIA, *résiliation*, ITT inception **[std]**:

    dth_h(t)  = l_h(t) x q_h
    ptia_h(t) = l_h(t) x (1 - q_h) x q_ptia x P(t)
    lapses(t) = l_h(t) x (1 - q_h) x (1 - q_ptia x P(t)) x w
    n_itt(t)  = l_h(t) x (1 - q_h) x (1 - q_ptia x P(t)) x (1 - w) x i_rate,  i_rate = ι x I(t)
    h_stay(t) = l_h(t) x (1 - q_h) x (1 - q_ptia x P(t)) x (1 - w) x (1 - i_rate)

Out of ITT, in the order recovery, transition to IPT, death in claim **[std]**, for each
duration cohort `z`:

    rec_itt(t, z) = l_itt(t, z) x rho(z)
    trn_ipt(t, z) = l_itt(t, z) x (1 - rho(z)) x tau(z)
    dth_itt(t, z) = l_itt(t, z) x (1 - rho(z)) x (1 - tau(z)) x q_s(z)
    stay(t, z)    = l_itt(t, z) x s_itt(z)

For `z < itt_max_months` the survivors advance, `l_itt(t+1, z+1) = stay(t, z)`. For
`z = itt_max_months` (36, the 1 095-day cap) they are **assessed** instead of advanced:
`cap_itt(t) = stay(t, itt_max_months)`, of which `ipt_share_at_cap` passes to IPT and the
remainder returns to `healthy`. Out of IPT there is no recovery — the only exits are death
and the age limit: `dth_ipt(t) = l_ipt(t) × q_ipt`, `ipt_stay(t) = l_ipt(t) − dth_ipt(t)`.
State update, from the states opening month `t` to those closing it:

    l_h(t+1)     = h_stay(t) + SUM_z rec_itt(t, z) + (1 - ipt_share_at_cap) x cap_itt(t)
    l_itt(t+1,1) = n_itt(t);  l_itt(t+1, z+1) = stay(t, z)  for z < itt_max_months
    l_ipt(t+1)   = ipt_stay(t) + SUM_z trn_ipt(t, z) + ipt_share_at_cap x cap_itt(t)

Recovered lives return to `healthy` and are again exposed to inception **[std]**. When
`ipt_benefit_basis = crd`, IPT is not a state at all: the mass that would enter IPT instead
triggers a single payment `crd(t + 1) × Q` and leaves the model, exactly as a death does
[S1] [S2] [S7].

### Benefit outgo, expenses and net cash flow (EOM)

    ben_deces(t) = crd(t+1) x Q x (dth_h(t) + SUM_z dth_itt(t,z) + dth_ipt(t)) x D(t)
    ben_ptia(t)  = crd(t+1) x Q x ptia_h(t)
    ben_itt(t)   = ech x Q x IR x SUM_z stay(t, z)
    ben_ipt(t)   = ech x Q x IR x (ipt_stay(t) + SUM_z trn_ipt(t, z))
    expenses(t)  = e_m(y) x (l_h + l_itt + l_ipt)(t) + ec_m(y) x (l_itt + l_ipt)(t)

    liability_cf(t) = ben_deces + ben_ptia + ben_itt + ben_ipt + expenses - prem
    net_cf(t)       = -liability_cf(t)

`ben_itt` includes the capped cohort — a life in ITT throughout month `t` is paid for that
month whether it then stays, passes to IPT at the cap, or returns to `healthy` — and
`ben_ipt` includes lives that transitioned at EOM `t`, so the ITT → IPT move creates no
unpaid month. New inceptions `n_itt(t)` are **not** paid for month `t`. Death, PTIA,
*résiliation* and expiry generate no other payment: no surrender value, no maturity benefit.

### Monthly processing order [std]

At month `t = 0..T − 1` (nothing survives the frame; at `t = T − 1`, the last month, all
cover and any claim in payment terminate without value [S1] [S9]):

1. **Anniversary (BOM, `t = 0, 12, 24, …`):** advance `y` and `a`; set `D(t)`, `P(t)`,
   `I(t)`; re-read `prem_pp(y)` on the CRD basis, leave it unchanged on the
   *capital initial* basis.
2. **Guarantee-cessation transfer (BOM):** if `I(t) = 0` and any `l_itt`/`l_ipt` mass
   remains, move all of it into `l_h` and zero those states.
3. **Premium income (BOM):** `prem(t) = prem_pp(y) × l_h(t)`.
4. **Loan instalment (EOM):** the schedule carries `crd(t)` to `crd(t + 1)` —
   deterministic, unaffected by any decrement.
5. **Transitions out of `healthy` (EOM):** death, PTIA, *résiliation*, ITT inception.
6. **Transitions out of ITT (EOM):** recovery, IPT transition, death in claim, per duration
   cohort; then the 1 095-day assessment on cohort `z = itt_max_months`.
7. **Transitions out of IPT (EOM):** death.
8. **State update** to time `t + 1` for `l_h`, `l_itt(·, z)`, `l_ipt`.
9. **Benefit outgo (EOM):** `ben_deces`, `ben_ptia`, `ben_itt`, `ben_ipt`.
10. **Expenses (EOM)**, then discount at `v(t)` and accumulate.

### Known modeling pitfalls

Each of these produces a model that looks right and is wrong. They are the test list.

- **Reading the CRD from a table instead of computing it.** The whole product hangs off
  `crd`; a pasted schedule will not satisfy `crd(k) = crd(k−1) × (1 + i) − ech` at every `k`
  and `crd(T)` will not be zero. Assert both.
- **Using the wrong CRD, or the wrong rate conversion.** `crd(t)` (opening month `t`, before
  its instalment) and `crd(t + 1)` (closing it, after the instalment) differ by the month's
  capital repayment — EUR 609.20 over month `t` = 0 in the base cell; the convention here is
  the **closing** balance `crd(t + 1)` and whichever is chosen must be used everywhere. A
  model that indexes `crd` on the month rather than on the time point pays a whole month's
  capital too much or too little. Separately, French loans quote a *taux nominal annuel*
  whose monthly rate is nominal ÷ 12, not `(1 + nominal)^(1/12) − 1`; the effective
  conversion changes `ech`, and therefore every benefit and the TAEA.
- **Collapsing Décès and PTIA into one decrement.** They pay the identical benefit, so the
  temptation is strong — and it is wrong, because `deces_end_age` (85) and `ptia_end_age`
  (70) differ. A collapsed decrement either pays PTIA after 70 or stops paying death
  before 85.
- **Letting the premium fall when the ITT/IPT guarantees cease.** The rate is *nivelé*: the
  cover shrinks at 70 and the premium does not [S13]. In the base cell that is 24 months ×
  EUR 140.00 = **EUR 3 360.00 of premium per surviving policy against death cover alone**; a
  model that switches the premium off with the guarantee understates premium income by
  exactly that. The mirror error is letting `ben_itt` or `ben_ipt` run past the age limit:
  both must be exactly zero wherever `I(t) = 0`, and the in-claim mass must be *moved*, not
  deleted — deleting it breaks the state identity and destroys the death cover those lives
  still hold.
- **Collapsing the ITT duration dimension, or dropping the cap.** A single ITT bucket with
  duration-independent terminations misstates runoff badly — the proxy recovery rate falls
  0.55 → 0.15 while the IPT transition rate rises 0.02 → 0.12 across the three duration years
  — and the 1 095-day assessment cannot be expressed at all without `z`. If cohort `z` = 36
  simply advances to `z` = 37, ITT claims run for ever and IPT is never fed from the cap: in
  the base cell that is 35 % of the 0.198077 of each inception still in ITT at three years.
- **Paying the ITT → IPT movers twice, or not at all.** A life moving from ITT to IPT at EOM
  `t` must be paid exactly once for month `t`. Assert
  `ben_itt(t) + ben_ipt(t) = ech × Q × IR × (l_itt(t+1) − n_itt(t) + l_ipt(t+1) + (1 −
  ipt_share_at_cap) × cap_itt(t))` — the paying mass equals the closing disabled mass, less
  the month's new inceptions, plus the share of the capped cohort sent back to `healthy`:
  those lives were in ITT throughout month `t` and are paid for it, but they end the month
  in neither disabled state, so an identity written without that term is short by
  `ech × Q × IR × (1 − ipt_share_at_cap) × cap_itt(t)` — up to EUR 0.13 a month in the base
  cell. Relatedly, benefit is monthly in arrears: including `n_itt(t)` in `ben_itt(t)` pays
  a full month at the instant of inception.
- **Charging premium to lives in claim, or lapsing them.** Premiums come from `l_h` only
  [S5] [S11]; `prem_pp × (l_h + l_itt + l_ipt)` overstates premium income and is easy to
  write by accident when the model also tracks total lives in force. Symmetrically, applying
  the *résiliation* decrement to `l_itt`/`l_ipt` silently cancels claims in payment.
- **Quotité applied twice, or to the wrong leg.** `quotite` scales the benefit *and* the
  premium, once each. Applying it to the CRD and again to the benefit is invisible at
  `quotite` = 1.00 — the base cell will not catch it. Test at `quotite` = 0.60. For the same
  reason `indemnitaire` must be the same formula with `IR < 1`, not a second benefit
  expression that can drift from the *forfaitaire* leg.
- **Assuming the "decreasing" premium decreases.** On the CRD basis at entry age 52 the
  premium *rises* from EUR 125.33 in policy year 1 to a peak of EUR 164.03 in year 10 before
  falling to EUR 31.65 in year 20, because the attained-age rate climbs faster than the CRD
  falls. A monotonicity assertion on the CRD-basis premium will fail — correctly.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions. No public French ADE
policyholder-behaviour study was retrieved, and the CCSF's published series are counts of
substitution *requests*, not portfolio lapse rates [R12].

- **Base résiliation [std].** `lapse_rate(y)` per the table above; monthly
  `w = 1 − (1 − lapse_rate)^(1/12)`, applied to `l_h` only. The shape — low in year 1,
  tripling in year 2, then decaying to a 7 % ultimate — is a reading of the statutory
  mechanics rather than of data. Cancellation is available *à tout moment* from signature of
  the loan offer [R1] [R3] [REG-R35], so nothing legal holds year 1 down; what holds it down
  is that the borrower has just signed, the lender's ten-business-day answer and the
  substitute's effective-date rule put real friction in the path [R1] [R3] [R8], and the
  *fiche standardisée* has only just been read [R4] [R5]. From year 2 the insurer's own
  **annual reminder** of the cancellation right arrives [R1], brokers solicit, and the
  substitution machine engages. This is **materially higher than a classic protection
  lapse**: substitution requests to banking networks rose from 99 265 in H1 2021 to 181 600
  in H1 2023, the alternative share of insured portfolios rose from 15.3 % to 16.0 % between
  2021 and May 2023, and about 215 000 external alternative contracts were added in 17
  months [R12].
- **Substitution as a response to the premium gap [std].** Résiliation here is not a lapse in
  the ordinary sense — the cover does not stop, it moves — so the rate is made to respond to
  the gap between the premium in force and the price of an equivalent contract in the market:

      gap(y)   = max(0, prem_pp(y) / market_prem_pp(y) - 1)
      w_dyn(y) = min(w_max, lapse_rate(y) x (1 + beta x gap(y)))

  with `beta` = 3.0 and `w_max` = 0.35 **[std]** and `market_prem_pp` a scenario input (base:
  equal to `prem_pp`, so `gap` = 0 and `w_dyn` = `lapse_rate`). The sensitivity is
  deliberately steep: the CCSF measured bank group tariffs falling **14 %–30 % across the age
  range** between 2019 and 2023 while medically-selected external alternative contracts moved
  between **−40 % and +16 %** by age [R12], so a book written at an older tariff faces a
  two-digit gap without doing anything. Acceptance is not automatic — lenders accept
  88 %–90 % of requests through banking networks and 70 %–87 % through intermediaries [R12] —
  so an **acceptance ratio of 0.88 [std]** multiplies the substitution component, refused
  requests remaining in force [R3].
- **Selective withdrawal [std note].** Substitution requires an equivalent-guarantee offer
  from another insurer [R7] [REG-R36], which on a medically-selected contract means passing
  underwriting again: healthy lives leave, impaired lives stay, and the residual book's
  morbidity is worse than the table. The socio-professional skew is consistent — CSP1 are
  58 % of substitutions and 69 % of external alternative contracts taken at origination but
  only 27 % of the banks' mortgage portfolios [R12]. The base applies **no** anti-selection
  loading **[std]**; the scenario lever is `itt_inception_rate × (1 + selection_load)`.
- **Lapse in claim is zero [std]** — premiums are waived and the benefit is in payment
  [S5] [S11]. **Early repayment** ends the cover if total [S1] [S9] and rebases the premium
  on the guaranteed CRD less the amount repaid if partial [S9] [S10]; the base holds the
  amortisation schedule fixed **[std]**, an early-repayment decrement being a documented
  extension. The **questionnaire waiver** and the ***droit à l'oubli*** are **underwriting**
  effects, not projection decrements: they change who is in the book and at what rate, not
  how a policy runs. The waiver applies only where the insured share of the cumulative
  *encours* is ≤ EUR 200 000 **and** repayment falls before the 60th birthday [R1] [R2],
  which is narrow — 58.5 % of borrowers were under the amount threshold but only 23 % of
  those contracts were eligible, and contracts without medical selection are only 31 % of
  substitutions [R12]. Where it does apply, external alternative contracts without medical
  selection were repriced up by **about 10 % on average** against 2021 tariffs [R12] — an
  anti-selection loading with a public number. The base carries no such loading and no
  `underwriting_basis` column **[std]**.

---

## Worked example

The base cell, run from issue for 15 months. Configuration: male, `entry_age` 52,
`capital_initial` EUR 200 000, `loan_rate_annual` 3.00 % (`i` = 0.0025), `loan_term_months`
240, `quotite` 1.00, `premium_basis` = `capital_initial`, `premium_rate_annual` 0.84 %,
`indemnity_basis` = `forfaitaire` (`IR` = 1.00), `franchise_days` 90, `itt_max_days` 1 095,
`ipt_benefit_basis` = `echeance`, `deces_end_age` 85, `ptia_end_age` 70, `itt_ipt_end_age`
70. All decrements are the **[std]** proxy tables above and the discount is 2.5 %/yr flat
**[std]** (used only for present values in Checks); every assumption is [std] except the
guarantee structure, the benefit bases and the age limits, which are [S9] [S11] [S13] as
tabulated in the spec.

Derived constants: `ech` = 1 109.1952; `prem_pp` = 200 000 × 1.00 × 0.0084 / 12 = **140.00**.
Monthly rates at `a` = 52: `q_h` = 0.000327255, `q_ptia` = 0.000032673, `ι` = 0.000904486,
`w` = 0.003396053 in year 1 and 0.010596241 in year 2, each from `1 − (1 − r)^(1/12)` on the
annual rates 0.00392, 0.000392, 0.01080, 0.04 and 0.12. Duration-year-1 terminations:
`ρ` = 0.064376669, `τ` = `q_s` = 0.001682143, so `s_itt` = 0.932478274. At `a` = 53,
`q_h` = 0.000357368 and `ι` = 0.000980268.

Months are 0-based, so the first row is `t` = 0 (policy year `y` = 1 throughout the first
twelve). The CRD and state columns are the **closing** quantities of month `t`, i.e. the
values at time `t + 1`; the cash flow columns are the flows of month `t`.

| t | crd(t+1) | l_h(t+1) | l_itt(t+1) | l_ipt(t+1) | prem(t) | ben_deces(t) | ben_ptia(t) | ben_itt(t) | ben_ipt(t) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 199,390.80 | 0.995344 | 0.000901 | 0.000000 | 140.00 | 65.25 | 6.51 | 0.00 | 0.00 |
| 1 | 198,780.09 | 0.990768 | 0.001737 | 0.000001 | 139.35 | 65.03 | 6.46 | 0.93 | 0.00 |
| 2 | 198,167.84 | 0.986267 | 0.002513 | 0.000004 | 138.71 | 64.79 | 6.41 | 1.80 | 0.00 |
| 3 | 197,554.07 | 0.981837 | 0.003232 | 0.000008 | 138.08 | 64.54 | 6.36 | 2.60 | 0.01 |
| 4 | 196,938.76 | 0.977474 | 0.003898 | 0.000013 | 137.46 | 64.28 | 6.32 | 3.34 | 0.01 |
| 5 | 196,321.91 | 0.973174 | 0.004516 | 0.000019 | 136.85 | 64.01 | 6.27 | 4.03 | 0.02 |
| 6 | 195,703.52 | 0.968933 | 0.005088 | 0.000026 | 136.24 | 63.72 | 6.22 | 4.67 | 0.03 |
| 7 | 195,083.58 | 0.964750 | 0.005617 | 0.000034 | 135.65 | 63.42 | 6.17 | 5.26 | 0.04 |
| 8 | 194,462.09 | 0.960620 | 0.006107 | 0.000043 | 135.06 | 63.12 | 6.13 | 5.81 | 0.05 |
| 9 | 193,839.05 | 0.956540 | 0.006561 | 0.000053 | 134.49 | 62.81 | 6.08 | 6.32 | 0.06 |
| 10 | 193,214.46 | 0.952509 | 0.006980 | 0.000063 | 133.92 | 62.48 | 6.04 | 6.79 | 0.07 |
| 11 | 192,588.30 | 0.948524 | 0.007367 | 0.000074 | 133.35 | 62.16 | 5.99 | 7.22 | 0.08 |
| 12 | 191,960.57 | 0.937659 | 0.007789 | 0.000085 | 132.79 | 67.31 | 6.49 | 7.62 | 0.09 |
| 13 | 191,331.28 | 0.926937 | 0.008184 | 0.000099 | 131.27 | 66.54 | 6.40 | 8.07 | 0.11 |
| 14 | 190,700.41 | 0.916356 | 0.008553 | 0.000114 | 129.77 | 65.77 | 6.30 | 8.49 | 0.13 |

Column sums over `t` = 0..14: `prem` 2 032.99, `ben_deces` 965.23, `ben_ptia` 94.16,
`ben_itt` 72.95, `ben_ipt` 0.71, `expenses` 38.10.

**Supplementary — one ITT cohort through the 1 095-day cap.** `S(z)` is the probability that
a claim incepting at `z` = 0 is still in ITT at the end of duration month `z`:

| z | ρ(z) | τ(z) | q_s(z) | s_itt(z) | S(z) |
|---|---|---|---|---|---|
| 1 | 0.064377 | 0.001682 | 0.001682 | 0.932478 | 0.932478 |
| 6 | 0.064377 | 0.001682 | 0.001682 | 0.932478 | 0.657404 |
| 12 | 0.064377 | 0.001682 | 0.001682 | 0.932478 | 0.432180 |
| 13 | 0.029286 | 0.005143 | 0.002535 | 0.963274 | 0.416308 |
| 24 | 0.029286 | 0.005143 | 0.002535 | 0.963274 | 0.275843 |
| 25 | 0.013452 | 0.010596 | 0.003396 | 0.972779 | 0.268335 |
| 35 | 0.013452 | 0.010596 | 0.003396 | 0.972779 | 0.203620 |
| 36 | 0.013452 | 0.010596 | 0.003396 | 0.972779 | 0.198077 |

At `z` = 36 the surviving 0.198077 is assessed: **0.069327 passes to IPT** (35 %) and
**0.128750 returns to `healthy`** (65 %). Expected months of ITT payment per inception =
Σ_{z=1..36} S(z) = **14.721231**, i.e. **EUR 16 328.72** of ITT benefit per inception at
`ech × Q` = 1 109.1952.

**Checks.**

*The loan spine, two ways.* From the annuity formula, `crd(1)` = 1 109.1951957 ×
(1 − 1.0025^(−239)) / 0.0025 = **199 390.8048**. By roll-forward,
`crd(0) × (1 + i) − ech` = 200 000 × 1.0025 − 1 109.1951957 = **199 390.8048** — identical.
At the far end `crd(239)` = 1 106.4291 and `crd(239) × 1.0025` = 1 109.1952 = `ech`, so
`crd(240)` = 0 exactly. Total instalments 240 × 1 109.1952 = 266 206.85, of which 66 206.85
is interest.

*The state recursion, from the four decrements.* `l_h(1)`, the state at the end of month
`t` = 0, should be
(1 − 0.000327255)(1 − 0.000032673)(1 − 0.003396053)(1 − 0.000904486) = **0.995344**, which is
the table's first row. The residual mass is the four exits of that month — `dth_h(0)` =
0.000327255, `ptia_h(0)` = 0.000032662, `lapses(0)` = 0.003394831, `n_itt(0)` = 0.000901090
— and 0.995344 plus those four is 1.000000. Over the whole 15 months `l_h + l_itt + l_ipt` =
0.925024 and cumulative exits = 0.074976, summing to 1.000000000000: `check_states()`.
`l_h` then falls 0.4598 % per month through policy year 1 (0.995344 → 0.990768) and 1.1455 %
per month in year 2 (0.948524 → 0.937659) — the loi Lemoine substitution assumption
arriving, monthly `w` going from 0.003396053 to 0.010596241, a factor of 3.12 diluted by the
unchanged mortality and inception decrements. The mortality step at `t` = 12, the first
month of policy year 2, shows separately in `ben_deces`, which rises 62.16 → 67.31 as `a`
goes 52 → 53 (`mort_rate` 0.00392 → 0.00428) on a CRD that is still falling.

*The in-arrears benefit rule.* `ben_itt(0)` = 0.00 because the only ITT mass at the end of
month 0 is that month's own inception. `ben_itt(1)` = `ech × s_itt(1) × n_itt(0)` =
1 109.1952 × 0.932478274 × 0.000901090 = **0.93** — the month-0 inceptions, one month later,
net of one month's terminations (`s_itt` is on the claim-duration clock `z`, where the first
month in payment is `z` = 1). `ben_deces(0)` = `crd(1) × q_h` = 199 390.8048 × 0.000327255 =
**65.25**, and `ben_ptia(0) / ben_deces(0)` = 6.512472 / 65.251648 = 0.0998, the
`ptia_rate` ratio of 0.10 less the month of death exposure that precedes PTIA in the
decrement order — the ordering is visible in the arithmetic.

*Aggregates over the full 240 months, at 2.5 % flat.* PV of premium income is
**EUR 12 602.19** on the level 0.84 % *capital initial* basis and **EUR 12 588.82** on the
CRD basis (ratio 1.001062; equivalent level rate 0.8391 %, rounded to 0.84 % for the spec),
the CRD basis being non-monotonic — EUR 125.33 in year 1, EUR 164.03 at its year-10 peak,
EUR 31.65 in year 20. PV of outgo is `ben_deces` 7 170.56 + `ben_ptia` 635.87 + `ben_itt`
1 932.71 + `ben_ipt` 1 293.18 + `expenses` 334.17 = **EUR 11 366.49**, a margin of 9.81 % on
premium, with death and PTIA **70.8 %** of the benefit PV and ITT plus IPT **29.2 %** against
the market's published premium split of **69 % / 30 %** [REG-R37] — a coincidence of
calibration rather than evidence, but the only external check available on the shape of the
basis. Finally `I(t)` = 0 from `t` = 216 (`a` = 70): `crd(216)` = **EUR 25 806.51** is still
owed as that month opens, 0.009266 + 0.013982 of mass in ITT and IPT moves to `l_h`,
`ben_itt` and `ben_ipt` are exactly zero for `t` = 216..239, and premium income continues
— **EUR 3 360.00 nominal per surviving policy** (24 × EUR 140.00), EUR 638.67
survivorship-weighted.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers consume
them and are NOT reproduced here.

- **Solvabilité II.** Technical provisions = best estimate + risk margin, the best estimate
  being the probability-weighted average of future cash flows discounted at the relevant
  risk-free term structure [REG-R4], with curves published monthly by EIOPA
  [REG-R5] — exactly the projections above, on both the premium and the claim side. No
  cost-of-capital rate in this library rests on a retrieved instrument [REG-R2], so any
  risk-margin figure would be **[std]**; none is specified.
- **French statutory provisions.** Art. R. 343-3 of the Code des assurances enumerates
  eleven technical provisions [REG-R6]; the two an ADE book touches are the *provision
  mathématique* — which for a French contract includes future management costs, so it is not
  a pure net-premium reserve — and the *provision pour égalisation* for mortality
  fluctuations on group death business. **How a French insurer actually reserves the
  increasing-risk pattern created by a *nivelé* premium was not established by any retrieved
  source and is [unverified]** (spec, Regulatory context). The model supplies the cash flows
  such a provision consumes; it does not compute one.
- **Claims in payment** are a disabled-life annuity: the expected present value of
  `ech × Q × IR` until recovery, transition, death, the age limit or loan expiry, run from
  `(a, z)` with the recursions above and `l_h(0)` = 0; the supplementary table is that
  annuity's survival column for `z` = 0. **IFRS 17** [REG-R45] consumes the same projections
  with its own discounting, risk adjustment and CSM layers (cited-not-specified), and the
  professional frame is NPA 1 [REG-R43] and NPA 2 [REG-R44], the Institut des actuaires'
  *pratiques recommandées* on general actuarial practice and on actuarial models.

---

## Key sensitivities and model risks

1. **Résiliation.** First-order and product-defining: it sets premium income, the effective
   duration of the book and, through selective withdrawal, the morbidity of what remains.
   The whole table is **[std]** with no French anchor and the dynamic response to the premium
   gap is a construction, not a calibration; the observable facts are counts of substitution
   requests and a 15.3 % → 16.0 % market-share shift [R12], neither of which is a lapse rate.
   Test `lapse_rate`, `beta` and the acceptance ratio independently.
2. **ITT inception and termination.** Inception drives claim frequency; the recovery /
   IPT-transition split drives claim length and therefore the whole disabled-life annuity — a
   small change in `itt_recovery_rate` compounds over 36 months and again through the 0.35
   split at the cap. Both proxy tables are **[std]** placeholders.
3. **Mortality level and the CRD profile together.** Death is 70.8 % of the benefit PV and
   its cost is `crd(t + 1) × q_h(a)`, a falling schedule times a rising rate; the peak of that
   product, not either factor alone, is where the death cost sits, and the loan term moves it.
4. **The premium basis, and the age limits.** Level on *capital initial* against annually
   re-read on the CRD is a different cash flow shape for the same cover, and the difference is
   largest exactly where lapse is highest; the two are PV-equivalent here **by construction**
   and would not be in a real tariff. The cover-end ages are cited rather than [std], but their
   interaction with loan term is under-appreciated — 24 uncovered months in the base cell,
   worse for a longer loan or an older entrant, and the CCSF records "maximum cover age
   exceeded" among the commonest causes of claim decline [R12].
5. **The 1 095-day assessment split, indemnitaire exposure, expenses and claim admission.**
   `ipt_share_at_cap` converts a bounded three-year claim into an annuity that can run to the
   end of the loan; nothing public quantifies it and the liability is roughly linear in it. At
   `income_loss_ratio` = 1.00 the *indemnitaire* cell equals the *forfaitaire* cell, but real
   *indemnitaire* business pays materially less to employees whose salary is maintained
   [S6] [S10]. Expenses (EUR 334.17 of PV) and the assumed 100 % claim admission — against
   observed declines of 7.7 %–16.3 % on incapacity claims [R12] — are second-order for the
   total and first-order for the margin.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-assurance_emprunteur-r1
[R12]: #frlib-assurance_emprunteur-r12
[R17]: #frlib-assurance_emprunteur-r17
[R2]: #frlib-assurance_emprunteur-r2
[R3]: #frlib-assurance_emprunteur-r3
[R4]: #frlib-assurance_emprunteur-r4
[R5]: #frlib-assurance_emprunteur-r5
[R7]: #frlib-assurance_emprunteur-r7
[R8]: #frlib-assurance_emprunteur-r8
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R35]: #frlib-reg-r35
[REG-R36]: #frlib-reg-r36
[REG-R37]: #frlib-reg-r37
[REG-R4]: #frlib-reg-r4
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
