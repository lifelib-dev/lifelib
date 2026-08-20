# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `_research/critical-illness.md`); [REG-R#]
tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks
claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`. The model mirrors the term assurance reference model in
`products/term_assurance/` (base chassis); only CI-specific mechanics are new here.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums, main
  claims, additional-payment claims, children's-cover claims, expenses) for a
  single-policy model point of accelerated (and, as a variant, standalone) Critical
  Illness Cover. Discounting, reserves and capital are not computed (see Valuation and
  reserve pointers).
- **Projection frequency.** Monthly grid over the policy term (12 x term months)
  **[std]**. The contract itself has no accumulation account; monthly is chosen for
  parity with the other reference models in this library.
- **Timing conventions [std].** Premiums and maintenance expenses at the beginning of
  the policy month (BOM); claims and decrements at the end of the policy month (EOM).
  Annual decrement rates are converted to monthly via
  `q_m = 1 − (1 − q_annual)^(1/12)`; small frequency loadings may use the `rate/12`
  approximation, stated where used.
- **Age basis.** Age nearest birthday (ANB) **[std]**; attained age advances on policy
  anniversaries. Chosen for consistency with the CMI assured-lives table conventions
  [unverified — the convention of the restricted tables was not confirmed from a
  fetched document]; any consistent basis works if used for *all* lookups.
- **Currency.** GBP. All amounts per single policy.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  Joint life first event is a variant (two-life survivorship product) **[std scope:
  not in base]**.
- **Survival period.** 14 days [S1] [std pick, see product-spec footnote 9]. In the
  accelerated base model it is cash-flow-neutral (death within 14 days of diagnosis
  pays the same `SA` as a death claim [S1]) and is ignored as a timing refinement
  **[std]**. In the standalone variant it reduces payable claims (below).
- **Rounding.** Intermediate values at full precision; displayed to pence **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `contract_type` | enum {accelerated, standalone} | accelerated |
| `issue_age` | int (ANB) | 40 |
| `sex` | enum {M, F} | M |
| `smoker` | enum {NS, S} | NS |
| `sum_assured` | currency (SA) | 100,000 **[std]** |
| `term_years` | int (5–50 [S2] [S5]) | 25 **[std]** |
| `cover_basis` | enum {level} (decreasing/FIB out of scope) | level |
| `life_basis` | enum {single, joint_first_event} | single **[std]** |
| `premium_guarantee` | enum {guaranteed, reviewable} | guaranteed [S1] |
| `premium_monthly` | currency | 55.00 **[std]** (no public rate cards — placeholder) |
| `premium_mode` | enum {monthly, annual} | monthly **[std]** |
| `children_cover` | bool (automatic on the composite [S1]) | true |
| `indexation` | bool (increasing-cover option; base: false) | false **[std]** |
| `issue_date` | date | month 1 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at end of month t; l(0) = 1 | monthly decrements |
| `t` / `y` / `a` | Policy month; policy year = ceil(t/12); attained age = issue_age + y − 1 (ANB) | monthly |
| `P(t)` | Premium rate in force (constant under guaranteed premiums; reset at reviews in the reviewable module) | at reviews only |
| `SA(t)` | Sum assured (constant at SA for level cover; indexation module updates annually) | on events |
| `grace_flag(t)` | In-grace indicator (60-day grace [S1] [S4]) — deterministic base model does not enter grace | monthly |
| `n_AP_used` | Additional-payment claims used per condition (contract cap: 1 per condition [S11]) — not tracked in the frequency-loading approximation **[std]** | — |
| `n_child_used` | Children's claims used (cap 2 [S1]) — not tracked in the frequency-loading approximation **[std]** | — |

There is no account value, asset share, surrender value, bonus, or MVR state in this
product: lapse pays nothing [S1] [S4] [S5] [unverified as explicit statement].

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Main benefit | SA on first of death / TI / CI diagnosis + survival (accelerated); CI only (standalone) | [S1] [S4] [S8] [S11] |
| Additional-payment benefit `B_AP` | min(0.25 x SA, 25,000) = 25,000 at the anchor cell; non-depleting | [S1] [S4] [S11] |
| Children's benefit `B_ch` | min(0.50 x SA, 25,000) = 25,000 at the anchor cell; non-depleting; 2-claim policy cap | [S1] |
| Child funeral benefit | 4,000 — excluded from the base model (de minimis) | [S1]; exclusion **[std]** |
| Survival period | 14 days | [S1]; pick **[std]** |
| Premium | Level, guaranteed for the term; 60-day grace, no surrender value | [S1] [S4] |
| Term / expiry | 5–50 years; policy ends by 75th birthday | [S2] [S5] |

### (b) Insurer-discretionary current elements (snapshot)

Guaranteed-premium CIC has almost no discretionary machinery — there are no bonus
rates, no asset shares, no MVRs. Two snapshot elements exist:

| Input | Snapshot value | Basis |
|---|---|---|
| Reviewable-premium reviews (variant module only) | Reviews every 5 years from the 5th anniversary; changes driven by claims/industry experience, medical advances, law; one carrier: "no limits" on changes, <2% or 50p ignored; another's intermediary variant: ±5% tolerance, individual health not a factor. Snapshot: premiums unchanged at each review **[std]** | [S3] [S4] [S5] |
| Indexation basis (if `indexation = true`) | RPI snapshot 3.0% p.a. **[std]** → cover +3.0%, premium +4.5% (x1.5 factor), within caps 10%/15% | mechanics [S1] [S4]; RPI level **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

The CMI's critical illness investigation covers standalone and full accelerated
(death + CI) business, on a diagnosis-rate approach: AC04 insured-lives accelerated-CI
diagnosis-rate tables (WP50, 2003–2006 experience), cause-specific rates (WP52, updated
WP151), and CIBT93 as the population-based comparison table [R8] [R9]. The current
protection base-table generation is the "16" Series (term assurance mortality and
accelerated CI, 2015–2018 experience, finalized with WP154) [REG-R26]; the latest
public experience output is WP167 (accelerated CI by cause, 2017–2020) [R9]. **Honest
flagging:** CMI working papers are public, but current CMI tables and datasets are
restricted to Authorised Users (subscribers) [REG-R22] [R9 — access limits](#uklib-critical_illness-r9) [unverified]; AC04/16-Series rate values were not obtained. The reference basis below
is therefore a **[std] proxy** shaped like the named tables, to be replaced by a
licensed basis in any real application.

| Input | Reference basis | Basis tags |
|---|---|---|
| CI diagnosis rates `i_ci(x)` | [std] proxy table below, shaped like an insured-lives accelerated-CI diagnosis-rate table (AC04/16-Series structure: sex/smoker-distinct, age-increasing) | structure [R8] [REG-R26]; values **[std]** |
| Mortality `q_d(x)` | [std] proxy table below, shaped like ~0.70 x ONS National Life Tables qx (population mortality is heavier than insured experience; scalar and pivot values are rounded placeholders, not derived ONS data) | ONS tables redistributable [REG-R32]; values **[std]** |
| Overlap factor `k` | 0.10 flat (see combined decrement below) | **[std]** |
| Standalone survival-period slippage `δ` | 0.03 (fraction of diagnoses dying within 14 days) | **[std]** |
| Additional-payment frequency | `a(x) = 0.15 x i_ci(x)`, non-terminating | **[std]** |
| Children's-cover claim frequency | `λ_ch = 0.0004` p.a. per policy, non-terminating, while children_cover active | **[std]** |
| Lapse `w(y)` | [std] table below; no dynamic lapse in base | **[std]** |
| Mortality/morbidity improvement and CI trend `τ` | 0% p.a. in base; if an improvement overlay is required, express as "CMI_20xx with long-term rate p% [std]" | [REG-R30]; base **[std]** |
| Expenses | Initial 200 per policy; maintenance 30 p.a. inflating 3% p.a.; claim expense 250 per main claim | **[std]** |

[std] proxy diagnosis and mortality rates (annual, male non-smoker; pure placeholders
— NOT CMI or ONS values; interpolate log-linearly between pivot ages **[std]**):

| Age x | 40 | 45 | 50 | 55 | 60 | 65 |
|---|---|---|---|---|---|---|
| `i_ci(x)` | 0.0015 | 0.0025 | 0.0040 | 0.0070 | 0.0110 | 0.0170 |
| `q_d(x)` | 0.0009 | 0.0014 | 0.0022 | 0.0036 | 0.0060 | 0.0100 |

[std] lapse table (annual rates; protection-book shape, calibration to be replaced by
the user's experience — UK CI lapse studies are proprietary):

| Policy year | 1 | 2 | 3–5 | 6+ |
|---|---|---|---|---|
| `w(y)` | 10% | 8% | 6% | 4% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1..12n (n = term_years); y = ceil(t/12); a = attained age (ANB) |
| `SA` | sum assured (100,000 at the anchor cell) |
| `P` | monthly premium (55.00 **[std]** at the anchor cell) |
| `i_ci(a)` | annual CI diagnosis rate (first diagnosis of a listed condition, incl. TPD) |
| `q_d(a)` | annual best-estimate mortality rate |
| `k` | overlap: proportion of deaths that follow a CI diagnosis that already gave rise to (or would give rise to) a claim in the same year (0.10 **[std]**) |
| `q_claim(a)` | annual combined claim decrement (accelerated), defined below |
| `q_m(t)`, `w_m(t)` | monthly claim and lapse rates: `1 − (1 − annual)^(1/12)` |
| `a_m(t)` | monthly additional-payment frequency ≈ `0.15 x i_ci(a) / 12` **[std]** |
| `λ_m` | monthly children's claim frequency ≈ `λ_ch / 12` = 0.0000333 **[std]** |
| `B_AP`, `B_ch` | 25,000 and 25,000 (anchor cell; see contractual inputs) |
| `E0`, `E_m(y)`, `E_cl` | initial expense 200; maintenance `30/12 x 1.03^(y−1)` per month; claim expense 250 **[std]** |
| `l(t)` | in-force probability at end of month t; l(0) = 1 |
| `δ` | standalone survival-period slippage (0.03 **[std]**) |
| `τ` | CI trend rate (0 in base **[std]**) |

Dimensional check: all benefit amounts are GBP; `q_m`, `w_m`, `a_m`, `λ_m` are
dimensionless monthly probabilities/frequencies; every cash-flow line below is
GBP/month per policy in force at the relevant weighting.

### Combined decrement for accelerated CI

The insured event is *death or first CI diagnosis, whichever first* — the CMI's
accelerated investigation measures exactly this combined claim incidence with
cause-of-claim splits [R8] [R9]. Adding `q_d` and `i_ci` naively double-counts lives
that are both diagnosed and die in the same period: once the CI claim has been paid
(diagnosis + 14-day survival), the subsequent death of that life is not a second
claim; and a death within the survival period converts the CI claim into a death claim
of the same amount rather than adding one. The classical independent-rates
formulation is diagnosis rates plus mortality net of the overlap
[unverified as a market-practice statement — recorded as such in the research file]:

    q_claim(a) = i_ci(a) x (1 + τ)^(y−1) + q_d(a) x (1 − k)          [std]

where `k` is the proportion of deaths preceded by a claimable CI diagnosis (deaths
"already counted" in `i_ci`). **[std] simplification:** `k = 0.10`, flat across ages,
in the absence of public cause-of-death-linked CI data (the cause-specific splits in
WP52/WP151/WP167 [R8] [R9] are the right calibration source for subscribers).
Sensitivity range 0–0.25 (see Key sensitivities). The 14-day survival period needs no
further adjustment in the accelerated design: whichever way the overlap resolves, `SA`
is paid once [S1].

### Standalone variant deltas

Death pays nothing; the policy simply terminates. Decrement splits into paying and
non-paying parts **[std]**:

    q_pay(a)  = i_ci(a) x (1 + τ)^(y−1) x (1 − δ)        — CI claims paid (survive 14 days)
    q_exit(a) = q_d(a) x (1 − k) + i_ci(a) x (1 + τ)^(y−1) x δ
                                                          — deaths without payment, incl.
                                                            deaths within the survival period

Total decrement `q_claim = q_pay + q_exit` (same in-force runoff as the accelerated
model at these parameters); only the *paid* part generates claim outgo. Death within
the survival period pays nothing on the composite standalone variant [S4] [S11]; a
premium-refund-on-death feature exists in some designs [S4] [S11 — recorded jointly in
the research file] and is excluded **[std]**.

### Monthly processing order [std]

At BOM of month t:

1. Premium income: `P x l(t−1)` (survivors at the start of the month pay).
2. Maintenance expense: `E_m(y) x l(t−1)`. (Initial expense `E0` at t = 1 only,
   weight 1.)

At EOM of month t:

3. Main claim decrement: expected claim outgo `SA x q_m(t) x l(t−1)` (accelerated;
   standalone uses `q_pay_m`), plus claim expense `E_cl x q_m(t) x l(t−1)`.
4. Additional-payment claims (non-terminating — do NOT decrement `l`):
   `B_AP x a_m(t) x l(t−1)`.
5. Children's-cover claims (non-terminating — do NOT decrement `l`):
   `B_ch x λ_m x l(t−1)`.
6. Lapse applied to non-claiming survivors; update in-force:
   `l(t) = l(t−1) x (1 − q_m(t)) x (1 − w_m(t))` **[std order: claim before lapse]**.
7. At t = 12n (term end): policy expires; no maturity or surrender value
   [S1] [S4] [S5].

The frequency-loading treatment of steps 4–5 deliberately ignores the contractual
claim-count caps (1 per additional-payment condition [S11]; 2 children's claims [S1])
and the per-child cross-policy cap (£50,000 [S1]): at the [std] frequencies the
probability of hitting a cap is second-order. Exact treatment would need claim-count
state variables (`n_AP_used`, `n_child_used`).

### Cash flow outputs (per policy, month t)

| Cash flow | Formula | Sign | Timing |
|---|---|---|---|
| Premium income | `P x l(t−1)` | + | BOM |
| Initial expense | `E0` at t = 1 | − | BOM |
| Maintenance expense | `E_m(y) x l(t−1)` | − | BOM |
| Main claims | `SA x q_m(t) x l(t−1)` (standalone: `q_pay_m`) | − | EOM |
| Claim expenses | `E_cl x q_m(t) x l(t−1)` | − | EOM |
| Additional-payment claims | `B_AP x a_m(t) x l(t−1)` | − | EOM |
| Children's-cover claims | `B_ch x λ_m x l(t−1)` | − | EOM |
| Surrender outgo | 0 (no surrender value [S1] [S4] [S5]) | — | — |

Grace (60 days [S1] [S4]) is not separately modeled in the deterministic base: lapse
rates are assumed to already reflect grace-period cures **[std]**. Death during grace
pays the death benefit less unpaid premiums [term chassis]; immaterial at monthly
resolution **[std]**.

### Reviewable-premium module (variant)

For `premium_guarantee = reviewable`: `P(t)` is constant between reviews; at each
5-yearly review from the 5th anniversary [S3] [S4], `P ← P x (1 + ρ_review)` where
`ρ_review` is a scenario input (snapshot 0 **[std]**). Contractual constraints: one
carrier's form — no limits, changes under 2% or 50p ignored, policyholder may instead
reduce cover [S4] [S5]; another's intermediary form — ±5% tolerance per review,
individual health not a factor [S3]. A review-driven lapse response belongs in behavior
modeling (below). Premium rates for in-force reviewable business are insurer-discretionary
current elements — class (b) snapshots, not guarantees.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; UK CI lapse experience
studies are proprietary, so shapes are stated with rationale and no source is cited
for calibration.

- **Base lapse [std].** `w(y)` per the table above, converted monthly. Rationale:
  protection lapse is duration-skewed (early years highest — buyer's remorse,
  remortgaging, distribution churn) and levels off in later durations.
- **No interest-sensitive lapse.** There is no cash value or credited rate to arbitrage;
  the interest-sensitive dynamic-lapse machinery of the accumulation products in this
  library is deliberately absent **[std]**.
- **Premium-review shock (reviewable module only) [std].**
  `w_shock = min(0.30, w(y) + 2.0 x max(0, ρ_review − 0.05))` applied in the 12 months
  following a review that raises premiums by more than 5%. Rationale: one carrier's
  unlimited review changes [S4] make review-driven shocks the dominant behavioral risk
  on reviewable business; slope and cap are placeholders.
- **Selective lapsation [std].** Optional morbidity-anti-selection overlay: after a
  lapse-shock event, remaining lives carry `i_ci x (1 + η)` with `η = 0.10`.
  Rationale: healthier lives lapse first when premiums rise; magnitude is a
  placeholder.
- **Indexation take-up (if indexed) [std].** Declining an increase 3 years in a row
  removes the option [S1] [S4]; base model assumes full take-up while active.
- **GIO / life-change option exercises.** Excluded from the base model point **[std]**;
  exercise creates a new policy/increase at current rates without underwriting
  [S1] [S4] [S11] — an anti-selection cost that a production model should load for.

---

## Worked example

Anchor cell: male 40 non-smoker, accelerated, SA = £100,000, term 25 years, level
guaranteed premium P = £55.00/month **[std]**. Age-40 assumptions: `i_ci` = 0.0015
**[std]**, `q_d` = 0.0009 **[std]**, `k` = 0.10 **[std]**, `τ` = 0 →
`q_claim = 0.0015 + 0.0009 x 0.90 = 0.00231` annual;
`q_m = 1 − (1 − 0.00231)^(1/12) = 0.00019270`. Year-1 lapse 10% →
`w_m = 1 − 0.90^(1/12) = 0.0087416`. `a_m = 0.15 x 0.0015 / 12 = 0.00001875`;
`λ_m = 0.0004 / 12 = 0.0000333`. `B_AP = B_ch = 25,000`. Maintenance
`E_m = 30/12 = 2.50` (year 1); claim expense 250; initial expense £200 at t = 1 (not
shown in the table). Survivor factor per month:
`s = (1 − q_m)(1 − w_m) = 0.9998073 x 0.9912584 = 0.9910674`.

| Month t | l(t−1) | Premium `P·l` | Main claim `SA·q_m·l` | Claim exp `250·q_m·l` | Add-pay `B_AP·a_m·l` | Child `B_ch·λ_m·l` | Maint `E_m·l` | Net CF | l(t) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 55.00 | 19.27 | 0.05 | 0.47 | 0.83 | 2.50 | 31.88 | 0.991067 |
| 2 | 0.991067 | 54.51 | 19.10 | 0.05 | 0.46 | 0.83 | 2.48 | 31.59 | 0.982215 |
| 3 | 0.982215 | 54.02 | 18.93 | 0.05 | 0.46 | 0.82 | 2.46 | 31.31 | 0.973441 |

Trace, month 1: premium 55.00 x 1; expected main claim 100,000 x 0.00019270 = 19.27;
claim expense 250 x 0.00019270 = 0.05; additional payment 25,000 x 0.00001875 = 0.47;
children's 25,000 x 0.0000333 = 0.83; maintenance 2.50. Net = 55.00 − 23.12 = 31.88
(31.88 − 200 initial expense = −168.12 in total month-1 cash flow).
l(1) = 1 x (1 − 0.00019270) x (1 − 0.0087416) = 0.991067. Note the additional-payment
and children's rows do not enter l(t): they are non-terminating loadings
[S1] [S3] [S4] [S8] [S11].

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers
consume them and are cited, not reproduced:

- **Solvency UK.** Technical provisions = best estimate + risk margin (Technical
  Provisions 2.4); best estimate = probability-weighted cash flows discounted on the
  risk-free term structure, gross of reinsurance, realistic assumptions, homogeneous
  risk groups (3.1–3.2, 9.1–9.2, 10.1) [R7] [REG-R1]. Risk margin: cost-of-capital
  method, CoC 4%, λ = 0.9 taper with floor 0.25, effective 31/12/2024
  [R7] [REG-R4]. The matching adjustment is in its own Rulebook Part [R7] and is in
  practice irrelevant to CI term business [unverified].
- **IFRS 17.** UK-adopted IFRS 17 (effective 1 January 2023) [REG-R38] measures these
  contracts as fulfilment cash flows plus CSM [mechanics summary: unverified — the
  standard text was not fetched]; the expected-cash-flow engine is the same
  projection, with regime-specific discounting, risk adjustment and aggregation.
- **Professional standards.** TAS 100 v2.0 applies to all technical actuarial work
  from 1 July 2023 [R10] [REG-R33]; TAS 200 v2.0 (insurance) applies from 1 January
  2025 [REG-R34].

---

## Key sensitivities and model risks

Dominant assumptions, in order:

1. **CI trend and condition-definition drift.** The dominant assumption risk for CI
   business: diagnosis rates trend with medical practice (earlier and wider
   diagnosis), and the covered event itself moves when the ABI revises model
   definitions — the 2021/22 review broadened Alzheimer's to all dementia, tightened
   cancer staging exclusions, and excluded myocardial injury from heart attack, with
   compliance by 31 January 2024 [R2] [R3]; prior reviews 2011, 2014, 2018 [R3].
   Definition changes produce *step* changes in `i_ci` that no trend parameter
   anticipates; sensitivity-test `τ` at ±2% p.a. **[std]** and re-map the incidence
   basis at each definition-review generation.
2. **Level and shape of the diagnosis-rate proxy.** `i_ci` here is a [std] placeholder
   because AC04/16-Series values are subscriber-restricted [REG-R22] [REG-R26];
   miscalibration scales claims one-for-one. WP167 also flags COVID-affected 2020
   experience [R9].
3. **Overlap factor `k`.** Bounds: assuming `k = 0` maximally double-counts
   (overstates combined incidence by the true overlap x `q_d` per year); `k = 0.25`
   may understate. Calibrate
   from cause-of-claim data (WP52/WP151/WP167 lineage) where licensed [R8] [R9].
4. **Lapse.** With level guaranteed premiums against steeply age-increasing `i_ci`,
   early durations pre-fund later ones: higher-than-assumed late-duration lapses
   release liability, lower ones extend exposure to the steep part of the incidence
   curve; the BEL is not monotone in a single lapse scalar. Lapse assumptions must be
   realistic and condition-dependent under the Rulebook (9.1–9.2) [R7].
5. **Expenses and expense inflation.** Second-order next to (1)–(4) on this
   mono-benefit product **[std]** placeholders throughout.
6. **Guaranteed vs reviewable premiums.** The base model's premiums are guaranteed —
   morbidity deterioration cannot be repriced, so items (1)–(3) fall entirely on the
   insurer. The reviewable module transfers trend risk to policyholders at the cost of
   review-shock lapse and selective lapsation (anti-selection multiplier `η`)
   [S3] [S4] [S5].

Known modeling pitfalls:

- **Double counting death and CI.** Summing `q_d + i_ci` without the overlap term
  overstates accelerated claim incidence; conversely, applying `k` to the standalone
  *paid* decrement (instead of to the non-paying death exit) understates claims.
- **Survival-period misapplication.** Applying the 14-day survival reduction `δ` to
  the accelerated main benefit is wrong — death within the survival period still pays
  `SA` as a death claim [S1]; `δ` bites only in the standalone variant [S4] [S11].
- **Depleting the sum assured for partial claims.** Additional-payment and children's
  claims must not reduce `SA` or decrement `l(t)` [S1] [S3] [S4] [S8] [S11]; modeling
  them as accelerations (the severity-graded plan-account depletion design [S10]) is a
  different product.
- **Terminating on additional-payment claims.** Same error, opposite sign: only the
  main benefit ends the policy [S1] [S4] [S11].
- **Age-basis mismatch.** `i_ci`, `q_d` and attained-age indexing must share the ANB
  **[std]** basis.
- **Proxy-basis leakage.** The [std] proxy rates in these notes are placeholders and
  must not be presented as CMI or ONS values; production work replaces them with a
  licensed basis and documents the substitution (TAS 100 data/assumption
  requirements [R10] [REG-R33]).
- **Premium placeholder.** £55/month is not a market rate (no insurer publishes CI
  rate cards — research-file gap); profitability conclusions from the worked example
  are meaningless. One carrier's reviewable reviews have "no limits" [S4] — do not model
  reviewable business with the guaranteed-premium constraint.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #uklib-critical_illness-r10
[R2]: #uklib-critical_illness-r2
[R3]: #uklib-critical_illness-r3
[R7]: #uklib-critical_illness-r7
[R8]: #uklib-critical_illness-r8
[R9]: #uklib-critical_illness-r9
[REG-R1]: #uklib-reg-r1
[REG-R22]: #uklib-reg-r22
[REG-R26]: #uklib-reg-r26
[REG-R30]: #uklib-reg-r30
[REG-R32]: #uklib-reg-r32
[REG-R33]: #uklib-reg-r33
[REG-R34]: #uklib-reg-r34
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
