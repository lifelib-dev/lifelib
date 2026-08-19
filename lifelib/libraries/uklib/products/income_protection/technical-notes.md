# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md`, whose numbering is carried verbatim from
`_research/income-protection.md`; [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own
R-numbering; research provenance in `_research/regulatory-actuarial.md`).
**[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter
values are identical to those in `product-spec.md`.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums, benefit
  outgo, expenses) for a single-policy model point of full-term guaranteed-premium
  own-occupation IP. Reserves are not computed (see Valuation and reserve pointers).
- **Model structure.** Three-state multiple-state model — healthy/active (H), sick
  and in claim payment (S), dead (D) — the structure of the CMI graduations: CMIR 12
  introduced the healthy–sick–dead multiple-state model for UK PHI, applied to the
  IPM 1991-98 graduations and carried through to the IP11 Series [R4] [R1]. (The CMIR
  12 report title/date is recorded from search summaries only [unverified].) Lapse is
  an additional exit from H. Experience is parameterized exactly as the CMI publishes
  it: claim **inception** rates by sex, deferred period and occupation class, and
  claim **termination** rates split by recovery and death, duration-dependent [R1] [R2].
- **Projection frequency.** Monthly grid, matching the monthly-in-arrears benefit
  [S1] [S3] [S10]. Annual assumption rates are converted to monthly per the formulas
  below **[std]**.
- **Timing conventions [std].** Premiums received at the beginning of the policy
  month (BOM) from lives in H; state transitions occur at end of month (EOM); benefit
  for month t is paid at EOM to lives in claim payment throughout month t — in S at
  BOM and still in S at EOM (monthly in arrears [S1]; a claim incepting at EOM t
  receives its first payment at EOM t+1). The
  contractual daily pro-rating of partial claim months [S1] [S3] [S10] is replaced by
  whole-month payment **[std]**. Escalation applies at BOM of each anniversary month.
- **Age basis.** Age nearest birthday at entry, advancing with policy year **[std]**.
  No public statement of the IP11 age definition was retrieved (the briefing note
  records graduated age ranges 17–65 M / 17–60 F, extended to 70 [R1]); the choice
  is a pure convention and must be revisited by CMI Authorised Users.
- **Claim duration.** Measured in months since claim (payment) inception, i.e. since
  the end of the deferred period **[std]** convention; IP11 termination rates are
  two-dimensional in age and sickness duration, with run-in periods of increasing
  recovery rates at early durations for DP4/13/26 [R1]. Whether the CMI duration
  clock runs from sickness onset or payment start was not extracted from public
  documents — subscribers must align the convention with the tables they license.
- **Currency and units.** GBP; benefit and premium in £/month; rates are
  probabilities per period unless labelled "per mille".
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis; survivorship/state probabilities multiply per-policy
  cash flows. In-force portfolios need both active cells and claims-in-payment cells
  (with claim duration as a model-point attribute).

---

## Model point attributes

| Attribute | Type | Example (base cell) |
|---|---|---|
| `entry_age` | int | 35 **[std]** |
| `sex` | enum {M, F} | M **[std]** — IP11 rates are sex-split [R1] |
| `occ_class` | enum {1, 2, 3, 4} | 1 **[std]** — CMI occupation classes OC1–OC4 [R1] |
| `benefit_monthly` | currency (£/month at issue) | 2,000 **[std]** |
| `earnings_annual` | currency (underwriting record) | 40,000 **[std]** |
| `deferred_weeks` | enum {4, 8, 13, 26, 52} | 26 **[std]** |
| `expiry_age` | int (50–70) | 65 **[std]** |
| `escalation` | enum {none, RPI} | RPI (capped 10%, premium ×1.5) [S1] [S2] |
| `premium_monthly` | currency (£/month at issue) | 35 **[std]** — rates not public |
| `premium_basis` | enum {guaranteed} (reviewable/age-costed out of scope) | guaranteed |
| `status` | enum {active, in_claim} | active |
| `claim_duration_months` | int (in-claim cells only) | 0 |

Smoker status is not an attribute: the IP11 rate structure is sex / deferred period /
occupation class [R1]; any smoker differentiation sits in insurer pricing, which is
not public.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l_H(t)` | Probability in state H (active premium-payer, incl. any sickness spell still inside the deferred period — see Deferred-period mechanics) at EOM t | monthly |
| `l_S(t, z)` | Probability in claim payment at EOM t with claim duration z months (z = 1, 2, ...) | monthly, two-dimensional |
| `l_S(t)` | Total in-claim probability = Σ_z l_S(t, z) | derived |
| `B(y)` | Escalated monthly benefit in policy year y | at anniversaries |
| `P(y)` | Escalated monthly premium in policy year y | at anniversaries |
| `AP(y)` | Amount payable per month of full incapacity (spec formula; base: = B(y)) | at anniversaries |
| `n(t)` | New claim inceptions during month t | monthly |
| `rec(t)`, `dth_S(t)`, `dth_H(t)`, `lps(t)` | Exits: recoveries, deaths in claim, deaths in H, lapses | monthly |

There is no account value, surrender value or unit fund: the contract has no cash-in
value at any time [S4] [S5] [S7], so the only state is the insured population itself.

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited; from the spec)

| Input | Value | Basis |
|---|---|---|
| Deferred period d | 26 weeks (base cell) | menu [S6]; pick **[std]** |
| Benefit formula parameters | 65% / 50% bands, £60,000 breakpoint, £20,000/month cap, £1,500 guarantee, 90% tolerance | [S1] [S2] [S5] [S7]; picks **[std]** (spec footnotes 6–8) |
| Escalation mechanics | j(y) = min(max(RPI_y, 0), 0.10); B ×(1+j); P ×(1+1.5j); continues in claim | [S1] [S2]; multiplier pick **[std]** |
| Premium guarantee | Guaranteed level apart from escalation | [S1] [S3] [S5] [S7] |
| Waiver of premium | No premiums from lives in S (payable through the deferred period) | [S5] [S7] [S10] [S11]; convention **[std]** |
| Linked claims | Same-cause recurrence within 52 weeks: no new deferred period | [S1] [S3] [S5] [S7] [S10] [S11]; window pick **[std]** |
| Proportionate benefit | (A − B)/A × C on partial return to work | [S7]; common structure [S1] [S3] [S5] [S10] [S11] |
| Expiry | All cover and claim payments cease at the policy end date (age 65 base cell) | [S1] [S3] [S5] [S7] [S10]; age pick **[std]** |
| Grace | 60 days, cancellation without value | [S1] [S3]; pick **[std]** |

### (b) Insurer-discretionary current elements

For the guaranteed-premium full-term composite these are deliberately **thin**: there
are no bonuses, no reviewable charges, and no market value reductions — premiums are
guaranteed [S1] [S3] [S5] [S7] and there is no surrender value [S4] [S5] [S7]. Recorded
for the variations only:

- **Reviewable premiums** (variation): fixed for 5 years, then reviewed with no
  contractual cap [S1] [S4] [S6] [S10]. Review formulas are discretionary and
  undisclosed (research file gap) — any reviewable-premium model needs a **[std]**
  review rule; none is specified here.
- **Holloway surplus participation** (out-of-scope variation): surplus and bonus
  allocations plus a discretionary terminal bonus, on With-Profits Actuary advice
  [S11] [S12] — requires a capital-account state not present in this model.
- **Escalation index snapshot**: future RPI is an economic input, not insurer
  discretion; the reference snapshot is RPI = 3.0%/yr flat **[std]**, so
  j = 0.03, premium growth 4.5%/yr while premiums are payable.

### (c) Behavioral / experience assumptions (modeler's view)

The authoritative UK experience basis is the CMI IP11 Series (individual IP,
2007–2016 data): claim inception rates by sex, deferred period (DP1/4/13/26/52) and
occupation class (OC1–OC4); termination rates split recovery vs death,
two-dimensional in age and sickness duration; table naming
`IP11 {M/F} DP{d} OC{n} {Inc/Rec/Dth}` [R1]. **The rate values are restricted to CMI
Authorised Users** (the working papers and the IP Rate Table Tool are
subscriber-only [R2] [R3] [R5]; the CMI access model is per [REG-R22]), so the
reference basis below is a **[std] proxy shaped like the IP11 structure — the values
are NOT IP11 values and carry no CMI authority.** Known data issue: IP11 inception
rates are understated due to exposure errors; the CMI published indicative
adjustments alongside WP136 (terminations unaffected) [R1] [R2] [R3] — users with
table access must apply them.

| Input | Reference basis | Basis tags |
|---|---|---|
| Claim inception rates ι_a(a) | [std] proxy table below (structure: M, DP26, OC1 [R1]) | values **[std]** |
| Recovery rates ρ_a(z) | [std] proxy table below, by claim duration year (IP11 is duration- AND age-dependent [R1]; age suppressed **[std]**) | values **[std]** |
| Mortality in claim q_S_a(z) | [std] proxy, flat 3%/yr all durations (IP11: duration-dependent to 5 years, age-only beyond [R1]) | value **[std]** |
| Active-life mortality q_H_a(a) | ONS UK national life tables qx (sex-specific), ×100% factor | table [REG-R32]; factor **[std]** (1) |
| Mortality/morbidity improvement | None in base **[std]**; CMI_20xx with a [std] long-term rate is the projection convention for mortality | [REG-R30] |
| Lapse w_a(y) | [std] table below; no public UK IP lapse study was retrieved | **[std]** |
| Maintenance expense | £60/policy/yr, inflating 3.0%/yr | **[std]** |
| Claim management expense | £300/yr per claim in payment, inflating 3.0%/yr | **[std]** |
| Offset/guarantee effect | AP(y) = B(y) — amount-payable ratio 1.0 (offsets and guarantee assumed not to bite) | **[std]** (2) |
| Claim severity factor k | 1.0 (proportionate/rehabilitation claims not projected separately) | **[std]** (2) |
| Discount | PRA risk-free term structure for valuation [R7] [REG-R1]; flat 3.0%/yr in the worked example only | rate **[std]** |

1. ONS national life tables are the only freely redistributable UK mortality source
   (Open Government Licence); population mortality is heavier than insured
   experience [REG-R32]. CMI assured-lives table *names* are public (e.g. AM92/AF92
   [REG-R24]) but current insured tables are Authorised-User-restricted [REG-R22].
   Active-life mortality is a minor decrement in IP; the ×100% factor is a
   placeholder to be replaced with portfolio experience.
2. Offsets, the minimum benefit guarantee, and proportionate benefits change the
   amount paid relative to the chosen benefit (spec, Contractual mechanics). The base
   model pays the full escalated benefit; portfolio calibrations should set
   AP/B < 1 or k < 1 from claims experience.

**[std] proxy claim inception rates** (annual, per mille of lives in H; male, OC1,
DP26; linear interpolation between pivot ages; pure placeholders):

| Age a | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 64 |
|---|---|---|---|---|---|---|---|---|
| ι_a(a) ‰ | 1.0 | 1.3 | 1.8 | 2.6 | 4.0 | 6.5 | 10.0 | 14.0 |

**[std] proxy claim termination rates** (annual, by claim duration year since
payment inception; pure placeholders):

| Claim duration year | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| Recovery ρ_a | 0.40 | 0.25 | 0.15 | 0.10 | 0.05 |
| Death in claim q_S_a | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 |

The declining-with-duration recovery shape mirrors the qualitative structure the CMI
publishes (duration-dependent termination rates [R1]); the IP11 "run-in" feature
(recovery rates *increasing* over the first weeks of claim for DP4/13/26 [R1]) is
not reproduced at this granularity — a monthly refinement point for table licensees.

**[std] lapse table** (annual rates from H; lives in S do not lapse — premiums are
waived and the benefit is valuable **[std]**):

| Policy year | 1 | 2 | 3–5 | 6+ |
|---|---|---|---|---|
| w_a(y) | 10% | 8% | 6% | 4% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1..T; T = 12 × (expiry_age − entry_age) = 360 (base cell); y = ceil(t/12); attained age a = entry_age + y − 1 |
| B(y), P(y), AP(y) | escalated benefit, premium, amount payable (£/month); B(1) = 2,000, P(1) = 35 **[std]** |
| j | escalation rate = min(max(RPI, 0), 0.10); snapshot 0.03 **[std]** |
| ι_m(a) | monthly claim (payment) inception rate = 1 − (1 − ι_a(a))^(1/12) **[std]** |
| q_H_m(a), w_m(y) | monthly active mortality and lapse, same annual-to-monthly conversion **[std]** |
| ρ_m(z), q_S_m(z) | monthly recovery and death-in-claim rates at claim duration z months (from the annual rate of the duration year containing z) **[std]** |
| s_S(z) | monthly in-claim survival = (1 − ρ_m(z)) × (1 − q_S_m(z)) (independent decrements **[std]**) |
| e_m(y), ec_m(y) | monthly maintenance and claim-management expense = 60/12 and 300/12, × 1.03^(y−1) **[std]** |
| v(t) | discount factor to time t (valuation: PRA risk-free curve [R7] [REG-R1]; worked example: 1.03^(−t/12) **[std]**) |
| l_H(t), l_S(t, z) | state probabilities (state-variable table); l_H(0) = 1, l_S(0, ·) = 0 for an at-issue cell |

Dimensional check: ι, q, w, ρ are monthly probabilities (dimensionless); B, P, AP,
e are £/month; every cash flow below is £ per month per policy issued.

### Monthly processing order [std]

At month t (skip all steps from t > T; at t = T all cover and any claim in payment
terminate without value [S1] [S3] [S5] [S7] [S10]):

1. **Anniversary (BOM, months t = 13, 25, ...):** B(y) = B(y−1) × (1 + j);
   P(y) = P(y−1) × (1 + 1.5 × j) [S1] [S2]. In-claim benefit escalates identically
   [S1] [S2] — the same B(y) applies to lives in S.
2. **Premium income (BOM):** `PREM(t) = P(y) × l_H(t−1)`. Lives in S pay nothing
   (waiver [S5] [S7] [S10] [S11]); lives in H still inside a deferred period pay
   normally (see Deferred-period mechanics).
3. **Transitions (EOM), from H** — order death, then lapse, then inception among
   survivors **[std]**:
   - `dth_H(t) = l_H(t−1) × q_H_m(a)`
   - `lps(t) = l_H(t−1) × (1 − q_H_m) × w_m(y)`
   - `n(t) = l_H(t−1) × (1 − q_H_m) × (1 − w_m) × ι_m(a)` (new claims at duration z = 1)
4. **Transitions (EOM), from S** — order recovery, then death **[std]**, per
   duration cohort z:
   - `rec(t, z) = l_S(t−1, z) × ρ_m(z)`
   - `dth_S(t, z) = l_S(t−1, z) × (1 − ρ_m(z)) × q_S_m(z)`
   - `l_S(t, z+1) = l_S(t−1, z) × s_S(z)`
   - `l_S(t, 1) = n(t)`
5. **State update:**
   `l_H(t) = l_H(t−1) × (1 − q_H_m) × (1 − w_m) × (1 − ι_m) + Σ_z rec(t, z)`
   (recovered lives return to H and are again exposed to inception **[std]**; see
   the linked-claims limitation below).
6. **Benefit outgo (EOM):** `BEN(t) = k × AP(y) × [l_S(t) − n(t)]` — i.e. paid to the
   surviving cohorts z ≥ 2 only (equivalently Σ_z l_S(t−1, z) × s_S(z)): benefit is
   monthly in arrears [S1], so new inceptions n(t) = l_S(t, 1), seeded at EOM t,
   receive their first payment at EOM t+1. (Including n(t) in BEN(t) would pay a
   full month's benefit at the instant of payment inception and break the
   inception-annuity equivalence in Active-lives valuation.) Whole-month
   convention **[std]**.
7. **Expenses (EOM):** `EXP(t) = e_m(y) × [l_H(t−1) + l_S(t−1)] + ec_m(y) × l_S(t−1)`.
8. **Discount** cash flows at v(t) and accumulate.

Net cash flow (insurer perspective): `CF(t) = PREM(t) − BEN(t) − EXP(t)`. Death and
lapse generate no payment (no death benefit, no surrender value [S4] [S5] [S7]; the
out-of-scope £5,000–£10,000 death benefits in two sampled contracts [S3] [S5] would
add a `dth × DB` term).

### Deferred-period mechanics

The contract pays after d weeks (26, base cell) of continuous incapacity, with
premiums payable through the deferred period and waived from benefit start (spec).
The model embeds the deferred period **in the inception basis**: ι is a *claim
payment* inception rate specific to DP26 — exactly the quantity the CMI publishes
per deferred period [R1] — so sickness spells that recover inside the deferred
period never leave H, and lives sick within the deferred period remain in H (still
premium-paying, matching the contractual waiver-from-payment-start convention
**[std]**, spec footnote 16). Consequences:

- No separate "sick, not yet in payment" state is needed; the d-week lag between
  onset and payment is absorbed into ι's calibration. A timing refinement (shifting
  inception cash flow impact by d weeks) is second-order at DP26 **[std]**.
- Dual deferred periods and sick-pay-linked NHS/teacher deferreds [S1] [S3] [S5] [S7]
  [S10] would need spell-level modeling and are out of scope.
- **Linked claims limitation [std]:** contractually, a same-cause recurrence within
  52 weeks of payments stopping restarts payment without a new deferred period
  (spec). The base model returns recovered lives to H with the standard DP26
  inception basis, which understates short-horizon re-inception. Refinement: a
  post-recovery flag with a loaded ι for 12 months; not specified further here.

### Claims-in-payment valuation (disabled-life annuity)

A claim in payment is valued as a disabled-life annuity: expected present value of
the escalating benefit until recovery, death or expiry — the "claim annuity values"
the CMI Rate Table Tool produces for subscribers [R5]. For a claim at duration z0
months, attained age a0, with T_rem months to expiry:

    a_dis(a0, z0) = Σ_{m=1}^{T_rem} [ Π_{i=1}^{m} s_S(z0 + i − 1) ] × k × AP(y(m)) / AP(y(0)) × v(m)

so that claims-in-payment BEL outgo per £1/month of benefit in payment is a_dis, and
the cell's benefit liability is AP × a_dis + the claim-expense annuity (same
survival, ec_m in place of AP). Escalation enters through AP(y(m)) (step-ups at
policy anniversaries [S1] [S2]); the annuity truncates at expiry — payments stop at
the policy end date [S1] [S3] [S5] [S7] [S10].

### Active-lives valuation

Active-life BEL cash flows are steps 1–8 run from the valuation date: premium income
from l_H, benefit outgo from claims yet to incept (each n(t) seeds a new duration
cohort), and expenses. Equivalently, the benefit side can be written as
`Σ_t v(t) × n(t) × [k × AP × a_dis(a(t), 0-month equivalent)]` — the inception-annuity
decomposition of the same multi-state projection.

**Alternative: inception-annuity method [brief].** The historical alternative prices
each year's claim cost as (inception rate) × (disabled-life annuity at claim start)
without tracking in-claim cohorts through time — adequate for premium rating, but it
cannot roll claims-in-payment forward or produce per-period BEL cash flows, which is
why the multi-state formulation is the reference structure. The research file
records the pre-CMIR 12 history (Manchester Unity sickness-rate basis;
inception-annuity vs multi-state reserving) as [unverified] textbook knowledge — no
public IFoA source was retrieved; the CMIR 12 → IPM 1991-98 → IP11 multi-state
lineage itself is verified at landing-page level [R4].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no public UK IP
policyholder-behavior study was retrieved.

- **Base lapse [std].** w_a(y) per the table above; monthly
  w_m = 1 − (1 − w_a)^(1/12). Applied to H only; lives in S never lapse (premiums
  waived, benefit in payment) **[std]**.
- **Premium-shock lapse [std].** With escalation on, premiums rise 1.5 × j each
  year; the model multiplies lapse by
  `M_esc(y) = 1 + 2 × max(0, 1.5 × j(y) − 0.05)` in anniversary years (lapse
  response to premium increases above 5%; e.g. j at the 10% cap gives 1.5 × 0.10 =
  15% premium growth and M_esc = 1.2). Contract anchor: sampled insurers let
  policyholders decline escalation increases, with the option lapsing after
  consecutive refusals — two consecutive cancelled increases end the option in one
  contract [S5]; declining three consecutive increases removes it in another [S11];
  declines are modeled as lapse of the escalation margin only at portfolio level —
  the base single-cell model keeps escalation always-on and uses M_esc as the
  aggregate proxy.
- **Economic-cycle morbidity link [std note].** Claim inceptions are widely believed
  to rise (and recoveries to slow) in recessions — job insecurity raises claim
  propensity on an own-occupation definition. No sampled document or public CMI
  output quantifies this; it is recorded here as a scenario overlay
  `ι × M_cycle`, `ρ / M_cycle` with M_cycle = 1 in base **[std]**, not as a
  calibrated assumption.
- **GIO take-up, alterations, career breaks:** held at zero (spec: out of scope).

---

## Worked example

Claims-in-payment recursion for the base cell's level-cover variant **[std]** (the
escalation step falls outside the 3-month window shown): a claim in payment from
duration z = 0, benefit AP = B = £2,000/month, duration-year-1 proxy terminations
(ρ_a = 0.40, q_S_a = 0.03 **[std]**), discount 3.0%/yr flat **[std]**.

Monthly factors (derived): ρ_m = 1 − 0.60^(1/12) = 0.041675;
q_S_m = 1 − 0.97^(1/12) = 0.002535; in-claim survival
s_S = 0.958325 × 0.997465 = 0.955895; v = 1.03^(−1/12) = 0.997540.

| Month m | l_S start | Recoveries ρ_m × l_S | Deaths (1−ρ_m) q_S_m × l_S | l_S(m) = l_S × s_S | Benefit 2,000 × l_S(m) | v^m | PV |
|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 0.041675 | 0.002429 | 0.955895 | 1,911.79 | 0.997540 | 1,907.09 |
| 2 | 0.955895 | 0.039837 | 0.002322 | 0.913735 | 1,827.47 | 0.995086 | 1,818.49 |
| 3 | 0.913735 | 0.038080 | 0.002220 | 0.873434 | 1,746.87 | 0.992638 | 1,734.01 |

Three-month PV of benefit outgo: £5,459.59 per claim in payment. Trace, month 1:
survival s_S = (1 − 0.041675) × (1 − 0.002535) = 0.955895; expected benefit paid at
EOM = 2,000 × 0.955895 = £1,911.79 (in-arrears convention: exits during the month
receive nothing under the whole-month simplification **[std]**; contractually they
would receive a daily pro-rated amount [S1] [S3] [S10]); PV = 1,911.79 × 0.997540 =
£1,907.09. Claim expense follows the same survival column at ec_m = 300/12 = £25.00
per month **[std]**. On the active-lives side, the same conventions give month-1
premium income P × l_H(0) = £35.00 and expected new inceptions
n(1) ≈ ι_m(35) = 1 − (1 − 0.0013)^(1/12) = 0.000108 — each seeding this in-claim
recursion at z = 1.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers
consume them and are NOT reproduced here:

- **Solvency UK.** Technical provisions = best estimate + risk margin; the best
  estimate is the probability-weighted average of future cash flows discounted at
  the relevant risk-free term structure [R7] [REG-R1] — i.e. exactly the active-life
  and claims-in-payment projections above, both premium and claim sides. Risk margin:
  cost-of-capital method at 4% with life λ-tapering 0.9 [REG-R4] —
  cited-not-specified. The claims-in-payment element of IP is an MA "eligible
  element" where organised and managed separately [R8] [REG-R2]: the disabled-life
  annuity cash flows are the portion a UK insurer may discount at risk-free + MA
  under an MA permission.
- **IFRS 17.** UK-adopted IFRS 17 (effective 2023) applies to IFRS-reporting UK
  life insurers [REG-R38]; the fulfilment-cash-flow engine consumes the same
  projections with its own discounting, risk adjustment and CSM layers
  (cited-not-specified).
- **Professional standards.** TAS 100 (all technical actuarial work) and TAS 200
  (insurance-specific) govern UK actuarial use of such models [R10]
  (fetched_ok=false in the product research pass; verified via [REG-R33] [REG-R34]).

---

## Key sensitivities and model risks

Dominant assumptions, in rough order:

1. **Claim inception and termination (recovery) rates.** They set both sides of the
   liability: inceptions drive new-claim frequency, recoveries drive claim length —
   a small recovery-rate change compounds across the whole disabled-life annuity.
   Both proxy tables here are **[std]** placeholders; the real IP11 basis is
   restricted [R1] [R2] [R5] [REG-R22], and IP11 inceptions carry a known
   understatement requiring the WP136 indicative adjustments [R1] [R3].
   Sensitivity-test ι and ρ first, and independently.
2. **Morbidity trend.** The base holds morbidity level **[std]**; cause-mix shifts
   (notably mental-health claims, which interact with own-occupation assessment)
   move both ι and ρ. No public quantification was retrieved — treat as a scenario
   axis, not a calibrated input **[std note]**.
3. **Economic sensitivity of claims.** Recession-linked inceptions and slowed
   recoveries (the M_cycle overlay) are the classic IP experience risk on
   own-occupation business — a [std] scenario note, deliberately not calibrated
   here.
4. **Escalation/inflation.** RPI-linked benefit escalating in claim [S1] [S2] makes
   the disabled-life annuity inflation-sensitive precisely when it is longest; the
   10% cap is an embedded inflation option. The premium side compensates only ×1.5
   on actives, and not at all on claims in payment (waiver).
5. **Lapse.** Second-order for claim cost but first-order for premium income and
   deferred-acquisition economics; the table is **[std]** with no public anchor.

Known modeling pitfalls:

- **Duration dimension.** Collapsing l_S(t, z) to a single bucket with
  duration-independent termination rates materially misstates claim runoff — the
  duration gradient (0.40 → 0.05 in the proxy) is the defining feature of IP
  terminations [R1].
- **Premium waiver double-count.** Projecting premium income from l_S lives
  overstates premiums; premiums come from l_H only (waiver [S5] [S7] [S10] [S11]).
- **Expiry truncation.** The disabled-life annuity must truncate at the policy end
  date [S1] [S3] [S5] [S7] [S10]; an untruncated annuity materially overstates
  liabilities for claims incepting near expiry.
- **Amount payable vs chosen benefit.** Offsets, the £1,500 guarantee and
  proportionate benefits mean amounts paid can differ from B; modeling AP = B
  **[std]** overstates outgo where the maximum-benefit formula bites (and
  understates nothing — AP ≤ B always).
- **Linked claims.** Returning recovered lives to the standard inception basis
  ignores the waived deferred period on 52-week recurrences (see limitation note) —
  understates outgo for short-recovery portfolios.
- **Run-in periods.** IP11 recovery rates increase over the first weeks of claim
  for DP4/13/26 [R1]; annual duration-year granularity **[std]** smooths this away
  — significant for short deferred periods, less so at DP26.
- **Basis-structure mismatch.** The proxy termination rates drop the age dimension
  **[std]**; IP11 is two-dimensional (age × duration), with claimant mortality
  duration-dependent to 5 years and age-only beyond [R1]. Table licensees should
  restore both dimensions.
- **Escalation timing.** B escalates on policy anniversaries in this model
  **[std]**; some contracts escalate in-claim amounts on claim anniversaries with
  index-lag rules (e.g. RPI five months prior, post-claim catch-up [S10]) — align
  with the contract being modeled.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-income_protection-r1
[R10]: #uklib-income_protection-r10
[R2]: #uklib-income_protection-r2
[R3]: #uklib-income_protection-r3
[R4]: #uklib-income_protection-r4
[R5]: #uklib-income_protection-r5
[R7]: #uklib-income_protection-r7
[R8]: #uklib-income_protection-r8
[REG-R1]: #uklib-reg-r1
[REG-R2]: #uklib-reg-r2
[REG-R22]: #uklib-reg-r22
[REG-R24]: #uklib-reg-r24
[REG-R30]: #uklib-reg-r30
[REG-R32]: #uklib-reg-r32
[REG-R33]: #uklib-reg-r33
[REG-R34]: #uklib-reg-r34
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
