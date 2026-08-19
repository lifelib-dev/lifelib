# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md`, numbering carried from `_research/pension-annuity.md`; [REG-R#] tags
refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation. Parameter values are
identical to those in `product-spec.md`; the mechanics anchor is one carrier's
pension annuity [S1] [S2].

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (annuity instalments
  to annuitant and dependant, guarantee-period payments, value-protection lump sums,
  maintenance expenses) for a single pension annuity in payment. Discounting, the
  matching adjustment and reserves are not computed (see Valuation and reserve
  pointers).
- **Mortality is the model.** The contract has no premiums after outset [S2 §1.1], no
  surrender value [S2 §12] [S5 cl.14.7], no account value and no policyholder options
  after the cancellation window [S1 p4]. The only decrements are deaths; the only
  stochastic drivers are longevity and (for indexed options) inflation. This is the
  design property that makes the liability MA-eligible [R1].
- **Projection frequency.** Monthly grid, t = 1, 2, ... months from the start date
  **[std]**. Payment dates fall on the grid per the frequency m; exact-day mechanics
  (one carrier's first-of-month payments and stub proportioning [S5 §§5.2–5.3],
  another's working-day adjustment [S2 §2.4]) are not modeled **[std]**.
- **Timing conventions [std].** Escalation is applied at the start of the month
  containing the policy anniversary (first at t = 13) [S2 §3.3]. Advance instalments
  are paid at the start of a payment period and require survival at the start;
  arrears instalments at the end, requiring survival at the payment date. Deaths are
  decremented at end of month; a death in month t means the life does not receive an
  arrears payment due at the end of month t **[std convention]**.
- **Age basis.** Age last birthday (ALB) **[std]**, chosen to index the [std] ONS
  life-table proxy by single year of age [R13]; the ONS convention itself is
  [unverified]. Annual rates convert monthly as q_m = 1 − (1 − q_x)^(1/12) **[std]**.
- **Limiting age.** ω = 115 **[std]**: the [std] base table is extended beyond its
  maximum tabulated age by log-linear extrapolation of qx, capped at 1 at ω.
- **Currency and model points.** GBP throughout [S2 §1.3]. Single-policy model
  points, projected on an expected (probability-weighted) basis: survival
  probabilities multiply scheduled per-policy cash flows. No aggregation logic is
  specified here.
- **Joint-life independence.** Annuitant and dependant mortality are independent
  **[std]** (common-shock/"broken-heart" dependence is a documented model risk).

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `purchase_price` P | currency | 100,000 [S1 p11] |
| `annuitant_age` x_a | int (ALB) | 65 [S1 p11] |
| `annuitant_sex` | enum {M, F} | M **[std]** |
| `rating_multiplier` θ_a | float ≥ 1 (1 = standard; enhanced overlay) | 1.0 **[std]** |
| `dependant_present` | bool | true |
| `dependant_age` x_d | int (ALB) | 62 **[std]** |
| `dependant_sex` | enum {M, F} | F **[std]** |
| `dependant_pct` δ | float ≤ 1 [S1 p9] | 0.50 **[std]** |
| `overlap` | bool (with/without overlap [S2 §§5.9–5.11]) | false **[std]** |
| `annual_income` A(1) | currency p.a. | 5,400 **[std]** (see Worked example) |
| `frequency` m | enum {12, 4, 2, 1} [S2 §2.2] | 4 |
| `timing` | enum {advance, arrears} [S2 §2.3] | arrears |
| `proportion` | bool (arrears only [S2 §4]) | false |
| `escalation_type` | enum {level, fixed, rpi_catchup, lpi5} (spec menu) | fixed |
| `escalation_rate` g | float ≤ 0.10 [S2 §3.2] | 0.03 **[std]** |
| `guarantee_months` n | int, 12–360, 0 if none [S1 p10]; XOR with VP [S2 §§6.7, 7.6] | 0 |
| `vp_pct` v | float ≤ 1 [S1 p11]; v + δ ≤ 1 on first-death basis [S2 §7.3] | 0.50 **[std]** |
| `vp_basis` | enum {first_death, last_survivor} [S2 §7.3] | first_death |

The premium P is the amount applied to the annuity after PCLS and adviser charges
[S1 p4]; PCLS itself is pre-purchase and outside the model. A(1) is a pricing input:
no insurer publishes a rate card, so A(1) is taken from a quote or calibrated to the
anchor (£100,000 at 65 buying £6,657 p.a. with 50% VP, January 2026 [S1 p11]; the
illustration's frequency/timing/escalation basis is not recorded).

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `A(y)` | Annualized income in policy year y (annuitant scale) | anniversaries |
| `peak` | Running peak of the RPI reference index (catch-up state) | anniversaries (rpi_catchup only) |
| `G(t)` | Cumulative gross instalments scheduled through month t | payment dates |
| `l_a(t)` | Annuitant survival probability to end of month t; l_a(0) = 1 | monthly |
| `l_d(t)` | Dependant survival probability to end of month t; l_d(0) = 1 | monthly |
| `d_a(t)` | Probability annuitant dies in month t = l_a(t−1) − l_a(t) | monthly |
| `n_rem(t)` | Remaining guarantee months = max(0, n − t) | monthly |
| `VPbal(t)` | Value-protection balance = max(0, v × P − G(t)) | payment dates |

Because instalments while the annuitant is alive are deterministic given the
escalation path, G(t) and VPbal(t) are deterministic schedules in a deterministic
projection — the expected VP outgo needs no path simulation (see recursions).

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Instalment amount | A(y)/m at each payment date | [S1 p8] [S2 §2.2] |
| Escalation rule | per `escalation_type`: fixed g ≤ 10%; RPI 0-floor with catch-up (12 months ending six months before the anniversary); LPI = RPI capped 5%, floor 0, September year | [S2 §3.2, §3.3, defs]; LPI floor harmonization **[std]** (spec footnote 5) |
| Dependant's income | δ × income, same escalation basis; % of the higher of income at death and at guarantee end | [S2 §§5.12–5.13] |
| Overlap rule | with: dependant stream runs during remaining guarantee; without: starts at guarantee end | [S2 §§5.9–5.11] |
| Guarantee period | n months of instalments certain, escalation continuing as if alive | [S2 §§6.5–6.6] [S7 §4.2] |
| Value protection | max(0, v × P − G(death)) on the chosen basis; v + δ ≤ 1 (first-death) | [S1 p11] [S2 §7, §7.3] |
| Surrender value | none, at any time | [S1 p4] [S2 §12] [S5 cl.14.7] |
| Charges to policyholder | none (priced into the rate) | [S1 p6] |

### (b) Insurer-discretionary current elements

**None post-purchase.** The contract is non-participating [S7 §7.9] with all options
fixed at outset [S1 p4]: there are no bonus rates, no reviewable premiums, no market
value reductions, and no discretionary charges — class (b) is empty for this product.
The only insurer-discretionary quantity is the annuity rate at purchase (pricing, not
an in-force element); its snapshot is the January 2026 anchor quote [S1 p11], and
day-to-day rate setting is not publicly documented [unverified].

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base annuitant mortality | Proper bases: SAPS S3/S4 pensioner tables (S4 released February 2024, graduated on 2014–2019 data) [R10] [R11] or the insured-annuitant PMA16/PFA16 family [REG-R27]. Both are restricted to CMI Authorised Users [R11] [REG-R22], so the reference basis is a **[std]** proxy: latest ONS UK national life table qx by age/sex [R13] × annuitant adjustment α = 0.80 | [R10] [R11] [R13] [REG-R22] [REG-R27]; α **[std]** (i) |
| Mortality improvements | CMI Mortality Projections Model, cited by name/version: CMI_2024 (WP201, June 2025, calibrated to E&W data to 31 Dec 2024) [R12]; current version CMI_2025 (WP211, March 2026) [REG-R30]. Model software restricted; reference fallback is a **[std]** deterministic scale: 1.25% p.a. reduction in qx for ages ≤ 90, tapering linearly to 0% at age 110, applied from the base table's data mid-year | [R12] [REG-R30]; scale **[std]** (ii) |
| Enhanced/impaired rating | Overlay on qx: q_rated = min(1, θ_a × q_base), θ_a ≥ 1 (equivalently a rated-age offset); standard life θ = 1.0 | existence [S1 p5] [S4] [S6] [S9]; overlay **[std]** (iii) |
| Lapse / surrender | None — no surrender value exists | [S1 p4] [S2 §12] [S5 cl.14.7] [R1] |
| Maintenance expense | £30 per policy per annum, payable monthly while any payment obligation remains, inflating at the RPI assumption | **[std]** (iv) |
| RPI inflation (for indexed options) | 3.0% p.a. deterministic | **[std]** (v) |

(i) The SAPS table naming convention (e.g. S3PMA/S3PFA) is [unverified — not stated
on the fetched page] [R10]. ONS national life tables are period tables of population
mortality, freely downloadable and updated annually (latest release dated 10 December
2025 per the fetched dataset page) [R13]; population mortality is heavier than
annuitant experience, hence the α < 1 adjustment. α = 0.80 is a shape-level
placeholder, not calibrated to any published annuitant-vs-population comparison — a
production basis must license CMI tables [R11] [REG-R22].
(ii) CMI_2025 projects improvements converging to a user-chosen long-term rate with
no default recommendation [REG-R30 detail marked unverified in the reference
library](#uklib-reg-r30); the [std] flat-then-taper scale exists only so the reference implementation
is runnable without CMI access, and materially understates the age–period–cohort
structure of the real model [R12].
(iii) Insurers' rating structures (postcode, condition-specific factors [S1 p5] [S9])
are not public; the multiplier form is the simplest overlay that reprices longevity
without touching contract mechanics.
(iv) No insurer publishes expense assumptions (charges are priced into the rate
[S1 p6]); £30 p.a. is a round placeholder for in-payment administration. Acquisition
cost is out of scope (single-premium, priced-in).
(v) Deterministic RPI cannot value the RPI floor, the catch-up ratchet, or the LPI
cap — all inflation options. See Key sensitivities.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | month index from start date, t = 1, 2, ...; policy year y = ceil(t/12) |
| m | payments per year (12/4/2/1); payment months T = {12k/m : k = 1, 2, ...} (arrears) or {12k/m : k = 0, 1, ...} mapped to the start of month 12k/m + 1 (advance) |
| A(y) | annualized income in policy year y; inst(t) = A(y(t))/m for t ∈ T |
| g | fixed escalation rate (0.03 **[std]**, ≤ 0.10 [S2 §3.2]) |
| I(k), peak | RPI reference index at anniversary k and its running maximum (catch-up state) [S2 defs] |
| δ | dependant's percentage (0.50 **[std]**, ≤ 1 [S1 p9]) |
| n | guarantee period in months (0 or 12–360 [S1 p10]) |
| v | value-protection percentage (0.50 **[std]**, ≤ 1 [S1 p11]); v + δ ≤ 1 on first-death basis [S2 §7.3] |
| P | purchase price (100,000 [S1 p11]) |
| G(t) | cumulative gross instalments scheduled through month t |
| q_a(t), q_d(t) | monthly mortality of annuitant/dependant (rated, improved) |
| l_a(t), l_d(t) | survival probabilities from outset; d_a(t) = l_a(t−1) − l_a(t) |
| w(t) | dependant-stream availability: 1 if overlap or t > n, else 0 [S2 §§5.9–5.11] |
| c_e, π | maintenance expense p.a. (30 **[std]**) and expense/RPI inflation (0.03 **[std]**) |

Dimensional check: A(y) is currency per annum; inst = A/m is currency per payment;
G, P, VP lump sums are currency; q, l, δ, v, w are dimensionless. Every cash flow
below is currency per month.

### Escalation update (start of month 12(y−1)+1, y ≥ 2) [S2 §3.3]

    level:        A(y) = A(y−1)
    fixed:        A(y) = A(y−1) × (1 + g)
    lpi5:         A(y) = A(y−1) × (1 + min(0.05, max(0, rpi_Sep(y−1))))      [S2 §3.2, defs; floor [S5 §7.1.4][S9 §4.3]]
    rpi_catchup:  see pseudocode                                              [S2 defs]

RPI catch-up pseudocode (path-dependent ratchet [S2 defs]; a second carrier operates
the same rule [S9]):

    # I[k] = RPI reference level for anniversary k
    # (index for the 12 months ending six months before the anniversary [S2 defs])
    peak = I[0]                      # reference level at outset
    for k = 1, 2, ...:               # k-th anniversary
        if I[k] > peak:
            A = A * (I[k] / peak)    # increase by the excess over the prior peak
            peak = I[k]
        # else: A unchanged (income frozen until the index exceeds its peak)

Equivalently A(y) = A(1) × max(I(0..y−1)) / I(0): income is indexed to the running
peak of the reference index. Under the deterministic RPI assumption (3.0% **[std]**)
the index is monotone and the ratchet never binds, so rpi_catchup degenerates to
fixed-3%; the ratchet has value only under stochastic inflation (see sensitivities).

### Scheduled payment schedule (per policy, before survival weighting)

At each payment month t ∈ T: scheduled annuitant instalment inst(t) = A(y(t))/m;
scheduled dependant instalment δ × inst(t). Update G(t) = G(t−) + (instalments
scheduled at t). The dependant's amount uses δ × the income "as if alive" A(y(t)):
this implements the contractual "% of the higher of income at death and income at
guarantee end" [S2 §5.12] exactly, because under the (non-decreasing **[std]** menu)
escalation options the as-if-alive income path is monotone, so the higher-of base
plus same-basis escalation [S2 §5.13] reproduces δ × A(y(t)) at every later date.

### Expected cash flows (month t)

**Annuity outgo** (annuitant stream with its guarantee floor, plus dependant stream),
for t ∈ T (arrears; for advance replace l(t) with l(t−1) **[std]**):

    E[ANN(t)] = inst(t) × max(1{t ≤ n}, l_a(t))                — certain during guarantee [S2 §6]
              + inst(t) × δ × (1 − l_a(t)) × l_d(t) × w(t)     — dependant stream [S2 §5]

The first term pays the full instalment regardless of survival while the guarantee
runs (annuity-certain floor [S2 §§6.5–6.6] [S7 §4.2]) and l_a(t) × inst(t) thereafter.
The second term pays the dependant when the annuitant is dead and the dependant
alive, gated by w(t): with overlap both streams run during the remaining guarantee;
without overlap the dependant stream starts at guarantee end [S2 §§5.9–5.11].
(Guarantee and VP never coexist in the representative design: n > 0 ⇒ v = 0
[S2 §§6.7, 7.6].)

**Proportionate final payment** (arrears with proportion only [S2 §4]): for a death
in month t, the accrued stub to the next scheduled instalment is approximated as

    E[PROP(t)] = d_a(t) × (h(t) + 0.5) / (12/m) × inst(next(t))   **[std half-month accrual]**

where h(t) is the number of complete months since the last payment date. Without
proportion (representative default) this term is zero and nothing is paid for the
final partial period [S2 §4].

**Value protection** (first-death basis; n = 0):

    E[VP(t)] = d_a(t) × VPbal(t−1),   VPbal(t) = max(0, v × P − G(t))   [S1 p11][S2 §7]

G accumulates gross instalments scheduled while the annuitant is alive; measuring
the balance at t−1 implements "instalments already paid" for a mid-month death
**[std discretization]**. On the last-survivor basis, replace d_a(t) with the density
of the last death, d_last(t) = d(l_a + l_d − l_a l_d)(t), and let G accumulate the
dependant's instalments too [S2 §7.3] [S5 §8.4]. (One carrier's variant additionally
nets guarantee payments due, excluding future RPI/LPI increases [S7 §4.3] —
implementable by extending G with guarantee outflows.)

**Maintenance expense**:

    E[EXP(t)] = (c_e / 12) × (1 + π)^(y−1) × IF(t)                       **[std]**
    IF(t) = min(1, max(1{t ≤ n}, l_a(t)) + 1{δ>0} × (1 − l_a(t)) × l_d(t))

IF(t) is the probability any payment obligation remains (guarantee certain, annuitant
alive, or dependant stream in payment) **[std]**.

**Total gross liability cash flow**: CF(t) = E[ANN(t)] + E[PROP(t)] + E[VP(t)] +
E[EXP(t)]. There is no premium income (single premium at t = 0 is a pricing input,
not projected [S2 §1.1]) and no surrender outgo [S2 §12].

### Mortality construction

    q_base(x, s)   = ONS qx by age/sex [R13] × α,  α = 0.80              **[std]** (proxy for SAPS S4 [R10][R11] / PMA16-PFA16 [REG-R27])
    q_imp(x, c)    = q_base(x) × (1 − f(x))^(c − c_0)                    **[std]** improvement fallback (f = 1.25% p.a. ages ≤ 90, linear taper to 0 at 110; c_0 = base-table data mid-year; production: CMI_2025 with a chosen long-term rate [R12][REG-R30])
    q_rated(x, c)  = min(1, θ × q_imp(x, c))                             **[std]** enhancement overlay
    q_m            = 1 − (1 − q_rated)^(1/12)                            **[std]**
    l(t)           = l(t−1) × (1 − q_m(t)),  separately for annuitant (θ_a) and dependant (θ_d)

### Monthly processing order

1. If t starts a policy year (t = 12(y−1)+1, y ≥ 2): apply the escalation update
   (including catch-up state) [S2 §3.3].
2. If t ∈ T: record scheduled instalments; update G(t).
3. Decrement mortality: update l_a(t), l_d(t), d_a(t).
4. Compute expected payment flows E[ANN(t)], E[PROP(t)] using survival to the
   payment point (arrears: end of month t, i.e. l(t); advance: end of month t−1,
   i.e. l(t−1)) **[std]**.
5. Compute E[VP(t)] from d_a(t) and VPbal(t−1); update VPbal(t).
6. Accrue E[EXP(t)].
7. Stop when IF(t) < 10^-6, or when every in-scope life has passed the limiting age
   (t/12 + x_a > ω and, if a dependant is present, t/12 + x_d > ω), ω = 115 **[std]**
   — stopping on the annuitant's age alone would truncate a younger dependant's tail.

---

## Policyholder behavior modeling

There is none to model, and this is a cited product feature, not an omission: after
the 30-day cancellation window the policyholder holds no options — no surrender or
transfer [S1 p4] [S2 §12] [S5 cl.14.7] [S7 §7.5] [S9 §3.9], no alteration of options
[S1 p4] [S4] [S6] [S9], and no premium flexibility [S2 §1.1]. Consequently the model has
**no lapse decrement and no dynamic behavior formulas**; the MA eligibility conditions
effectively require this shape (no policyholder options beyond a bounded surrender
option) [R1].

Behavior enters only at outset, outside the projection, as basis-selection effects
**[std]** to consider when calibrating mortality:

- **Annuitization anti-selection.** Since the 2015 pension freedoms annuitization is
  optional [R6], so voluntary annuitants self-select for longevity — a reason
  annuitant bases sit below population mortality (the direction of α < 1 **[std]**).
- **Enhanced-annuity selection.** Whole-market enhanced quoting is mandated at the
  point of sale [R5]; lives remaining on standard terms are healthier on average.
  The reference model carries this through θ, not through behavior dynamics.
- **Cancellation window.** The 30-day cooling-off [S1 p7] [S2 §13] is ignored
  (projection starts from a completed purchase) **[std]**.

---

## Worked example

Configuration (the worked model point; parameters as in `product-spec.md`):
P = £100,000 [S1 p11]; annuitant male 65, dependant female 62 **[std]**; quarterly
(m = 4) in arrears, without proportion [S2 §§2.2–2.3, 4]; fixed escalation g = 3%
**[std]**; dependant δ = 50% **[std]**; value protection v = 50% on the annuitant's
(first) death **[std]** — v + δ = 100%, exactly at the contractual bound [S2 §7.3];
no guarantee period (XOR rule [S2 §§6.7, 7.6]). Starting income A(1) = £5,400 p.a.
**[std]** — an illustrative quote level (no public rate card exists; the cited anchor,
£6,657 p.a., is for a 50%-VP basis whose escalation/frequency basis is not recorded
[S1 p11], and an escalating joint-life basis starts lower than a level one for the
same premium [S1 p8] [S4] [S6]). Scenario: the annuitant dies in month 17; the
dependant survives throughout. All amounts in GBP.

Instalments: year 1: 5,400/4 = 1,350.00 per quarter; year 2 (from t = 13):
A(2) = 5,400 × 1.03 = 5,562.00, so 1,390.50 per quarter. Dependant income after
death: δ × A(2) = 2,781.00 p.a. = 695.25 per quarter, first paid at the next
scheduled payment date after death (t = 18) **[std convention]**.

| t (month) | Event | Annuitant CF | Dependant CF | VP lump sum | G(t) |
|---|---|---|---|---|---|
| 3 | Q1 instalment (arrears) | 1,350.00 | — | — | 1,350.00 |
| 6 | Q2 instalment | 1,350.00 | — | — | 2,700.00 |
| 9 | Q3 instalment | 1,350.00 | — | — | 4,050.00 |
| 12 | Q4 instalment | 1,350.00 | — | — | 5,400.00 |
| 13 | Anniversary: A ← 5,400 × 1.03 = 5,562.00 | — | — | — | 5,400.00 |
| 15 | Q5 instalment | 1,390.50 | — | — | 6,790.50 |
| 17 | Annuitant dies. VP = max(0, 0.50 × 100,000 − 6,790.50) | — | — | 43,209.50 | 6,790.50 |
| 18 | Q6 date: no annuitant payment (arrears, without proportion [S2 §4]); dependant stream starts | 0.00 | 695.25 | — | 7,485.75 |
| 21 | Q7 instalment (dependant) | — | 695.25 | — | 8,181.00 |
| 24 | Q8 instalment (dependant) | — | 695.25 | — | 8,876.25 |

Checks. VP balance at death uses instalments paid before death: G(16) = 6,790.50, so
the lump sum is 50,000 − 6,790.50 = 43,209.50 [S1 p11] [S2 §7]. Had "with proportion"
been chosen, a stub of ≈ (1 + 0.5)/3 × 1,390.50 = 695.25 would be paid for the
accrued month-and-a-half since t = 15 (**[std]** half-month accrual; one carrier would
net this stub off the VP fund-value formula [S5 §8.3]). The dependant's 695.25 continues
for her life, escalating 3% at each anniversary on the same basis [S2 §§5.12–5.13].

Guarantee/VP interaction. Had the model point instead carried a 10-year guarantee
**[std default]** and no VP (the XOR rule forbids both [S2 §§6.7, 7.6]), the death in
month 17 would change nothing until month 120: instalments of 1,390.50, escalating 3%
each anniversary as if the annuitant were alive [S7 §4.2], continue to beneficiaries
through t = 120 (annuity-certain floor), and — without overlap — the dependant's
695.25-style stream would begin only from the first payment date after t = 120, at
δ × the income at the end of the guarantee period [S2 §§5.9–5.12]. With overlap, the
dependant's stream would run from t = 18 alongside the guarantee payments
[S2 §§5.9–5.11]. In expectation these scenario flows are reproduced by the E[ANN(t)]
formula with n = 120 and w(t) as defined.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers
consume them and are NOT reproduced here:

- **Solvency UK best estimate.** Technical provisions = best estimate + risk margin;
  the best estimate is the probability-weighted average of future cash flows
  discounted at the relevant risk-free term structure, market-consistently [REG-R1].
  The CF(t) vector above is exactly that input.
- **Matching adjustment.** These cash flows feed MA discounting (risk-free + MA) for
  eligible portfolios: MA permission required; eligibility conditions include no
  future premiums, restricted underwriting risks, the ≤ 5% BEL mortality-stress
  test, and no policyholder options [R1] [REG-R2]. Reform context: CP19/23 → PS10/24,
  effective 30 June 2024 [R2] [REG-R5]; supervisory expectations and matching tests
  in SS7/18 (October 2025 version) [REG-R8]. The MA calculation itself is
  cited-not-specified.
- **Risk margin.** Cost-of-capital method at 4% with life-business tapering λ = 0.9
  (floor 0.25) per SI 2023/1346 [REG-R4]; requires an SCR runoff —
  cited-not-specified.
- **Transitionals.** TMTP (simplified regime from 31 December 2024) affects pre-2016
  back-books only; it adjusts technical provisions, not projected cash flows
  [REG-R3].
- **IFRS 17.** UK-adopted IFRS 17 (adopted 16 May 2022, effective 1 January 2023)
  [REG-R38] measures the same contracts as fulfilment cash flows plus risk
  adjustment plus CSM (measurement mechanics summarized from general knowledge —
  [unverified] in the reference library, which verifies the adoption facts only);
  the expected-cash-flow engine is identical, with regime-specific discounting and
  margins layered on.
- **Tax.** Pension annuities are pension business — non-BLAGAB, trade-profit basis
  [REG-R17] [S5 §14.11]; no policyholder fund tax enters the projection.
- **Professional standards.** Technical actuarial work using this model in the UK
  falls under FRC TAS 100 v2.0 [REG-R33] and TAS 200 v2.0 (effective 1 January 2025)
  [R14]. Proxy models fitted on top of heavy annuity cash-flow models — and the
  outputs the heavy model must expose for them — are treated in the IFoA proxy-model
  working party paper [REG-R36].

---

## Key sensitivities and model risks

Dominant assumptions, in order:

1. **Longevity level (base table × α × θ).** The liability is a life-contingent
   payment stream with no offsetting decrements; a lower mortality level lengthens
   every annuity stream. The [std] α = 0.80 population-proxy adjustment is the
   weakest link in the reference basis — production work must substitute licensed
   SAPS S4 / PMA16-era tables [R10] [R11] [REG-R27] [REG-R22].
2. **Longevity trend (improvements).** The [std] deterministic scale stands in for
   CMI_2025 [REG-R30]; the choice of long-term improvement rate is the single most
   sensitive judgment in UK annuity valuation, and the CMI model's user-set long-term
   rate has no default recommendation [REG-R30, detail unverified](#uklib-reg-r30). The prescribed MA
   mortality stress (worse of +15% level / +0.15pp additive, ≤ 5% BEL movement) [R1]
   gives a regulatory yardstick for level-risk materiality.
3. **Inflation exposure (RPI/LPI options).** RPI-linked instalments make the
   liability an inflation swap; the 0-floor, catch-up ratchet and LPI 5% cap are
   inflation option positions [S2 §3.2, defs]. A deterministic 3% path **[std]**
   values them at intrinsic only: the floor and ratchet never bind and the cap never
   pays off — stochastic inflation (or option-adjusted margins) is required for a
   market-consistent value. RPI reform risk (index definition) is additional and not
   modeled.
4. **Dependant assumptions.** δ, the age gap, and dependant mortality drive the
   joint-life tail; the independence assumption **[std]** ignores broken-heart
   dependence and common lifestyle factors, overstating the expected dependant
   stream modestly.
5. **Expense inflation.** Second-order (expenses are small against instalments), but
   the in-payment term is 30+ years, so the π assumption compounds.

Known modeling pitfalls:

- **Guarantee double-counting.** During the guarantee, the annuitant stream is
  certain — do not also weight it by l_a(t) (the max(1{t≤n}, l_a) form prevents
  paying 1 + l_a). Symmetrically, VP and guarantee never coexist in the
  representative design [S2 §§6.7, 7.6]; engines supporting the combinable variant
  offered by one carrier must net guarantee payments off VPbal [S7 §4.3] or the death
  benefit is double-paid.
- **Overlap gating.** Without overlap the dependant stream is gated on t > n even
  when the annuitant died mid-guarantee; applying δ from the death date silently
  converts every without-overlap policy into the more expensive with-overlap form
  [S2 §§5.9–5.11].
- **Higher-of dependant base.** The δ × A(y(t)) simplification relies on
  non-decreasing escalation; if a decreasing option is configured (one carrier's pure
  RPI [S5 §7.1.2]), the contractual "higher of income at death and at guarantee end"
  [S2 §5.12] must be implemented explicitly.
- **Survival-measurement timing.** Arrears payments require survival at the payment
  date; advance payments at the period start. Using end-of-period survival for
  advance payments understates the liability by roughly one period's mortality per
  payment — material at high ages.
- **Catch-up state.** The RPI ratchet is path-dependent: peak must persist across
  anniversaries. Resetting it each year turns the catch-up into a plain 0-floor and
  overstates indexed income after deflation-recovery paths [S2 defs].
- **Escalation timing.** Increases apply on the anniversary [S2 §3.3], not on
  payment dates; applying the year-2 rate to the t = 12 arrears instalment (accrued
  in year 1) overstates income. GMP-bearing policies use different escalation dates
  (1 April / 1 May at one carrier [S5 §7.2]) — out of scope with GMP generally **[std]**.
- **VP balance timing.** VPbal must net instalments *paid before death*; netting the
  instalment due at the death-month payment date that was never paid (arrears,
  without proportion) understates the lump sum [S2 §§4, 7]. Symmetrically, on
  advance timing an instalment paid at the *start* of the death month has been paid:
  in advance payment months net it (use VPbal after the month-t advance payment,
  not VPbal(t−1)) or the lump sum is overstated by one instalment.
- **Population-proxy basis risk.** The [std] ONS × α basis has the wrong shape as
  well as level versus annuitant tables (socio-economic mix, amounts weighting
  [R10] [R11 detail unverified](#uklib-pension_annuity-r11)); treat all reference-basis results as mechanics
  demonstrations, not valuations — and note the CMI restriction honestly rather
  than shipping approximated "SAPS-like" rates [REG-R22].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-pension_annuity-r1
[R10]: #uklib-pension_annuity-r10
[R11]: #uklib-pension_annuity-r11
[R12]: #uklib-pension_annuity-r12
[R13]: #uklib-pension_annuity-r13
[R14]: #uklib-pension_annuity-r14
[R2]: #uklib-pension_annuity-r2
[R5]: #uklib-pension_annuity-r5
[R6]: #uklib-pension_annuity-r6
[REG-R1]: #uklib-reg-r1
[REG-R17]: #uklib-reg-r17
[REG-R2]: #uklib-reg-r2
[REG-R22]: #uklib-reg-r22
[REG-R27]: #uklib-reg-r27
[REG-R3]: #uklib-reg-r3
[REG-R30]: #uklib-reg-r30
[REG-R33]: #uklib-reg-r33
[REG-R36]: #uklib-reg-r36
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[REG-R5]: #uklib-reg-r5
[REG-R8]: #uklib-reg-r8
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
