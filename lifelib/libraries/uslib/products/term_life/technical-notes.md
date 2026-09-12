# Technical Notes

**Status:** Draft, 2026-08-03. Companion to `product-spec.md` in this directory — all
contractual parameters used here (premiums, fee, modal factors, windows) are the same
representative values specified there. This is a **standardized composite** for reference
modeling, not any single insurer's product. [S#]/[R#] tags cite the product research notes
(`_research/term-life.md`); [REG-R#] tags cite the cross-product reference library
(`references/regulatory-and-actuarial-references.md`; research provenance in
`_research/regulatory-actuarial.md` for R1–R34 and in `_research/appp-a820-a821-a822.md` and
`_research/appp-a830.md` for the AP&P Manual appendix items cited here, same R-numbering); **[std]** marks standardizations introduced for
the reference implementation; [unverified] flags carry over from the research notes.

---

## Model scope and conventions

- **Scope.** Single-life, fully underwritten level premium term per `product-spec.md`:
  10/20/30-year level periods (base cell 20-year), Jump-to-ART post-level term (PLT) with
  unchanged face to expiry at attained age 95, convertible before min(end of level period,
  attained age 70), no cash value, non-participating [S2] [S3] [S6]. Gross liability cash
  flows only; reserves are pointers (see Valuation section).
- **Projection frequency [std]: monthly.** Monthly steps (monthiversary processing) are
  the model. Every *contractual* element of the product is on an annual cycle — level
  premiums, ART renewals at anniversaries, the shock lapse at the level-period end — and
  the model keeps them there; what the monthly grid adds is the timing of everything that
  is not: modal premium collection, mid-year claim settlement, monthly expense accrual,
  and the ability to carry mode-specific behavior (monthly-mode policies show materially
  lower shock lapse and PLT mortality deterioration [R4]). An annual step remains a
  well-defined special case of the recursion below and reproduces its in-force at every
  anniversary exactly — see *Annual equivalence* — but it is not what the reference model
  runs.
- **Time index [std].** `t` is 0-based and counts **policy months**, as in lifelib's
  `basiclife/BasicTerm_S`: the first period is `t = 0` (the issue month), period `t` runs
  from time `t` to time `t + 1`, and the frame is `t = 0, 1, …, proj_len − 1` with
  `proj_len = 12(95 − x)` the number of policy months projected. Because every contractual
  schedule is annual, the policy year is **derived** and used as a lookup key:
  `dur(t) = t // 12` is the completed policy years at the start of month `t` and the
  contractual **policy year is the 1-based label `dur(t) + 1`**; where these notes say
  "policy year k" as contract language, the months are `t = 12(k − 1) … 12k − 1`. Nothing
  is indexed by the policy year.
- **Timing [std].** Monthiversary (BOM) processing: premiums and premium-linked expenses
  at the beginning of the month, in the months the mode makes them due; deaths during the
  month with claims paid at month end; lapses, shock lapses, and conversions at month end
  after deaths. The shock lapse is processed at the END of the final level-period month,
  `t = 12n − 1` (equivalently, immediately before the first ART premium falls due at
  `t = 12n`) — consistent with VM-20's "shock lapse in the final year of a level premium
  period" [R2] and the SOA study's measurement of lapse at the end of the level term [R4].
- **Age basis.** Age nearest birthday (ANB) **[std choice, sourced pattern]**: all four
  carriers with verifiable age rules use ANB [S2] [S3] [S5] [S6], and 2017 CSO / 2015 VBT are
  published in ANB variants [R3] [REG-R18]. Attained age = issue age + completed policy
  years, `dur(t) = t // 12` completed at the start of month `t`, so age changes on the
  anniversary and not on the birthday [S3] [S5] [S6].
- **Model points.** Single-policy model points (seriatim); one policy per model point with
  a count/weight field for grouping. VM-20 NPR is a seriatim quantity [R2], so seriatim
  granularity keeps the projection reusable for valuation feeds.
- **Units.** Currency in USD; face in dollars; rates per $1,000 where contractual
  [S2] [S3] [S5]; decrement rates are quoted **annual effective** throughout and
  subscripted `m` where the monthly rate actually applied is meant.

---

## Model point attributes

| Attribute | Type | Example (specimen anchor cell) |
|---|---|---|
| `policy_id` | str | "TL-000001" |
| `issue_date` | date | 2026-01-01 |
| `issue_age` | int (ANB) | 35 |
| `sex` | enum {M, F} | M |
| `rate_class` | enum {PPlusNT, PNT, StdNT, StdTob} | StdNT |
| `plan` | enum {T10, T20, T30} | T10 |
| `face_amount` | float ≥ 100,000 | 100,000 |
| `band` | int 1–4 (derived from face) | 1 |
| `premium_mode` | enum {A, SA, Q, M} | A (the anchor cell; the mode drives which months collect an instalment) |
| `policy_count` | float (weight) | 1.0 |
| `duration_inforce` | int (for in-force runs; 0 at issue) | 0 |

The example column is the specimen anchor cell M35/StdNT/$100k/10-yr [S6], which the worked
example below projects. Attribute menu per `product-spec.md` (issue-age grid **[std]**,
4 classes **[std]**, 4 bands [S5]/**[std]**).

## State variables

| Variable | Definition |
|---|---|
| `l(t)` | In-force policies at start of month t, i.e. at time t (l(0) = policy_count at issue) |
| `d(t)` | Deaths in month t |
| `x(t)` | Lapses (incl. shock lapse) at end of month t |
| `c(t)` | Conversions at end of month t |
| `AP(t)` | Annualized guaranteed gross premium for the policy year containing month t (rate-table row for that policy year, + fee) |
| `P(t)` | The modal instalment of `AP(t)` actually collected at BOM t; zero in a month no instalment is due |
| `dur(t)` | Completed policy years at the start of month t, `t // 12`; the contractual policy year is the 1-based label `dur(t) + 1` |
| `phase(t)` | LEVEL (dur(t) < n), PLT (dur(t) ≥ n, attained age < 95), EXPIRED (t ≥ 12(95 − x)) |
| `conv_elig(t)` | Boolean: dur(t) < n and attained age < 70 |

No account value, cash surrender value, loan, or shadow-account state exists for this
product [S3] [S6].

---

## Assumption inputs

Three classes are distinguished; keeping them in separate input structures is deliberate
architecture (the same split VM-20 makes between prescribed/guaranteed and prudent-estimate
elements [R2] [REG-R23]).

### (a) Contractual / guaranteed elements (from the spec — cited)

| Item | Value | Basis |
|---|---|---|
| Guaranteed premium scale | Level `AP` for n years, then guaranteed ART scale to age 95; full schedule printed at issue | [S3] [S6] |
| Anchor schedule (M35/StdNT/$100k/10-yr) | $140 (yrs 1–10); $764, $830, $992 (yr 15), $1,526 (yr 20), $4,250 (yr 30), $10,946 (yr 40), $30,965 (yr 50), $74,780 (yr 60 — the months `t = 708 … 719`, attained age 94, the final policy year to expiry at 95) | [S6] |
| Policy fee | $65/yr, level, inside `AP` | [S6] |
| Modal factors | SA 0.52 / Q 0.27 / M 0.08333 | [S6] |
| Death benefit | Level face; proceeds = face + pro-rata unearned premium − due unpaid premium | [S6] |
| Grace | 31 days | [S3] [S6] [S7] |
| Conversion window / credit | min(n, age 70); credit = one annual premium after year 1 | [S2] [S3] [S6] |
| Expiry | Attained age 95 | [S2] [S3] [S5] [S6] |

### (b) Current non-guaranteed scales

For this product there are none: premiums and death benefit are fully guaranteed
[S3] [S6], and the representative product sets the current PLT scale equal to the
guaranteed Jump-to-ART scale **[std]** (product-spec fn 10; graded current PLT scales
observed in the market [R4] are a documented variation, not modeled). This block is
intentionally empty so the input schema matches sibling products (UL etc.).

### (c) Behavioral / experience assumptions (best estimate)

| Assumption | Recommended public basis | Reference-model standardization |
|---|---|---|
| Best-estimate mortality | 2015 VBT primary tables (ANB, sex/smoker-distinct) with relative-risk (RR) tables for preferred fit [REG-R18], A/E-adjusted to ILEC 2012–2019 inter-company experience [R8] [REG-R19] (ILEC expected basis 2015 VBT RR100 [unverified]) | Class factors on 2015 VBT-style base: PPlusNT 0.80, PNT 0.90, StdNT 1.00, StdTob 1.75 **[std]** (fn A) |
| Guaranteed-basis mortality (for reserve feeds) | 2017 CSO, ANB, smoker-distinct, loaded [R3] [REG-R17] | Direct table lookup, no adjustment |
| Level-period lapse | SOA/LIMRA 2015–2022 Term & WL lapse study [R6]; older full-factor study [REG-R20] | Duration vector, fn B **[std]** |
| Shock lapse & PLT lapse | SOA U.S. Post-Level Term study (2021) [R4] [REG-R22] | Jump-ratio-keyed table, see Policyholder behavior **[std]** |
| PLT mortality deterioration | Same study [R4] [REG-R22] | Multiplier grading 3.50 → 2.00, see Policyholder behavior **[std]** |
| Conversion rate | SOA 2016 conversion experience study [R7] (2009–2023 SOA/LIMRA update in progress [R7, partly unverified](#uslib-term_life-r7)) | 1%/yr while eligible; 2% in final eligible year **[std]** (fn C) |
| Maintenance expense | — (no public basis in research set) | $30/policy/yr inflating 2%/yr **[std]** (fn D) |
| Acquisition expense | — | $300/policy at issue **[std]** (fn D) |
| Commission | — | 80% of premium year 1; 5% years 2–n; 2% PLT **[std]** (fn D) |
| Premium tax | — | 2.0% of collected premium **[std]** (fn D) |
| Premium mode | Modal factors from the specimen [S6] | A / SA / Q / M as a model point attribute, collected on the mode's own cycle; mode affects PLT behavior only via the optional [R4] factors **[std]** |

**Footnotes**

- **(A) Class factors [std].** The 2015 VBT provides 10 nonsmoker and 4 smoker RR tables
  for preferred-class fit [REG-R18]; the four factors {0.80, 0.90, 1.00, 1.75} are a
  compressed stand-in chosen so that StdNT reproduces the specimen anchor pricing cell
  [S6] and the NT spread stays inside the RR-table range. Calibration to actual RR tables
  is an implementation refinement.
- **(B) Level-period lapse [std].** Annual rates by policy year: 6%, 5%, then 4% for
  years 3 through n−2, year n−1: 6% (anticipatory rise — lapse rates begin increasing one
  to two policy years before the end of the level period [R6]), year n: shock lapse
  (below). Each is converted to the monthly rate applied within its policy year, except
  the shock — see *Monthly rates from annual assumptions*.
  Detailed study rates by sex/age/band/mode sit behind SOA paid data packages (research
  notes, Gaps); the vector is an order-of-magnitude standardization consistent with the
  public highlights: 30-year term lapse rates at attained ages 60+ run 1.0%–1.5% [R6], so
  for T30 the 4% mid-band grades to 1.5% from attained age 60 **[std]**.
- **(C) Conversion [std].** The public 2016 study landing page documents incidence
  analysis by age/sex/class/size but no headline rate was recorded in the research notes
  [R7]; 1%/yr (2% final year) is a placeholder magnitude. Treatment of the conversion cash
  flow: see Cash flow components.
- **(D) Expenses/commission [std].** No insurer expense or commission data appear in the
  retrieved public documents; these are round reference values for a complete gross cash
  flow statement. Replace with company-specific unit costs in any real application. The
  policy fee ($65 [S6]) is intended as the contractual funding of per-policy maintenance.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| x | Issue age (ANB); n = level term period in years; F = face amount |
| t | Month index, 0-based: t = 0, 1, …, 12(95 − x) − 1 (proj_len = 12(95 − x) months). Month t sits in policy year dur(t) + 1 |
| dur(t) | Completed policy years at the start of month t, `t // 12` |
| l(t) | In-force count at start of month t (time t); l(0) = 1 per unit model point |
| q(t) | Best-estimate **annual** mortality at the attained age of month t, incl. class factor and PLT multiplier; q_m(t) = 1 − (1 − q(t))^(1/12) is the rate applied in the month |
| w(t) | **Annual** lapse rate of the policy year containing month t; in policy year n it *is* the shock lapse. w_m(t) is the rate applied in the month, and the shock is not spread — see below |
| cv(t) | **Annual** conversion rate (0 outside eligibility window); cv_m(t) = 1 − (1 − cv(t))^(1/12) |
| AP(t) | Annualized guaranteed gross premium for the policy year containing month t |
| P(t) | Modal instalment collected at BOM t: modal factor × AP(t) in a due month, 0 otherwise [S6] |
| G(t) | Premium income in month t; K(t) commission; E(t) expenses; X(t) premium tax |
| DC(t) | Death claims incurred in month t; CV(t) conversion credit outflow |
| M(d) | PLT mortality multiplier at PLT duration d = dur(t) + 1 − n **in years** (d = 1 in the first PLT policy year, months t = 12n … 12n + 11) |
| J | Initial premium jump ratio = AP(12n)/AP(12n − 1), the first ART annualized premium (policy year n+1) over the last level one (policy year n), fee included [R4] [R2 convention](#uslib-term_life-r2) |

### Monthly rates from annual assumptions [std]

Every assumption in this product is published, calibrated and tabulated **annually**: the
mortality table is annual, the lapse vector is by policy year, the conversion rate is per
year. The monthly rates the recursion applies are derived from them at the constant-force
conversion, so that twelve months compound back to exactly the annual rate:

```
q_m(t)  = 1 − (1 − q(t))^(1/12)
cv_m(t) = 1 − (1 − cv(t))^(1/12)
w_m(t)  = 1 − (1 − w(t))^(1/12)               ordinary lapses only — see the shock below
```

**The shock lapse is the one exception and is NOT spread.** w(n−1), the annual rate of the
final level-period policy year, *is* the shock; it is applied in full at the end of the
final level-period month, `t = 12n − 1`, immediately before the first ART premium falls
due at `t = 12n` [R2] [R4]. The other eleven months of that policy year therefore carry
w_m = 0. Spreading it instead would lapse policies before the renewal notice that causes
them to lapse, and would leave a larger block to pay the first ART premium.

### Decrement order and recursion

Deaths first, then end-of-month voluntary decrements (lapse and conversion) applied to
survivors, with conversion and lapse treated as competing rates on the same survivor pool
**[std]**. Base case l(0) = 1 per unit model point; for t = 0, 1, …:

```
d(t)  = l(t) · q_m(t)
s(t)  = l(t) · (1 − q_m(t))                   survivors to end of month t
c(t)  = s(t) · cv_m(t)
x(t)  = s(t) · (1 − cv_m(t)) · w_m(t)
l(t+1)= s(t) · (1 − cv_m(t)) · (1 − w_m(t))
      = l(t) · (1 − q_m(t)) · (1 − cv_m(t)) · (1 − w_m(t))
```

Termination at expiry: l(t) = 0 for x + dur(t) ≥ 95, i.e. for t ≥ proj_len = 12(95 − x)
[S2] [S3] [S5] [S6]; the survivors of the last month t = 12(95 − x) − 1 expire rather than
decrement (the implementation books them as `pols_maturity`).

**Annual equivalence.** Because the ordinary rates compound back to their annual values
and the shock sits on a year boundary, the recursion collapses over any twelve months of
one policy year to `l(t+12) = l(t)(1 − q)(1 − cv)(1 − w)` — the annual-step recursion,
term for term. The in-force **at every anniversary** is therefore identical on the two
grids, to floating point, and a monthly run can be checked against an annual one on that
column alone. Nothing else agrees, and nothing else should: the cash flows are where the
finer grid does its work.

### Cash flows (per unit in force at issue)

```
G(t)  = P(t) · l(t)                           premium, BOM  [S6 schedule and modal scale]
K(t)  = k(t) · G(t)                           commission, BOM  [std]
X(t)  = 0.02 · G(t)                           premium tax, BOM  [std]
E(t)  = 300 · 1{t=0} + (30/12) · 1.02^(t/12) · l(t)
                                              maintenance/acquisition, BOM  [std]
DC(t) = F · d(t)                              death claims, EOM  [S6]
CV(t) = AP(t) · c(t) · 1{dur(t)≥1}            conversion credit, EOM  [S6]
NetCF(t) = G(t) − K(t) − X(t) − E(t) − DC(t) − CV(t)
```

with k(t) = 80% in policy year 1, 5% in policy years 2…n, 2% after **[std]**, applied to
the premium collected — so a modal payer earns it in instalments too. Three quantities
stay on the **annualized** premium AP and so do not move with the mode: the jump ratio J
and the conversion credit CV(t). The acquisition expense is mode-independent too, for a
different reason — it is a flat per-policy amount, not a fraction of any premium.

Maintenance expense accrues at a twelfth a month and inflates continuously,
`1.02^(t/12)`, rather than stepping at anniversaries. Twelve twelfths of $30 is the
annual charge, and the continuous factor puts a full policy year of it about 0.9% above
the anniversary-stepped figure; what changes materially against the annual grid is that a
decrementing block carries **less** of it, because it is borne by the in-force of each
month rather than of the anniversary.

Simplifications **[std]**: (i) the pro-rata unearned-premium refund on death and the
due-unpaid-premium deduction [S6] are not modeled — on the monthly grid the item is
bounded by one modal instalment, so it is immaterial by construction for a monthly payer
and at most one annual premium on the deceased cohort for an annual one; (ii) grace-period
mechanics [S3] [S6] are not separately modeled — lapse is treated as effective at the
monthiversary; (iii) reinstatement [S3] [S6] is not modeled as a decrement reversal.

### Conversion treatment [std choice — explained]

Two defensible treatments exist:

1. **Decrement with cost load (adopted).** Conversion removes the policy from the term
   block (`c(t)` above); the direct cash flow charged to the term product is the
   contractual conversion credit of one annual premium [S6]. The post-conversion mortality
   anti-selection documented by the SOA conversion studies [R7] is borne by the permanent
   product's model, not double-counted here. Adopted because it keeps the term model
   self-contained, uses only contractual cash flows, and matches how the conversion credit
   is actually paid (against the new policy's initial premium [S6]).
2. **Transfer-out (alternative).** Model conversion as a zero-cash-flow transfer to a
   companion permanent model point (lifelib-style linked runs). Preferable when the library
   is run as a linked term+permanent projection; the switch is an output-routing choice,
   not a different liability.

### Processing order (monthiversary)

Numbered order each month:

1. Check expiry (attained age 95) and terminate [S2] [S3] [S5] [S6].
2. Collect the modal premium if one is due this month — modal factor × AP, the factors
   being A 1.0 / SA 0.52 / Q 0.27 / M 0.08333 [S6], with the modal load inside the factor.
   Instalments start at issue and repeat on the mode's cycle, so annual mode collects in
   the first month of each policy year and monthly mode in every month.
3. Pay commission and premium tax on the premium collected **[std]**.
4. Incur 1/12 of the annual maintenance expense; acquisition expense in month 0 only
   **[std]**.
5. Apply deaths at `q_m`; pay claims at end of month: F (simplification (i) above).
6. Apply conversions at `cv_m` if within the eligibility window; pay the conversion credit
   of one **annualized** premium [S2] [S3] [S6] (before any lapse, so that conversion and
   lapse compete on the same survivor pool).
7. At the level-period-end monthiversary only — month `12n − 1` — apply the shock lapse to
   survivors in full **[std]** (per [R2] [R4] timing).
8. Apply ordinary lapses at `w_m` to the remaining survivors **[std]**.
9. Roll forward `l`.

---

## Policyholder behavior modeling

All dynamic formulas in this section are **[std]** standardizations calibrated to the
ranges published in the SOA 2021 PLT study [R4] [REG-R22]; none is itself a published
industry formula.

### Shock lapse at end of level period

Keyed to the initial premium jump ratio J = AP(12n)/AP(12n−1) — the first ART
annualized premium (policy year n+1) over the last level one (policy year n), the two
months either side of the level-period boundary — with the policy fee included in both
premiums — the jump definition used by both the SOA 2021 study [R4] and
VM-20's prescribed-shock table (premium increase per $1,000 including the policy fee)
[R2]. The shock is w(n−1), the lapse rate of the last level-period year:

| J (jump ratio) | Shock lapse w(n−1) **[std]** |
|---|---|
| ≤ 2.0 | 35% |
| 2.0 – 4.0 | 55% |
| 4.0 – 6.0 | 80% |
| 6.0 – 8.0 | 85% |
| > 8.0 | 90% |

Rationale: the study's observed Jump-to-ART shock lapses span 27%–96% and increase with
the jump ratio and attained age [R4]; the bucket values sit inside that envelope. The anchor
cell (J ≈ 5.46 [S6]-derived) takes 80% — which coincidentally equals the VM-20 prescribed
NPR shock for its 10-year level period jumping to ART with a ≥400% increase [R2], but note
the two are conceptually distinct (best estimate vs prescribed). Optional refinements
supported by the study: +5 pts at attained ages 60+ and −15 pts for monthly-mode policies
(monthly mode shows materially lower shock lapse [R4]) **[std]**.

### PLT lapse after the shock

Elevated but declining by PLT duration in **policy years**, d = dur(t) + 1 − n [R4]:
30% in the first post-level-term year (d = 1), 15% in the second (d = 2), 10% from the
third (d ≥ 3) **[std]**, until expiry. These are annual rates and are spread over their
twelve months at `w_m` like any other ordinary lapse.

### PLT mortality deterioration (anti-selection)

Multiplicative on the best-estimate base table:

```
q(t)   = q_base(x+dur(t)) · class_factor · M(d),   d = dur(t) + 1 − n ≥ 1  (i.e. dur(t) ≥ n)
M(1)   = min(8.0, 1 + 0.55 · (J − 1))          [std]
M(d)   = max(2.0, M(1) − 0.15 · (d − 1))       [std]  (grade to 200%, then level)
```

(M(d) = 1 during the level period, dur(t) < n. The deterioration is a multiplier on the
**annual** rate, applied before the monthly conversion, so it grades once a year as the
study measures it and not once a month.)

For the anchor cell J ≈ 5.46 gives M(1) = 3.45 ≈ 3.50 (the worked example uses 3.50).
Rationale: first-year Jump-to-ART deterioration observed at 154%–1,066% of level-period
mortality, increasing with the jump; deterioration declines over PLT durations, falling
below 200% after roughly 10 years [R4] — M(d) reaches 2.00 at d = 11 and stays level.
Monthly-mode policies show lower deterioration [R4]; an optional 0.75 multiplier on
(M(d) − 1) for monthly mode is supported **[std]**.

### Anticipatory lapse

The annual rate of policy year n−1 is set 2 points above the mid-duration level (6% vs
4% in the base vector), because lapse rates begin to rise one to two policy years before
the end of the level period [R6] **[std]**.

### Conversion

cv(t) = 1% per year while `conv_elig`, 2% in the final eligible policy year (option value
is highest just before the window closes) **[std]**; zero otherwise, and spread over the
months at `cv_m`. Anti-selective conversion interacts
with PLT deterioration — converters are disproportionately impaired lives [R7 scope;
magnitude not recorded](#uslib-term_life-r7) — so implementations linking term and permanent blocks should not
apply both a conversion cost load and full PLT deterioration to the same lives (see
Conversion treatment above).

---

## Worked example

Specimen anchor-cell model point M35 / Standard NT / $100,000 / 10-year plan / annual
mode, unit in-force. Contractual premiums from the specimen guaranteed schedule:
AP = $140 for the months of policy years 1–10 (`t = 0 … 119`), AP = $764 in policy year 11
(`t = 120 … 131`) and $830 in policy year 12 [S6]; J = 764/140 ≈ 5.46. Assumptions:
illustrative best-estimate annual q_base rising from 0.00080 (age 35) to 0.00160 (age 44)
— vector 0.00080, 0.00085, 0.00090, 0.00095, 0.00100, 0.00110, 0.00120, 0.00130, 0.00145,
0.00160 — then 0.00180/0.00200 (ages 45/46) with M(1) = 3.50, M(2) = 3.35 **[std]**; annual
lapse vector 6%, 5%, 4%×6, 6% (anticipatory), 80% (shock, at month 119 in full), 30%, 15%
**[std]**; commission 80%/5%/2%, premium tax 2%, maintenance $30/yr accruing monthly and
inflating 1.02^(t/12), acquisition $300 **[std]**. All flows per the recursion above
(premium/commission/tax/expense BOM, claims EOM, no discounting).

### The months of policy year 1 (t = 0 … 11)

The annual premium falls in month 0 and nothing else does, which is what an annual-mode
policy on a monthly grid looks like: one premium, one acquisition charge, then eleven
months of claims and a twelfth of the maintenance charge each.

| t | l(t) | Premium G | Claims DC | Comm K | Maint+Acq E | Tax X | Net CF | l(t+1) |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 140.00 | 6.67 | 112.00 | 302.50 | 2.80 | −283.97 | 0.994791 |
| 1 | 0.994791 | 0.00 | 6.63 | 0.00 | 2.49 | 0.00 | −9.13 | 0.989608 |
| 2 | 0.989608 | 0.00 | 6.60 | 0.00 | 2.48 | 0.00 | −9.08 | 0.984453 |
| 3 | 0.984453 | 0.00 | 6.57 | 0.00 | 2.47 | 0.00 | −9.04 | 0.979325 |
| 4 | 0.979325 | 0.00 | 6.53 | 0.00 | 2.46 | 0.00 | −9.00 | 0.974223 |
| 5 | 0.974223 | 0.00 | 6.50 | 0.00 | 2.46 | 0.00 | −8.95 | 0.969148 |
| 6 | 0.969148 | 0.00 | 6.46 | 0.00 | 2.45 | 0.00 | −8.91 | 0.964099 |
| 7 | 0.964099 | 0.00 | 6.43 | 0.00 | 2.44 | 0.00 | −8.87 | 0.959077 |
| 8 | 0.959077 | 0.00 | 6.40 | 0.00 | 2.43 | 0.00 | −8.83 | 0.954081 |
| 9 | 0.954081 | 0.00 | 6.36 | 0.00 | 2.42 | 0.00 | −8.78 | 0.949111 |
| 10 | 0.949111 | 0.00 | 6.33 | 0.00 | 2.41 | 0.00 | −8.74 | 0.944167 |
| 11 | 0.944167 | 0.00 | 6.30 | 0.00 | 2.40 | 0.00 | −8.70 | 0.939248 |

The month-0 decrement is the check on the rate conversion: q(0) = 0.00080 and w(0) = 0.06
give q_m = 1 − (1 − 0.0008)^(1/12) = 0.00006669 and w_m = 1 − (1 − 0.06)^(1/12) =
0.00514301, so l(1) = (1 − 0.00006669)(1 − 0.00514301) = 0.994791 ✓, and twelve such
months land on l(12) = 0.939248 — the annual model's l(1), exactly.

### The same frame summed into policy years (years 1–12)

Each row is the total of its twelve months; `l at BOY` is l(12(k−1)), the count entering
the policy year, which is the number the annual grid carried on the same row.

| Policy year | months t | l at BOY | Premium G | Claims DC | Comm K | Maint+Acq E | Tax X | Net CF |
|---|---|---|---|---|---|---|---|---|
| 1 | 0–11 | 1.000000 | 140.00 | 77.78 | 112.00 | 329.42 | 2.80 | −381.99 |
| 2 | 12–23 | 0.939248 | 131.49 | 77.99 | 6.57 | 28.32 | 2.63 | 15.98 |
| 3 | 24–35 | 0.891527 | 124.81 | 78.76 | 6.24 | 27.55 | 2.50 | 9.77 |
| 4 | 36–47 | 0.855096 | 119.71 | 79.73 | 5.99 | 26.95 | 2.39 | 4.65 |
| 5 | 48–59 | 0.820112 | 114.82 | 80.50 | 5.74 | 26.36 | 2.30 | −0.08 |
| 6 | 60–71 | 0.786520 | 110.11 | 84.92 | 5.51 | 25.79 | 2.20 | −8.30 |
| 7 | 72–83 | 0.754229 | 105.59 | 88.84 | 5.28 | 25.22 | 2.11 | −15.86 |
| 8 | 84–95 | 0.723191 | 101.25 | 92.28 | 5.06 | 24.67 | 2.02 | −22.79 |
| 9 | 96–107 | 0.693361 | 97.07 | 97.74 | 4.85 | 23.89 | 1.94 | −31.36 |
| 10 | 108–119 | 0.650814 | 91.11 | 104.13 | 4.56 | 23.53 | 1.82 | −42.92 |
| 11 | 120–131 | 0.129955 | 99.29 | 69.90 | 1.99 | 4.08 | 1.99 | 21.33 |
| 12 | 132–143 | 0.090395 | 75.03 | 56.28 | 1.50 | 3.15 | 1.50 | 12.59 |

Reading the table: the 80% shock lapse at the end of month 119 (the last month of policy
year 10, the last level-period year) collapses in-force from 0.649859 to 0.129955; in
policy year 11 the premium per survivor jumps 5.46× while expected claims per survivor
reflect q = 0.00180 × 3.50 = 0.0063 — the anti-selected PLT block barely clears its own
claims [pattern per R4]. Conversion is switched off (cv = 0) in this table to keep it to
one decrement narrative; enabling cv(t) per the behavior section removes a further ~1%/yr
of `s(t)` during policy years 1–10 and adds the CV(t) outflow. (This worked example uses
guaranteed premiums that are contractual [S6]; every decrement/expense number is
illustrative **[std]** — it is a mechanics check, not a pricing result.)

Cross-checks. The premium, commission and tax columns are the *same numbers the annual
grid produced*, because an annual-mode premium is collected on the anniversary and
weighted by the anniversary in-force under either grid: 91.11 in policy year 10 either
way. Claims and expenses are not, and the direction is the informative part — policy
year 11 pays 69.90 of claims against the annual grid's 81.87, because a block losing 30%
of its lives over the year is exposed for less of it than an anniversary weighting
assumes, and the maintenance charge falls from 4.75 to 4.08 for the same reason. The
shock arithmetic: l(120) = l(119)(1 − q_m(119)) × (1 − 0.80) = 0.649859 × (1 − 0.00013343)
× 0.20 = 0.129955 ✓, which is also l(9)(1 − 0.0016)(1 − 0.80) on the annual grid, since
the eleven ordinary-lapse-free months before it carry only mortality.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**. Reserve layers consume those flows
but are not reproduced here:

- **VM-20 minimum reserve** = seriatim NPR + max(0, DR − NPR-aggregate) etc., with term
  NPR on 2017 CSO, prescribed interest, prescribed lapses (6%/10% by level-period length,
  prescribed shock 25%–80%, 0% after final premium) and an NPR floor at the cost of
  insurance to the next paid-to-date; the deterministic exclusion test no longer applies to
  term [R2] [REG-R3]. The DR for post-2017 issues must assume 100% lapse at the end of the
  level term where PLT would otherwise be profitable — PLT profits cannot be capitalized;
  PLT losses must be reflected [R2]. A projection feeding VM-20 must therefore be able to
  run with (a) prudent-estimate behavior per these notes and (b) the prescribed
  NPR/PLT-override assumption sets, from the same cash flow engine.
- **Pre-PBR in-force (A-830, the model regulation known outside the manual as "Regulation
  XXX")**: basic reserves = **max(segmented, unitary)** under the contract segmentation
  method [REG-R154 ¶21](#uslib-reg-r154); deficiency reserves as **quantity A less the basic reserve** [REG-R154 ¶17](#uslib-reg-r154),
  with X-factor select mortality confined to the **first segment** [REG-R154 ¶18](#uslib-reg-r154). The
  valuation table is **date-split, not 1980 CSO flat**: 1980 CSO with elective select
  factors **before 1 January 2004**, and the **2001 CSO Mortality Table from 1 January 2004**
  for basic reserves, deficiency reserves and the tabular cost of insurance
  [REG-R154 ¶¶16, 17, 23](#uslib-reg-r154). The quantitative substrate A-830 does not restate — what a basic
  reserve *is* (¶¶11–13), the minimum reserve behind the deficiency definition (¶¶19–20) and
  the maximum valuation interest rates (¶¶7–10) — is **A-820** [REG-R153]. Both appendices are
  now read at first hand and this pointer no longer rests on Model #830 alone [R1] [REG-R6].
- **Asset adequacy / cash flow testing** sits under VM-30/ASOP 22 [REG-R29] with ASOP 7
  governing the cash flow analysis itself [REG-R27] and ASOP 56 governing the model
  [REG-R32]; VM-20 practice detail in the Academy practice note [REG-R23] and assumption
  governance in the Academy resource manual [REG-R25].
- **Tax reserves**: 92.81% of the NAIC-method reserve, floored at net surrender value
  (zero for term), capped at statutory [REG-R16]. **GAAP/LDTI**: the same projected cash
  flows feed the LFPB with annually updated assumptions and single-A discounting through
  OCI [REG-R34] [unverified — source not fetched; corroborated summaries only].
  Reinsurance reserve financing of XXX
  term: AG 48 / Model #787 [REG-R11] [REG-R12].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order of economic impact for a level-term block:

1. **PLT shock lapse × mortality deterioration.** These two are jointly calibrated to the
   premium jump [R4]; moving one without the other misstates the PLT tail badly. Because
   VM-20 forces PLT profits to zero in the DR [R2], PLT optimism cannot help statutory
   results but PLT pessimism (deterioration above premium loadings) flows straight through.
2. **Best-estimate mortality level and slope.** The level-period margin is thin (see
   worked example — premiums ≈ expected claims at Standard NT); a few basis points of A/E
   [R8] [REG-R19] move the block's lifetime result materially.
3. **Level-period lapse.** Term with no cash value is lapse-supported in early durations
   (acquisition strain recovery) and lapse-sensitive before the shock (each anticipatory
   lapse in policy year n − 1 — policy year 9 of a T10 — [R6] forfeits a year of level
   premium against no benefit).
4. **Conversion incidence.** Converts remove healthy-ish premium payers and (in linked
   models) deliver anti-selected lives to the permanent block [R7]; sensitivity grows with
   the conversion window length.
5. **Expenses/commission [std]** matter mainly through the acquisition strain and the tiny
   PLT in-force tail (fixed per-policy costs on a shrinking block).

Known modeling pitfalls:

- **Shock timing double-count.** Applying the shock lapse both at the end of month
  `12n − 1` and the start of month `12n`, or **spreading it across the twelve months of
  policy year n at `w_m`**, changes the PLT premium base materially. The second of those
  is the live hazard on a monthly grid, and it is not a rounding difference: spreading an
  80% annual rate lapses roughly half the block before the ART renewal notice that is the
  cause of the lapse, and hands a smaller block the first ART premium. The shock belongs
  at the single point immediately before that premium — month `12n − 1`, in full
  [R2] [R4] **[std]**.
- **Jump ratio definition.** Include the policy fee in both numerator and denominator —
  the 2021 SOA study defines the jump including the fee (the 2014 study did not) [R4], and
  VM-20's shock table keys on premium increase per $1,000 including the fee [R2].
  Fee-in/fee-out inconsistency silently shifts a policy across shock buckets. **The formulaic
  engine uses the opposite convention, so the two must not be conflated:** A-830 ¶5's
  segmentation ratio is on guaranteed gross premium *per thousand of face amount*, "ignoring
  policy fees only if level for the premium paying period" — and the $65 fee is level for the
  whole period [S6], so the fee comes **out** there [REG-R154 ¶5](#uslib-reg-r154). One product, two
  premium-ratio conventions: **fee-in** for behaviour and the VM-20 NPR shock [R2] [R4],
  **fee-out** for A-830 segmentation. At the anchor cell they differ by nearly a factor of two
  (≈5.46 against ≈9.32) [S6]-derived.
- **Deterioration base.** M(d) multiplies the *best-estimate base* mortality, not the
  guaranteed/valuation table; applying it to 2017 CSO (already loaded [R3]) double-counts
  margin.
- **Converting the rate at the wrong point.** `q_m` and `w_m` are taken from the **fully
  loaded annual** rate — base × class factor × M(d) for mortality — not from the base
  table before the multipliers. Converting first and multiplying after gives a different
  number wherever a multiplier is not 1, which is the whole post-level term: at M(1) =
  3.50 the two differ by 0.21% of the monthly rate, compounding over the PLT tail.
- **Modal factor double-count.** The modal load lives in the modal factor [S6], so the
  premium collected is `factor × AP` and nothing else scales it. Three quantities stay on
  the annualized AP and must not be modalized: the jump ratio (the shock buckets are
  calibrated on annualized premiums [R4]) and the conversion credit (contractually one
  annual premium [S6]). The acquisition expense must not be modalized either, being a
  flat per-policy charge rather than a fraction of premium.
- **ANB/ALB mismatch.** Model ages, rate table lookups, and mortality tables must share
  the ANB basis [S2] [S3] [S5] [S6] [R3]; a silent ALB table import shifts mortality by half a
  year of age.
- **Expiry handling.** The guaranteed schedule ends at attained age 95 [S6]; projecting
  ART premiums past 95, or terminating a year early, corrupts the tail. The correct rule
  is `l(t) = 0 for x + dur(t) ≥ 95`: the last projected month is `t = 12(95 − x) − 1`, the
  last month of the policy year running from attained age 94 to expiry at 95; testing
  `x + dur(t) ≥ 94`, or ending the frame twelve months early, drops that whole year.
- **Banding on face decrease.** A requested face decrease re-scales premium excluding the
  fee (((a − b) × c) + b [S6]) and can cross a band boundary [S3]; implementations that
  re-derive `band` from `face_amount` each period handle this automatically.

---

*Companion documents: `product-spec.md` (contract terms), `sources.md` (citations).*

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-term_life-r1
[R2]: #uslib-term_life-r2
[R3]: #uslib-term_life-r3
[R4]: #uslib-term_life-r4
[R6]: #uslib-term_life-r6
[R7]: #uslib-term_life-r7
[R8]: #uslib-term_life-r8
[REG-R11]: #uslib-reg-r11
[REG-R12]: #uslib-reg-r12
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R17]: #uslib-reg-r17
[REG-R18]: #uslib-reg-r18
[REG-R19]: #uslib-reg-r19
[REG-R20]: #uslib-reg-r20
[REG-R22]: #uslib-reg-r22
[REG-R23]: #uslib-reg-r23
[REG-R25]: #uslib-reg-r25
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R3]: #uslib-reg-r3
[REG-R32]: #uslib-reg-r32
[REG-R34]: #uslib-reg-r34
[REG-R6]: #uslib-reg-r6
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
