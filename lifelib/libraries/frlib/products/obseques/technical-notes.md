# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26; see `sources.md`).

**Scope note.** These notes specify a reference liability cash flow projection model for the
standardized composite product defined in `product-spec.md` (same directory) — the French
**contrat obsèques** in its capital form. This is not any single insurer's product. [S#]/[R#]
tags refer to the source list in `_research/obseques.md` via `sources.md`; [REG-R#] tags refer
to the cross-product reference library `references/regulatory-and-actuarial-references.md` (its
own R-numbering). **[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter values are
identical to those in `product-spec.md`. Euro amounts use a decimal point and no thousands
separator so that every figure is machine-checkable; the sources use the French decimal comma
and the figures are transcribed unchanged.

The model is **`Obseques_FR_S`**, on a **monthly** grid. One engine serves three cells, which
differ only in the `premium_form` column of the model point table:

- **RefOBS-VIA** — *primes viagères*: entry 50, capital 5000 €, 336.03 €/year for life,
  revalorisation 1.00 % p.a. [S14]. **This is the worked-example cell.**
- **RefOBS-TMP** — *primes temporaires*: entry 50, capital 5000 €, 651.26 €/year for 10 years,
  revalorisation 1.00 % p.a. [S14].
- **RefOBS-UNI** — *prime unique*: entry 50, capital 5000 €, 4274.04 € once [S5],
  revalorisation 0.00 % **[std]** (the source presents its values *sans participation aux
  bénéfices*, so a non-zero rate would be inconsistent with its own surrender scale [S5]).

Two structural differences from the UK guaranteed-acceptance sibling in
`uklib/products/whole_of_life` drive most of the extra machinery here. The sum assured is a
**state variable that grows** out of the *participation aux bénéfices*, not a constant; and
**lapse pays money** — the surrender value is the *provision mathématique* [S1] [S8] [S9] —
so the "every lapse is a free profit release" arithmetic of the UK design does not carry over.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premium income, death outgo,
  surrender outgo, expenses) for single-policy model points. Reserves, discounting, risk margin
  and capital are pointed to, not computed.
- **Projection frequency.** Monthly **[std]**. The contractual premium is annual and payable in
  advance with instalment options [S1] [S8] [S9]; the monthly grid is required by the
  twelve-month *délai de carence*, whose boundary must not be smoothed.
- **Time index.** `t` is the **0-based** policy month: `t = 0` is the first policy month, month
  `t` runs from time `t` to time `t + 1`, and the frame is `t = 0, 1, …, proj_len − 1`, so
  `proj_len` is the *number* of projected months. The **policy year** is the contractual,
  1-based label derived from it, `y = policy_year(t) = floor(t/12) + 1`, and it is what the
  premium, lapse and select schedules are keyed by. Where these notes say "policy year 1" they
  mean the contractual year `y = 1`, which is `t = 0 … 11`.
- **Timing conventions [std].** Premiums at the beginning of the policy month (BOM); deaths
  resolved at end of month (EOM) against the BOM in-force; surrenders and *réductions* at EOM
  after deaths. Revalorisation and premium uprating step at policy anniversaries.
- **Age basis.** ***Différence de millésime*** — calendar year of subscription minus calendar
  year of birth [S1] [S8] [S9]; **not** age last birthday and **not** age nearest birthday. The
  true basis increments on 1 January; the model increments at the policy anniversary instead,
  `age(t) = entry_age + floor(t/12)` **[std]**, exact for January issues.
- **Projection horizon.** `proj_len = 12 × (omega − entry_age + 1)` months with **omega = 112**
  **[std]** — the number of projected months, so the last one is `t = proj_len − 1` — the
  tabulation limit of TH 00-02 in the annexe to art. A. 335-1 CA [REG-R23];
  `mort_rate` is forced to 1 at attained age omega. One insurer's tables run to attained age 115
  [S15], so the horizon is a modelling convention, not a contractual one.
- **Currency / units.** EUR. `mort_rate` and `lapse_rate` are annual and dimensionless,
  converted as `q_m = 1 − (1 − q)^(1/12)` **[std]**.
- **Model points.** Single-policy expected-value projection. Aggregate capital caps across
  contracts on one insured (10000 € [S1] [S8], 17580 € [S12]) are per-insured underwriting
  limits and are not modeled.
- **Claims settlement.** Immediate at EOM of the death month **[std]**. The post-mortem
  revalorisation between death and payment — the lower of the twelve-month average TME and the
  last TME at 1 November of the preceding year [S1] [S8] [R8] — and the statutory payment clock
  of art. L. 132-23-1 CA [REG-R31] are settlement-lag refinements, excluded.
- **Sign convention.** The notes print the stream outgo-positive as `liability_cf`; the model
  publishes `net_cf(t) = −liability_cf(t)`, income-positive, per the library convention.
- **Rounding.** Full precision carried; the worked example displays cash flows to the cent and
  survivorship to five decimals, and the model must reproduce it at that precision.

---

## Deltas against the temporaire décès chassis

`../temporaire_deces/technical-notes.md` specifies **`TD_FR_S`**, this library's protection
chassis — an individual French death cover on a decrement-and-premium engine that this product
reuses rather than reinvents. Those notes are the source of truth for the chassis; this section
states only what `Obseques_FR_S` takes unchanged and where it departs, and does not restate the
machinery. Source ids differ between the two products' research files, so facts belonging to the
chassis are pointed at by section rather than re-tagged here.

**Inherited unchanged.** The **age basis**: *différence de millésime*, calendar year of
subscription minus calendar year of birth, stepped at the policy anniversary as a **[std]**
proxy for the true 1 January step [S1] [S8] [S9]. The **decrement order**: the insured decrement
resolves first, the policyholder decrement takes the survivors of it. The **shared vocabulary**
and its sign convention — `pols_if`, `mort_rate`, `lapse_rate`, `premiums`, `claims`,
`expenses`, `net_cf`, `result_cf`, with `net_cf` income-positive and the notes' outgo-positive
stream published as `liability_cf`. The **mortality basis posture**: TH 00-02 / TF 00-02 are the
homologated regulatory tables for a death cover on both products, are cited by name and never
shipped [REG-R22] [REG-R23], and both models run a **[std]** Gompertz-form proxy rising 9 % per
year of age, anchored at 0.0040 at the reference cell's own entry age — here carrying a sex
dimension as well, because the premium is read from a published rate card and sex therefore
enters only the best-estimate decrement. And the **absence of an account value**: on both
products the benefit is a stated capital, not a fund.

Five departures, and each is first-order.

| | `TD_FR_S` — *temporaire décès* | `Obseques_FR_S` — *obsèques* |
|---|---|---|
| Underwriting | Underwritten issue: a two-tier *déclaration de santé* escalating to a full *questionnaire médical* and thence to examinations, with a *surprime* multiplier (`rating_factor`) on the tariff rate | **Guaranteed acceptance**: no questionnaire, no examination, at every retrieved contract [S1] [S11] [S12] [S13]. There is no rating factor and no rated-lives dimension |
| Anti-selection device | Underwriting itself; a *délai d'attente* only where the adhesion carried no medical formality, and off (`waiting_period_y = 0`) in the base run | A **12-month *délai de carence* on every contract that states a duration** [S1] [S8] [S9] [S11] [S13] — the rest reference *carences* in their tables without giving one [S5] [S14] [S15] [S16] — because underwriting is always waived. Not a variant: it is the chassis of the product |
| Year-1 exclusion | Suicide voids the death cover in year 1: `suicide_factor(t)`, a multiplicative withholding on `claims_death` in year 1 only, paying **nothing** | Suicide is excluded for 12 months [S1] [S8] [S12] [S13] but the insurer pays the ***valeur de rachat*** / *provision mathématique*, not zero [S1] [S8] [S12]. There is no `suicide_factor` cells here |
| Sum assured | `sum_assured`, level or on a fixed `benefit_schedule_id`; indexation off in the base run | `capital_pp(t)`, a **state variable that grows** out of the *participation aux bénéfices*, 1.00 % p.a. guaranteed in the reference cell [S14] |
| Premium-stops | `pols_lapse` moves `pols_if` and **nothing else**; `claims_lapse(t)` is structurally zero, by statute | `pols_lapse` is **paid `surr_value_pp(t)`**; `claims_lapse` is non-zero from t = 0 and worth 1005.89 € over the anchor cell's horizon |

Two second-order differences follow from the first five and are worth stating so an implementer
does not carry a chassis habit across. Both models run a **monthly** grid, but they carry
different things on it and end in different ways. `TD_FR_S` is contractually annual end to end —
a one-year cover renewed by *tacite reconduction* and repriced at every renewal, so its tariff,
its capital and its decrement vectors all step on the anniversary and its finer grid buys only
the timing of claims, expenses and the modal instalment — and its horizon ends at a stated
`cover_end_age` where nothing is payable. Here the monthly grid is forced by the product rather
than chosen for resolution, because the *carence* boundary at twelve months must not be smoothed,
and the model has **no term at all** — `proj_len = 12 × (omega − entry_age + 1)` with
omega = 112 **[std]**, and the contract ends only on death, on *rachat* or on lapse
[S1] [S8] [S9] [S11]. And the premium moves in opposite ways: on `TD_FR_S` the tariff is re-read
at the new attained age at every renewal, so the premium rises with age by construction; here it
is **fixed at inception** and the form is final [S1] [S5] [S14], which is exactly what produces
the overrun — cumulative premiums grow without bound while the capital grows at most at
`reval_rate`.

The statutory hinge under the last row of the table is one article. Art. L. 132-23 CA withholds
*réduction* and *rachat* from *assurances temporaires en cas de décès* and from immediate or
in-payment life annuities, and withholds *rachat* from survivorship capitals, pure endowments
and deferred annuities without return of premium. `TD_FR_S` is squarely the first of those, so
it has no surrender value, no paid-up value and no cash-value machinery at any duration. A
whole-life funeral contract is none of them: it falls in the residual *autres assurances sur la
vie* class, where "*l'assureur ne peut refuser la réduction ou le rachat*" [R10] — which is why
this model needs a surrender scale, a *réduction* strand and a second population at all, and why
the chassis's "a lapse costs nothing" arithmetic must not be carried over.

---

## Model point attributes

| Attribute | Type | Example (worked configuration, RefOBS-VIA) |
|---|---|---|
| `point_id` | int | 1 |
| `sex` | enum {M, F} | M |
| `entry_age` | int (*différence de millésime*) | 50 [S14] |
| `capital_0` | currency (€) | 5000.00 [S14] |
| `premium_form` | enum {single, temporary, lifetime} | lifetime [S1] [S5] [S14] |
| `prem_term_y` | int (years of premium payment; 1 = single, 0 = lifetime) | 0, the value `premium_form = lifetime` implies [S1] [S5] [S14]; 5 / 10 / 15 / 20 / 25 are the documented temporary terms [S1] [S5] [S8] |
| `prem_cease_age` | int (attained age premiums stop; 0 = never) | 0 **[std]** (a) |
| `annual_premium` | currency (€/year) | 336.03 [S14] |
| `prem_freq` | int in {1, 2, 4, 12} | 1 **[std]** (b) |
| `carence_months` | int | 12 [S1] [S8] [S9] |
| `carence_refund_basis` | enum {gross, net_assistance, net_instalment} | gross [S1] |
| `carence_refund_rate` | float (interest on the refund, p.a.) | 0.00 [S1] [S8] [S9] |
| `accident_mult` | float (post-*carence* accidental multiplier) | 1.0 [S1] [S9] [S14]; 2.0 from year 2, subject to `accident_cap`, variant [S8] |
| `reval_rate` | float (annual capital revalorisation) | 0.0100 [S14] |
| `reval_prem_linked` | bool (remaining premiums uprated too) | false [S14]; true variant [S9] [S10] [S11] |
| `surr_penalty_years` | int | 0 [S1] [S11]; 10 variant [S8] |
| `surr_penalty_rate` | float | 0.00 [S1] [S11]; 0.05 variant [S8] |
| `reduction_share` | float (share of premium-stops becoming paid-up) | 0.00 **[std]** (c) |
| `issue_month` | int (calendar month of subscription) | 1 **[std]** (d) |

Footnotes:
- (a) **[std]** `prem_cease_age = 0`: whether lifetime premiums ever stop is not settled by the
  retrieved tables — one runs them to attained age 115 [S15], one to 95 [S5], one implies
  cessation near 90 from equal cumulative figures at ages 90 and 95 [S6], and one sells an
  explicit "to age 80" form [S9] [S10]. Never-ceasing is chosen because it is the documented
  design that produces the overrun this product is criticised for.
- (b) **[std]** `prem_freq = 1`: annual in advance, matching the contractual default [S1] and
  the published rate cards [S5] [S14]. Setting 12 requires the documented 2.2 % instalment
  loading [S11] to be applied to `annual_premium`, not a re-tariffing.
- (c) **[std]** `reduction_share = 0` in the base cell: *réduction* is contractually the normal
  consequence of non-payment [R7] [S1] [S8] [S9], but no public source gives any split between
  voluntary surrender and paid-up conversion — none gives any decrement rate at all. Zero keeps
  the worked example checkable; the recursion is specified below and the parameter is the
  sensitivity dial.
- (d) **[std]** `issue_month = 1`: **no retrieved document gives an issue month** and nothing in
  `_research/obseques.md` bears on one. It exists to make the age-basis approximation of the
  conventions section auditable rather than invisible. *Différence de millésime* steps on
  1 January [S1] [S8] [S9]; the model steps `age` at the policy anniversary; the two coincide
  exactly for a January issue and are out by up to one policy year of mortality otherwise. Every
  shipped model point sets 1, so the approximation is visible in the data rather than buried in
  a formula, and a user projecting real dates changes a column instead of a formula.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` = l(t) | Premium-paying policies in force; l(k) is measured at **time k months from issue**, l(0) = 1 | monthly (deaths, surrenders, *réductions*) |
| `pols_paid_up(t)` = l_r(t) | Paid-up (*réduit*) policies in force; l_r(k) at time k, l_r(0) = 0 | monthly (entries on *réduction*, exits on death) |
| `capital_pp(t)` | Guaranteed capital per policy, uprated by `reval_rate` | policy anniversaries |
| `cum_prem_pp(t)` | Premiums collected per policy to the BOM of month t — the *carence* refund base | monthly (premium months only) |
| `prem_ann(t)` | Current annual premium; rises with the capital when `reval_prem_linked` | policy anniversaries |
| `surr_value_pp(t)` | Surrender value = *provision mathématique* per policy | monthly |
| `reduced_capital_pp(t)` | Paid-up capital fixed at the date of *réduction* | on conversion |
| `in_carence(t)` | Indicator `t < carence_months` | monthly |
| `age(t)` | Attained age = `entry_age + floor(t/12)` | policy anniversaries |

**l is a time-point function, and on a 0-based frame it lines up exactly.** These notes carry
l(k) and l_r(k) at **time k months from issue**, l(0) = 1 at issue; the model indexes its
counts at the **start** of the month, and the start of month t is time t, so `pols_if(t)` is
l(t) and `pols_paid_up(t)` is l_r(t) with no offset at all. That is the quantity the worked
example prints — its column is headed `pols_if(t)` — and it is the weight the model applies to
every cash flow of month t. The end-of-month count is l(t+1), which the model publishes as
`pols_if_at(t, "AFT_DECR")`. The convention is restated in the `Projection` docstring's symbol
map, which is the authority for which cells name carries which symbol.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Cover | Whole life, no term, no maturity, no survival benefit | [S1] [S8] [S9] [S11] |
| Underwriting | Guaranteed acceptance; no medical questionnaire or examination | [S1] [S11] [S12] [S13] |
| *Délai de carence* | 12 months; accidental death pays the full capital from day 1; non-accidental death inside it pays the premiums collected | [S1] [S8] [S9] [S11] [S13] |
| Interest on the refund | None | [S1] [S8] [S9] |
| Refund netting | Gross premiums collected [S1]; **net of the assistance premium of 12 €/year** at one insurer [S8]; net of instalment charges at another [S9], quantified only as the 2.2 % annual-to-monthly loading [S11] | [S1] [S8] [S9] [S11] |
| Accidental-death cap | **20000 €** on the doubled accidental benefit at the one insurer that doubles it; that insurer's aggregate cap is 10000 €, or 20000 € where death follows an accident from year 2 | [S8] |
| Accident definition | Sudden, unforeseeable, non-intentional external cause — a near-identical core wording at both contracts that give one [S1] [S8]. The exclusions differ: **cerebral and cardio-vascular events are never accidents, whatever their origin**, at [S1] only, echoed by the market description, which adds myocardial infarction, coronary conditions and emotional shock [R21]; [S8] instead excludes acute and chronic illness and harm from medical or surgical treatment | [S1] [S8] [R21] |
| Suicide | Excluded in the first 12 months, and for a year after a capital increase | [S1] [S8] [S12] [S13] |
| Excluded-cause benefit | The *valeur de rachat* / *provision mathématique* — not zero | [S1] [S8] [S12] |
| Premium level | Fixed at inception; the premium form is final | [S1] [S5] [S6] [S7] [S14] [S16] |
| Revalorisation | 1.00 % p.a. of the capital, guaranteed, premiums unchanged | [S14] |
| First uprating | At the first anniversary — contracts must be in force at least a year | [S1] [S9] |
| Surrender | Total only, at the *provision mathématique*. At any time [S1] [S9] [S12]; at one insurer only once **one annual premium** has been paid [S8]. Settlement within 30 days [S1] [S8], **2 months** at another [S9] [S11] | [S1] [S8] [S9] [S11] [S12]; statutory basis [R10] [REG-R31] |
| Non-payment | 10 days, then 40 days' formal notice with **cover suspended**, then termination or *réduction* | [R7] [S1] [S8] [S9] |
| *Renonciation* | 30 calendar days, full refund of all premiums | [S1] [S8] [S11] [R7] [REG-R29] |
| Capital earmarking | Capital earmarked to the funeral up to its cost; funeral firm is first-rank beneficiary | [R2] [REG-R38] [S1] [S8] [S9] [S12] |

### (b) Insurer-discretionary current elements

Unlike the UK sibling, where this class is nearly empty, it carries real weight here — a French
funeral contract is a **participating** contract and the capital moves.

- **The revalorisation rate.** Discretionary at five of the seven insurers — PB credited
  annually to the capital [S1], by board decision for contracts in force at least a year [S8],
  through a *fonds de revalorisation* [S9], "*peut* être majoré" [S15], and on a published
  formula [S16] — set annually out of the *participation aux bénéfices* [S1] [S8] [S9] [S15]
  [S16];
  one publishes its formula — PB equals **90 % of technical and financial profits, after a 1 %
  management charge on funds under management and after the technical interest guaranteed at
  inception** (art. A 335-1 CA) [S16] [REG-R23]; one makes it a contractual guarantee at 1 % p.a.
  [S14], the only guaranteed rate retrieved anywhere. The statutory machinery (art. L. 331-3 CA
  [REG-R14], the *compte de participation aux résultats* at arts. A. 132-10 to A. 132-15
  [REG-R15], the eight-year release horizon of the *provision pour participation aux bénéfices*
  at art. A. 132-16 [REG-R16]) is documented once for the library in
  `../assurance_vie_euro/technical-notes.md` and is **not restated here**; this model consumes a
  declared rate and does not project a PB account. **No insurer's actually declared PB rate for
  a funeral contract in any year was found in any public source**; the only anchor besides the
  guarantee is 1.2854 % p.a., derived from a KID scenario [S11].
- **Whether the premiums are uprated with the capital.** No at five insurers [S5] [S6] [S7]
  [S14] [S16]; **yes, in the same proportion on the remaining premiums**, at one [S9] [S10]
  [S11]; not stated at a sixth [S1] — [unverified] there. A first-order fork, carried as
  `reval_prem_linked`.
- **The tariff.** A model point input. The standardised tables [S5] [S6] [S7] [S10] [S14] [S15]
  [S16] are the only public rate card, they state that they have no contractual value, and no
  insurer publishes the mortality table, technical rate, expense loading or margin behind them.
- **The technical rate at inception.** Two fragments exist in the whole retrieved set: **0.75 %
  with table TH 00-02** [S8] and **0 %** in a worked example [S1]. The statutory ceiling for a
  periodic-premium contract is the lower of 3.5 % and 60 % of the reference TME [REG-R17].
- **Charge levels within the disclosed maxima.** Art. A. 132-8 CA requires charge maxima to be
  disclosed in the *encadré*, not limited [REG-R30]; the observed maxima are in
  `product-spec.md` Table 7.

### (c) Behavioral / experience assumptions (modeler's view)

**Nothing in this class is sourced.** The research file's finding is blunt: no public source
gives any lapse, surrender or paid-up rate for this product, no mortality experience for
guaranteed-issue funeral lives, and no split of deaths between accidental and other causes.
Every figure below is a **[std]** drafting construction, to be replaced by experience.

| Input | Reference basis | Tag |
|---|---|---|
| Base mortality `q_base(x, sex)` | French population mortality by sex and single year of age, from INSEE [REG-R24], as a proxy for TH 00-02 / TF 00-02 | **[std]** (e) |
| Anti-selection loading `f_as` | **1.25**, level across durations and ages | **[std]** (f) |
| Select uplift `s(y)` | **1.60 / 1.30 / 1.15 / 1.00** for policy years 1 / 2 / 3 / 4+ | **[std]** (f) |
| Mortality improvement | None in base; a flat **0.8 % p.a.** reduction is the sensitivity proxy | **[std]** (i) |
| Accidental share of deaths `d_acc` | **0.05**, level | **[std]** (g) |
| Surrender / lapse `lapse_rate` | **6 % / 5 % / 3.5 % / 2.5 %** for policy years 1 / 2 / 3–5 / 6+ | **[std]** (h) |
| Paid-up share `reduction_share` | 0 in base; 0.5 as the variation | **[std]** (c) |
| Acquisition expense | **150 €** per policy at t = 0, commission included | **[std]** (j) |
| Maintenance expense | **24 €** per policy per year, 2.00 €/month, inflating **1.8 % p.a.** | **[std]** (j) |
| Claim handling | Folded into maintenance | **[std]** (i) |

Footnotes:
- (e) **[std]** base mortality: the decrement CSVs are proxies built from the INSEE population
  series [REG-R24] and anchored so that the model reproduces the placeholder rate stated in the
  worked example exactly. TH 00-02 / TF 00-02 are the regulatory tables here — named by two
  insurers [S8] [S11], homologated by the arrêté du 20 décembre 2005 [REG-R22] and annexed to
  art. A. 335-1 CA with their *décalage d'âge* schedules [REG-R23] — and are **cited by name and
  never redistributed**, per the house rule for restricted tables.
- (f) **[std]** anti-selection, and the direction of it. Acceptance is guaranteed — no medical
  questionnaire, no examination, entry to 84 or 85 [S1] [S8] [S11] [S12] [S13] — so the pool
  **cannot be better than population and self-selects worse**: an applicant who knows their
  prognosis has every reason to buy, and the only device standing against them is the
  twelve-month waiting period [R21]. The loading is therefore upward relative to population
  mortality, and it is **not flat in duration**: the excess sits at short durations and decays as
  the anti-selected cohort dies out. The first-year factor is the largest (1.60) even though a
  first-year illness death costs only a refund — the deaths still happen, they merely cost less,
  and moving the excess to year 2 would double-count the protection the *carence* already gives.
  The magnitude has no public calibration of any kind; the direction and the shape are the
  defensible part.
- (g) **[std]** accidental share 5 %: the contractual definition is **narrower than
  external-cause mortality**. Cerebral and cardio-vascular events are excluded whatever their
  origin at the one contract that says so [S1], and the market description adds myocardial
  infarction, coronary conditions and emotional shock [R21]; the other contract that defines an
  accident does not carry that carve-out but excludes acute and chronic illness and harm from
  medical or surgical treatment instead [S8]; the burden of proof is on the claimant [S1]; and a
  medical certificate stating the cause is required for any claim inside the waiting period [S1]
  [S8] [S9]. 5 % is set below any plausible external-cause share for those reasons, and level
  because no age split was found. It matters only inside the waiting period — where it is the
  whole of the difference between a refund and a capital.
- (h) **[std]** lapse shape: declining with duration, on the reasoning that a small-premium
  *prévoyance* contract bought for one purpose is lapsed early or not at all, reinforced by a
  surrender value worth far less than the premiums paid for decades (784.01 € after 5 years
  against 1680.15 € of premiums in the worked cell [S14]). The 30-day *renonciation* with full
  refund [S1] [S8] [REG-R29] is treated as never-issued business, outside the projection.
- (i) **[std]** two items with no source and no material effect on the base run. **Mortality
  improvement** is off in the base projection; France has no publicly available insured-lives
  projection model comparable to the CMI's, so the 0.8 % p.a. flat reduction is a sensitivity
  dial rather than a basis. **Claim handling** costs are folded into the maintenance expense
  rather than charged per death, because no retrieved document separates them — the contract
  documents disclose *charges*, not the insurer's own expenses.
- (j) **[std]** expense levels: no French source publishes a currency expense assumption for
  this product. The anchors are the disclosed **charges**, which bound expenses from above and
  leave the margin — acquisition charges of 2.5 % to 5.38 % of the guaranteed capital, i.e.
  125 € to 269 € on a 5000 € capital [S8] [S9], and ongoing charges of 0.40 % p.a. of the capital
  plus 0.57 % p.a. while lifetime premiums are paid, i.e. 48.50 €/year on 5000 € [S1]. The [std]
  acquisition expense sits inside that range and the [std] maintenance expense at about half the
  ongoing charge. The only aggregate figure published anywhere is a PRIIPs reduction in yield of
  1.77 % p.a. over 30 years [S11]. Expense inflation has no source at all.

---

## Cash flow components and recursions

### Notation (defined once, used throughout; `product-spec.md` states the same mechanics with a 1-based contractual month label, t_spec = t + 1)

| Symbol | Meaning | Cells name |
|---|---|---|
| t | policy month, **0-based**: t = 0, 1, …, proj_len − 1 | — |
| y | policy year = floor(t/12) + 1 — the contractual, 1-based label | — |
| x(t) | attained age = `entry_age` + y − 1 (*différence de millésime* proxy **[std]**) | `age` |
| C(y) | guaranteed capital in policy year y | `capital_pp` |
| C_0 | capital at issue | `capital_0` |
| r | annual revalorisation rate | `reval_rate` |
| P(t) | premium due at BOM of month t | `prem_due_pp` |
| P_a(y) | annual premium in policy year y | `prem_ann` |
| K(t) | premiums collected to the BOM of month t | `cum_prem_pp` |
| n_car | waiting period in months | `carence_months` |
| V(t) | surrender value = *provision mathématique* | `surr_value_pp` |
| C_red(t) | paid-up capital on *réduction* | `reduced_capital_pp` |
| u(x) | single premium per 1 € of whole-life capital at attained age x | `single_prem_rate` |
| q(y) | annual mortality rate for policy year y | `mort_rate` |
| q_m(y) | monthly mortality = 1 − (1 − q(y))^(1/12) **[std]** | `mort_rate_mth` |
| w(y), w_m(y) | annual / monthly total premium-stop rate | `lapse_rate`, `lapse_rate_mth` |
| rho | share of premium-stops that become paid-up rather than surrendered | `reduction_share` |
| d_acc | accidental share of deaths | `acc_share` |
| k_adb | accidental multiplier after the waiting period (1 or 2 [S8]) | `accident_mult` |
| M_acc | cap on the accidental benefit, 20000 € [S8] | `accident_cap` |
| a_ass | assistance premium netted from the refund, 12 €/year [S8] | `assistance_prem_pp` |
| phi | annual-to-monthly instalment loading, 2.2 % [S11] | `instalment_load` |
| l(t) | premium-paying in force at time t months from issue; l(0) = 1 | `pols_if(t)` — the model indexes at the start of month t, which is time t |
| l_r(t) | paid-up in force at time t; l_r(0) = 0 | `pols_paid_up(t)`, same alignment |
| surr_scale(t) | the published scale for a *rachat* in month t; the table is keyed by **elapsed months** and read at t + 1, the months elapsed at the end of month t | `surr_scale_pp` |

Dimensional check: capital, premiums and benefits are €; q, w, d, rho are dimensionless; every
expected cash flow below is € per month per policy issued.

### Decrements and survivorship

      q(y)   = q_base(x(t), sex) x f_as x s(y),   capped at 1, and = 1 at x = omega
      q_m(y) = 1 - (1 - q(y))^(1/12)
      w_m(y) = 1 - (1 - w(y))^(1/12)

      l(t+1)   = l(t) x (1 - q_m(y)) x (1 - w_m(y)),                  l(0)   = 1
      l_r(t+1) = l_r(t) x (1 - q_m(y)) + l(t) x (1 - q_m(y)) x w_m(y) x rho,
                                                                      l_r(0) = 0

with y = policy_year(t), the policy year of the month whose decrements are being applied: l(t)
is the count at the **start** of month t and l(t+1) the count at the end of it, after month t's
deaths and premium-stops.

Deaths resolve before premium-stops. `w(y) = 0` for a *prime unique* cell and for any month
after `prem_cease_age`: there are no premiums left to stop paying, so no premium-stop decrement
applies **[std]**. Voluntary surrender by a paid-up policyholder is not modeled **[std]**.

### Premiums

      P(t)   = P_a(y)   if t is a premium month and t is inside the paying period
             = 0        otherwise
      K(t)   = K(t-1) + P(t),                             K(0) = P(0)
      P_a(y) = annual_premium x (1 + r)^(y-1)             if reval_prem_linked [S9] [S10] [S11]
             = annual_premium                             otherwise [S5] [S14] [S16]

A premium month is `t ≡ 0 (mod 12/prem_freq)`; the paying period is month 0 only
(*prime unique*), months 0 to 12·`prem_term_y` − 1 (*primes temporaires*), or every month until
`prem_cease_age` (*primes viagères*, unbounded when that is 0). The premium is level and fixed
at inception unless `reval_prem_linked` [S1] [S5] [S14].

### Death benefit and the délai de carence

      DB_acc(t)  = C(y)                             if t <  n_car    [S1] [S8] [S9]
                 = min( k_adb x C(y), M_acc )        if t >= n_car    [S8]
      R(t)       = K(t)                              gross            [S1]
                 = max( 0, K(t) - a_ass x y )        net_assistance   [S8]
                 = K(t) / (1 + phi) if prem_freq > 1 else K(t)
                                                     net_instalment   [S9] [S11]
      DB_ill(t)  = R(t) x (1 + i_ref)^((t+1)/12)     if t <  n_car    i_ref = carence_refund_rate = 0
                 = C(y)                              if t >= n_car

      claims_death(t) = l(t) x q_m(y) x [ (1 - d_acc) x DB_ill(t) + d_acc x DB_acc(t) ]
                        + l_r(t) x q_m(y) x C_red(t)

The refund is of premiums **collected**, so with an annual premium in advance it is a step
function, flat across the first twelve months, not a monthly accrual. R(t) carries the three
`carence_refund_basis` variants: gross [S1], net of the assistance premium of 12 €/year for each
year begun [S8], or net of instalment charges [S9] — the only published quantification of which
is the 2.2 % annual-to-monthly loading [S11], so that basis does nothing on an annual-premium
cell. The cap M_acc = 20000 € is applied past the waiting period only; inside it the accidental
benefit is already the full capital, so doubling it there would double-count the day-one cover.
The cap is **inert on every shipped model point**: the largest accidental benefit any of them
reaches is 18532.12 € — the doubled-benefit variant at the far end of the horizon, where the
5000 € capital has revalorised to 9266.06 € — so no figure in the worked example or the shipped
run depends on it. It is specified and coded anyway, because that is where the contract puts it
and a larger `capital_0` reaches it [S8]. A paid-up policy is past the waiting period by
construction and pays `C_red` for any cause.

### Revalorisation of the capital

      C(1)   = C_0
      C(y)   = C_0 x (1 + r)^(y-1)      for y >= 2                    [S14]

The uprating starts at the **first anniversary**, not at issue: PB is allocated to contracts in
force at least one year [S1] [S9]. `reval_simple = true` replaces the geometric form with
`C(y) = C_0 x (1 + r x (y-1))` — see `product-spec.md` footnote (g), where the reading of the
contractual wording is [unverified]. Nothing is uprated inside the waiting period on the illness
leg: that benefit is a refund of premiums, not a capital.

### Rachat and réduction

      V(t)              = surr_scale(t) x capital_0 / 5000 x (1 - pen(t))
      pen(t)            = surr_penalty_rate  if t < 12 x surr_penalty_years, else 0
      claims_lapse(t)   = l(t) x (1 - q_m(y)) x w_m(y) x (1 - rho) x V(t)
      C_red(t)          = V(t) / u(x(t))                                on conversion [S1] [S8]

`surr_scale(t)` is an **external input table**: the surrender value in € for a 5000 € capital
by **elapsed months from issue**, for the cell's entry age and premium form, linearly
interpolated in elapsed months between the published quinquennial anchors **[std]** and held
flat beyond the last one. That key is a duration, not the projection's 0-based month index, and
it does not move with the frame. A *rachat* resolves at the **end** of month t, by which time
t + 1 months have elapsed, so `surr_scale(t)` reads the table at t + 1: the first projected
month, t = 0, is one month into the contract at 13.07 € on the worked cell, and the published
five-year anchor of 784.01 € is the value of month t = 59. Each
grid carries **all nine** published anchors, at 60, 120, 180, 240, 300, 360, 420, 480 and 540
months, plus a month-0 anchor that is **[std]**; dropping an intermediate one and letting the
interpolation stand in for it moves the scale by as much as 11 % and can erase the shape the
table exists to show — one *temporaire* grid peaks at 5074 € at 25 years and then declines
[S2], and that peak is an anchor, not an interpolant. The anchors are transcribed from the
standardised tables [S2] [S5] [S14] [S15] and already embed that insurer's own revalorisation,
which is why `V(t)` is **not** additionally scaled by `C(y)`. **`surr_scale_table.csv` is the
source of truth for which anchor came from which document**: its `provenance` column names the
insurer, the entry age, the premium form and the source id for every row, and these notes,
`model.md` and `product-spec.md` restate it rather than define it. The
production alternative is a prospective *provision mathématique* on the tariff basis; it is not
the reference implementation because **no insurer publishes its tariff basis** — the whole
retrieved set contains one technical rate with a table (0.75 %, TH 00-02 [S8]) and one rate
alone (0 % [S1]).

`u(x)` is the single premium per 1 € of whole-life capital at attained age x, a second external
input table anchored on the published *prime unique* rate card — 0.854808 at 50, 0.909720 at 60
and 0.963912 at 70, from 4274.04 / 4548.60 / 4819.56 € per 5000 € of capital [S5] — interpolated
and extrapolated **[std]**. It serves twice: it prices the `single` premium form, and it turns a
mathematical provision into a *valeur de réduction*.

### Cash flow outputs (per policy issued, month t)

| Cash flow | Formula | Column |
|---|---|---|
| Premium income | `l(t) × P(t)` | `premiums` |
| Death outgo | per the formula above, both populations | `claims_death` |
| Surrender outgo | `l(t) × (1 − q_m) × w_m × (1 − rho) × V(t)` | `claims_lapse` |
| Acquisition expense | 150 € at t = 0 **[std]** (j) | `expenses` |
| Maintenance expense | `(l(t) + l_r(t)) × 2.00 × 1.018^(y−1)` **[std]** (j) | `expenses` |
| Paid-up conversion | **no cash flow** — a state change only | — |
| Post-mortem revalorisation | excluded **[std]** (conventions, above) [S1] [S8] [R8] [REG-R31] | — |
| Maturity outgo | **identically zero — there is no maturity** [S1] [S8] [S9] | — |

      liability_cf(t) = claims_death(t) + claims_lapse(t) + expenses(t) - premiums(t)
      net_cf(t)       = -liability_cf(t)

### Monthly processing order **[std]**

At month t — `t = 0` for the first — for the l(t) policies in force at its **start**:

1. **BOM** — premium `P(t)` received if t is a premium month inside the paying period; add it to
   `cum_prem_pp`. Paid-up policies skip this step.
2. **BOM** — acquisition expense at t = 0; maintenance expense for the month, on both the
   premium-paying and the paid-up populations.
3. **Anniversary** (t ≡ 0 mod 12, t > 0) — uprate `capital_pp` by `reval_rate`; uprate
   `prem_ann` by the same rate if `reval_prem_linked`; step `age`. The order matters: the capital
   in force during policy year y is the one set at the start of year y, and the premium collected
   at step 1 of that same month is the uprated one.
4. **EOM** — deaths at `mort_rate_mth(y)` applied to `pols_if(t)` and `pols_paid_up(t)`;
   benefit per the *carence* rules for the first population, `reduced_capital_pp` for the second.
5. **EOM** — premium-stops at `lapse_rate_mth(y)` on the survivors of step 4: a fraction `rho`
   converts to paid-up (state change, no cash flow, `reduced_capital_pp` fixed at that month's
   `surr_value_pp / single_prem_rate`), and `1 − rho` surrenders and is paid `surr_value_pp(t)`.
   No premium-stop decrement applies where no premium is due.
6. The survivors are `pols_if(t+1)` and `pols_paid_up(t+1)`, the counts at the start of the next
   month.

### Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each
is stated so that it can be turned into an assertion, and the figures quoted are from the worked
example below.

1. **Paying the full capital inside the *carence*.** The single worst error available here. In
   the worked cell it turns the first month's (t = 0) expected death outgo from 0.380884 into
   3.345618 (×8.78) and
   policy-year-1 death outgo from 4.4274 into 38.8893 — an 8.8× overstatement of the front end
   of the liability. Assert: for `t < carence_months`, the illness leg of `claims_death` uses
   `cum_prem_pp`, not `capital_pp`.
2. **Dropping the accident leg inside the *carence*.** The mirror-image error. Accidental death
   pays the **full capital from day 1** [S1] [S8] [S9]; treating the whole waiting period as a
   refund takes the first month's death outgo from 0.380884 to 0.224846, understating it by
   **41 %**, and
   policy-year 1 from 4.4274 to 2.6136. Assert `claims_death(0) > q_m(0) × cum_prem_pp(0)`.
3. **Accruing the refund base monthly when the premium is annual.** With `prem_freq = 1` the
   refund base is a **step**, constant at 336.03 through months t = 0–11. Accruing it as
   `annual_premium × (t + 1) / 12` gives 28.00 at t = 0 and understates policy-year-1 death outgo
   by **26 %** (3.2750 against 4.4274). Assert
   `cum_prem_pp(0) == cum_prem_pp(11) == annual_premium`
   for the annual cell.
4. **Revalorising too early, or revalorising the wrong thing.** PB accrues only to contracts in
   force at least a year [S1] [S9], so uprating at issue makes `capital_pp(0) = 5050.00` and
   overstates the year-1 accidental leg — assert `capital_pp(t) == capital_0` for `t < 12`. And
   the illness benefit inside the waiting period is a refund of premiums, not a capital: it must
   not carry `reval_rate`. `carence_refund_rate` (zero in every retrieved contract [S1] [S8]
   [S9]) is a different parameter and must not be confused with it.
5. **Measuring the overrun against the wrong capital, and off by a year.** Cumulative premiums
   first exceed the **original** 5000 € capital at t = 168 (policy year 15) and the **revalorised**
   capital at t = 204 (policy year 18) — three years apart. Separately, the standardised tables
   date their columns by the age at the **end** of the year, so their "age 65" column is this
   model's attained age 64 during policy year 15. Both conventions are defensible; silently
   mixing them moves the published crossover by up to four years.
6. **Letting lifetime premiums stop by accident.** If `prem_cease_age` is defaulted to anything
   non-zero, the *viagère* overrun disappears and with it the product's characteristic feature.
   Assert that a `lifetime` point with `prem_cease_age = 0` still has `prem_due_pp > 0` at
   attained age 100.
7. **Getting the revalorisation coupling backwards.** Applying capital uprating without the
   matching premium uprating on a point configured after the insurer that couples them [S9]
   [S10] [S11] understates premium income; applying the premium uprating on any of the five that
   do not [S5] [S6] [S7] [S14] [S16] overstates it. One flag, `reval_prem_linked`, read from the
   model point and never hard-coded.
8. **Treating lapse as free.** This is where the UK sibling's model is actively misleading.
   *Rachat* pays the *provision mathématique* [S1] [S8] [S9] [S12], so `claims_lapse` is
   non-zero from t = 0. Setting it to zero moves the undiscounted net stream of the worked
   cell from 2236.92 to 3242.81 — a **45 % overstatement**. Assert `claims_lapse(t) > 0` for
   every t with `lapse_rate > 0`.
9. **Treating *réduction* as termination.** Non-payment produces a **paid-up contract**, not an
   exit, wherever the surrender value is sufficient [R7] [S1] [S8] [S9]; routing every
   premium-stop to the exit removes a death liability the contract still owes. With
   `reduction_share = 0.5` the paid-up population must appear in `claims_death` and must pay
   `reduced_capital_pp`, not `capital_pp`.
10. **Applying a premium-stop decrement where no premium is due.** After `prem_cease_age`, in a
    *prime unique* cell and in the paid-up state there is nothing to stop paying, and a lapse
    decrement there silently destroys liability. Assert `lapse_rate_mth(t) == 0` in all three.
11. **Paying zero on an excluded death.** Suicide in year 1, war, nuclear and murder by a
    beneficiary do not extinguish the contract: the insurer pays the *valeur de rachat* or the
    *provision mathématique* [S1] [S8] [S12], so an exclusion modelled as a zero benefit
    understates outgo by exactly `V(t)` per excluded death.
12. **Using the wrong age basis, or flattening the loading.** The basis is *différence de
    millésime* [S1] [S8] [S9]; age last birthday shifts the whole mortality lookup by up to a
    year at entry, and the *décalage d'âge* schedules annexed to art. A. 335-1 CA [REG-R23] apply
    on top of it where a homologated table is used. Separately, the anti-selection excess belongs
    at durations 1–3 and is largest in year 1 even though a year-1 illness death costs only a
    refund; a flat loading understates the year-2 spike, the largest single step in the worked
    cell's death-outgo series.

---

## Policyholder behavior modeling

All dynamic formulas below are **[std]** reference constructions. No public French source gives
any lapse, surrender or paid-up rate for this product; the shapes are drafting assumptions with
the qualitative anchors cited.

- **Base premium-stop rate [std].** The duration-declining table above, converted monthly, zero
  wherever no premium is due. The declining shape follows from the surrender value: for the
  first two decades it is worth a fraction of the premiums paid (784.01 € against 1680.15 € at
  five years, 1574.90 € against 3360.30 € at ten [S14]), so an early lapser loses most of their
  money and a late one has nearly reached a full payout.
- **No *carence*-completion spike [std].** Nothing changes for the policyholder at t = 12
  except that the cover becomes worth having, so there is no incentive to lapse there; the
  year-1 rate is set highest instead, for affordability and buyer's-remorse attrition.
- **Overrun-aware lapse [std].** Sensitivity module, off in base:
  `lapse_rate(y) = lapse_rate_base(y) × (1 + beta × 1{cum_prem_pp(t) > capital_pp(t)})`,
  beta = 0.5. The rationale is the disclosure the CCSF asked for [R13] [R15] and the KID warning
  that total premiums may exceed the capital [S11]; beta is a pure stress dial.
- **Réduction versus rachat [std].** Where a surrender value exists, stopping payment and taking
  nothing is strictly dominated by reducing, so the economically rational `reduction_share` is
  high, and the contract makes *réduction* the default outcome of non-payment [R7] [S1] [S8]
  [S9]. Zero in base, 0.5 as the variation, 1.0 as the upper stress. It dominates the
  late-duration liability and must never be approximated by perturbing the lapse rate instead.
- **The 40-day suspension [std].** Cover is suspended during the formal-notice window [S1], so a
  death there pays nothing. Ignoring it is conservative and is what the base model does;
  modelling it as an immediate exit is not, because the policyholder may still pay and continue.
- **Capital increases and *renonciation* [std].** Increases are not modeled: anti-selective on a
  guaranteed-issue book, mitigated but not removed by the fresh waiting period on the increment
  [S1] [S8]. The 30-day cooling-off with a full refund [S1] [S8] [REG-R29] is modeled as
  never-issued business, outside the projection.

---

## Worked example

**Cell RefOBS-VIA.** Entry age 50 male (*différence de millésime*), guaranteed capital
`capital_0` = 5000.00 €, *primes viagères* of `annual_premium` = 336.03 € payable **annually in
advance for life** with no cessation age, revalorisation `reval_rate` = 1.00 % p.a. compound on
the capital with the premium unchanged, `carence_months` = 12 with the illness leg paying the
premiums collected and the accident leg the full capital, `accident_mult` = 1,
`reduction_share` = 0, no surrender penalty. The premium, the revalorisation rate and the
surrender-value scale all come from **one** document [S14]; the waiting-period design comes from
the three contracts that state one [S1] [S8] [S9], because that document's tables reference
*carences* without giving a duration.

Assumptions, each tagged. **Mortality [std]**, an illustrative placeholder attributable to no
table: `q_base(x) = 0.0040 × 1.09^(x−50)`, anti-selection `f_as` = 1.25, select uplift
`s(y)` = 1.60 / 1.30 / 1.15 / 1.00 for y = 1 / 2 / 3 / 4+, so `mort_rate` is 0.008000 in policy
year 1, 0.0070850 in year 2 and 0.0167086 in year 15. **Lapse [std]** 6 % / 5 % / 3.5 % /
2.5 % for years 1 / 2 / 3–5 / 6+, all of it surrender since `reduction_share` = 0. **Accidental
share [std]** `d_acc` = 0.05. Monthly conversion `q_m = 1 − (1 − q)^(1/12)` **[std]**, so
`mort_rate_mth` = 0.00066912 and `lapse_rate_mth` = 0.00514301 in policy year 1. **Surrender
scale** [S14], linearly interpolated in elapsed months **[std]** between the published anchors
0 / 784.01 / 1574.90 / 2346.97 / 3151.33 / 3980.74 / 4828.57 / 5659.93 / 6429.96 / 7135.11 € at
0 / 60 / 120 / 180 / 240 / 300 / 360 / 420 / 480 / 540 elapsed months, read at t + 1. Expenses
are omitted from the table for clarity; `age(t)` = 49 + y. All amounts in €, full precision
carried, displayed rounded. `t` is the 0-based policy month and `y = floor(t/12) + 1` beside it.

| t | y | capital_pp | cum_prem_pp | db_illness | surr_value_pp | pols_if(t) | premiums | claims_death | claims_lapse |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 5000.00 | 336.03 | 336.03 | 13.07 | 1.00000 | 336.03 | 0.38 | 0.07 |
| 5 | 1 | 5000.00 | 336.03 | 336.03 | 78.40 | 0.97129 | 0.00 | 0.37 | 0.39 |
| 11 | 1 | 5000.00 | 336.03 | 336.03 | 156.80 | 0.93793 | 0.00 | 0.36 | 0.76 |
| 12 | 2 | 5050.00 | 672.06 | 5050.00 | 169.87 | 0.93248 | 313.34 | 2.79 | 0.68 |
| 23 | 2 | 5050.00 | 672.06 | 5050.00 | 313.60 | 0.88387 | 0.00 | 2.64 | 1.18 |
| 59 | 5 | 5203.02 | 1680.15 | 5203.02 | 784.01 | 0.77719 | 0.00 | 2.39 | 1.81 |
| 119 | 10 | 5468.43 | 3360.30 | 5468.43 | 1574.90 | 0.65347 | 0.00 | 3.25 | 2.17 |
| 168 | 15 | 5747.37 | 5040.45 | 5747.37 | 2205.42 | 0.55752 | 187.34 | 4.50 | 2.59 |
| 179 | 15 | 5747.37 | 5040.45 | 5747.37 | 2346.97 | 0.53639 | 0.00 | 4.33 | 2.65 |
| 204 | 18 | 5921.52 | 6048.54 | 5921.52 | 2682.12 | 0.48896 | 164.30 | 5.27 | 2.76 |
| 239 | 20 | 6040.54 | 6720.60 | 6040.54 | 3151.33 | 0.42361 | 0.00 | 5.55 | 2.81 |
| 299 | 25 | 6348.67 | 8400.75 | 6348.67 | 3980.74 | 0.31507 | 0.00 | 6.72 | 2.63 |
| 359 | 30 | 6672.52 | 10080.90 | 6672.52 | 4828.57 | 0.21337 | 0.00 | 7.43 | 2.16 |
| 479 | 40 | 7370.61 | 13441.20 | 7370.61 | 6429.96 | 0.05748 | 0.00 | 5.46 | 0.77 |
| 539 | 45 | 7746.59 | 15121.35 | 7746.59 | 7135.11 | 0.01799 | 0.00 | 2.88 | 0.26 |

`db_accident` equals `capital_pp` in every row, at every duration, and is therefore not printed.
Over the full horizon (t = 0 to 755, 756 months, ending at attained age 112) the undiscounted
totals are: `premiums`
6184.01, `claims_death` 2941.20, `claims_lapse` 1005.89, and `net_cf` summing to +2236.92 before
expenses.

**Checks.** *Survivorship, a different way.* The monthly decrements must compound back to the
annual ones exactly, so the in-force at the end of policy year 1 is available in closed form:
l(12) = (1 − q(1)) × (1 − w(1)) = 0.992 × 0.94 = **0.93248** — the year-1 annual rates — which
is the `pols_if(t)` printed against t = 12. Carrying it one year further,
l(24) = 0.93248 × (1 − 0.0070850) × 0.95 = **0.87957971**; the row at t = 23 prints l(23), one
month earlier, at 0.88387. *The capital and the surrender value at t = 204, two ways.* Policy
year 18 has had 17 upratings, so `capital_pp` = 5000 × 1.01^17 = **5921.52**; equivalently, take
the year-15 figure already in the table and carry it three years, 5747.37 × 1.01³ =
5747.37 × 1.030301 = **5921.52**. The surrender value at the end of month t = 204 — 205 elapsed
months — interpolates between the published 180-
and 240-month anchors: 2346.97 + (3151.33 − 2346.97) × 25/60 = 2346.97 + 335.15 = **2682.12**.
*The t = 11 / t = 12 step.* Expected death outgo rises from 0.357242 to 2.789356, a factor of
**7.8080**, and it decomposes exactly into three independent moves: in-force
0.93248/0.93793 = 0.994191, monthly mortality 0.00059234/0.00066912 = 0.885251 (the select
uplift drops from 1.60 to 1.30 while the base rate rises 9 %), and benefit
5050.00/569.2285 = 8.871657 — because the blended benefit steps from
0.95 × 336.03 + 0.05 × 5000 = 569.2285 to the full uprated capital. The product
0.994191 × 0.885251 × 8.871657 = 7.8080 reproduces the ratio. That step is the signature
discontinuity of the product, and it is the reason the grid must be monthly.

**Subsidiary table — the premium-form fork.** The same 5000 € capital and entry age 50, priced
across three forms on a single published rate card [S5], with cumulative premiums by attained
age (age 65 = 15 annual premiums, 75 = 25, 85 = 35, 95 = 45):

| Premium form | Annual premium | Cum. to 65 | to 75 | to 85 | to 95 | First premium exceeding 5000 |
|---|---|---|---|---|---|---|
| *prime unique* | 4274.04 once | 4274.04 | 4274.04 | 4274.04 | 4274.04 | never |
| *temporaire* 10 ans | 455.64 | 4556.40 | 4556.40 | 4556.40 | 4556.40 | never |
| *viagère* | 164.52 | 2467.80 | 4113.00 | 5758.20 | 7403.40 | the 31st, at attained age 80 |

The *viagère* row is the whole argument about this product in six numbers: 164.52 × 31 =
5100.12 first exceeds the capital in policy year 31, and by policy year 45 the insured has paid
7403.40 € for 5000 € of cover — while the two other forms stop, permanently, below the capital.
The crossover in policy year 31 falls inside the age-80-to-84 band the same rate card produces
for entry ages 50 / 60 / 70. The worked cell above, priced by a different insurer at more than
twice the lifetime premium (336.03 against 164.52), crosses at policy year 15 instead.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; the valuation layers consume
them and are cited, not reproduced.

- **Solvabilité II best estimate.** The probability-weighted average of future cash flows
  discounted at the EIOPA risk-free term structure [REG-R1] [REG-R4] [REG-R5], plus a risk
  margin. No cost-of-capital rate, contract boundary or standard-formula shock in this library
  was read from a retrieved instrument [REG-R2], so every such figure would be **[std]**; the
  SCR and MCR layers are cited-not-specified.
- **The statutory *provision mathématique*.** The French GAAP balance sheet persists alongside
  Solvabilité II. The *provision mathématique* is the difference between the present values of
  the two parties' commitments **including future management costs**, the first of eleven named
  technical provisions [REG-R6] — and, for this product, the quantity the contract makes the
  surrender value equal to [S1] [S8] [S9] [S12]. A production model computes it prospectively on
  the tariff basis; this reference model reads a scale, for the reason given above.
- **Participation aux bénéfices.** The minimum PB is computed globally on the statutory accounts
  [REG-R14] [REG-R15], and amounts parked in the *provision pour participation aux bénéfices*
  must be allocated or paid within eight years [REG-R16]. A funeral capital's revalorisation is
  the visible end of that machinery; the machinery itself is modeled once in
  `../assurance_vie_euro/technical-notes.md`. Note the open question recorded in
  `product-spec.md`: the 85 % PB floor of art. L. 2223-34-1 CGCT is drafted for the *prestations*
  form and may not reach a pure capital contract [R3].
- **Technical rate and tables.** Any guaranteed rate inside the tariff is capped by art.
  A. 132-1 CA at the lower of 3.5 % and 60 % of the reference TME for a periodic-premium
  contract [REG-R17]. TH 00-02 / TF 00-02 are the homologated non-annuity tables [REG-R22],
  reproduced with their *décalage d'âge* schedules in the annexe to art. A. 335-1 CA, which
  permits only homologated or actuary-certified tables [REG-R23]. They are cited and never
  shipped; the decrement CSVs are INSEE-derived **[std]** proxies [REG-R24].
- **Unclaimed contracts.** Under the loi Eckert a death benefit unclaimed for ten years transfers
  to the Caisse des dépôts and becomes State property after twenty years there, with revalorisation
  continuing until the deposit [REG-R39]. Small capitals and elderly beneficiaries make this a
  live item for this product specifically.
- **IFRS 17 and professional standards.** Fulfilment cash flows plus a contractual service
  margin, effective from 1 January 2023 with no French carve-out [REG-R45]; the same projection
  feeds it with different discounting and aggregation. NPA 2 *Modèles actuariels*, a recommended
  practice in force from 1 January 2016, is the standard this documentation and its test suite
  sit under [REG-R44].

---

## Key sensitivities and model risks

In order of influence on a guaranteed-acceptance funeral block:

1. **Anti-selection mortality, and its duration shape.** The `f_as` = 1.25 loading and the
   `s(1..3)` = 1.60 / 1.30 / 1.15 select uplift are pure **[std]** placeholders: no experience
   study of guaranteed-issue French funeral lives exists in any public source. The interaction
   with the waiting period is the point — the refund design exists precisely because year-1
   non-accidental mortality is anti-selected — so the loading and the *carence* must be stressed
   **together**, never one at a time.
2. **The revalorisation rate.** It compounds on the benefit for the whole of a whole-life
   contract. At 1.00 % p.a. the capital is 7746.59 € at 45 years against 5000 € at issue; the
   only other numerical anchor available is 1.2854 % p.a. derived from a KID scenario [S11],
   and five of seven insurers make the rate discretionary [S1] [S8] [S9] [S15] [S16]. Run 0 % /
   1 % / 2 %. Where `reval_prem_linked` is set [S9] [S10] [S11] the sensitivity partly
   self-hedges, which is exactly why the flag must not be averaged across a book.
3. **Premium form mix.** A portfolio fact rather than a sensitivity, and unobserved: the
   proportion of contracts sold in each form is published nowhere. A *viagère* book and a
   *prime unique* book of the same capital have opposite cash flow shapes — a long premium stream
   against a slowly rising benefit, versus a single receipt followed by four decades of pure outgo.
4. **Premium-stop behaviour and the surrender / *réduction* split.** With a real surrender value
   the liability is not lapse-supported in the way the UK design is: in the worked cell zero
   lapse *raises* the undiscounted net stream from 2236.92 to 3165.11, because the premiums a
   lapser stops paying are worth more than the reserve handed back. Run 0.5× / 1× / 2× base
   lapse, zero lapse, and `reduction_share` at 0 / 0.5 / 1.0. The discounted, expense-inclusive
   answer can differ in sign from the undiscounted one and should be checked separately.
5. **Longevity at the top of the table, against a fixed premium.** A *viagère* policy issued at
   50 is still paying premiums at 90 and the model is still projecting at 112; improvement
   assumptions lengthen the premium stream and defer the claim, and the horizon convention
   (omega = 112 **[std]**, against tables running to 115 [S15]) is itself an assumption. Over
   that horizon maintenance expenses inflate against a premium that by construction cannot move
   — unless `reval_prem_linked` is set, the one design in the set that indexes it [S9] [S10] [S11].
6. **Basis mixing.** The surrender scale, the premium and the revalorisation rate of the worked
   cell come from one insurer [S14] precisely so that they are consistent. Feeding one insurer's
   premium into another's surrender scale produces plausible-looking and wrong margins: the
   lifetime premium for the same capital spans 2.0:1 across the retrieved set at entry age 50,
   narrowing to 1.7:1 at 60 and 1.5:1 at 70.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-obseques-r10
[R13]: #frlib-obseques-r13
[R15]: #frlib-obseques-r15
[R2]: #frlib-obseques-r2
[R21]: #frlib-obseques-r21
[R3]: #frlib-obseques-r3
[R7]: #frlib-obseques-r7
[R8]: #frlib-obseques-r8
[REG-R1]: #frlib-reg-r1
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R38]: #frlib-reg-r38
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
