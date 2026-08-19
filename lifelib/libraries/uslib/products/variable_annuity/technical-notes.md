# Technical Notes

**Status:** Draft, 2026-08-04; AP&P Manual appendix material added 2026-08-06. All cited
sources accessed 2026-08-04 **except** [REG-R151] (AG 33), [REG-R153] (A-820), [REG-R156]
(A-250) and [REG-R157] (A-255), accessed **2026-08-06**.

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite product defined in `product-spec.md` (same directory). It is
not any single insurer's product. **[S#]/[R#]** tags resolve against
`_research/variable-annuity.md`; **[REG-R#]** tags resolve against the single shared
cross-product numbering space **R1–R157** curated at
`references/regulatory-and-actuarial-references.md` (R1–R34 from
`_research/regulatory-actuarial.md`, R35–R72 from
`_research/regulatory-actuarial-annuities.md`, and **R151–R157** the AP&P Manual
appendix items read at first hand on 2026-08-06 — of which four are cited here, **AG 33**
[REG-R151], **A-820** [REG-R153], **A-250** [REG-R156] and **A-255** [REG-R157] — with
most of the **R73–R149** block unused). **[std]** marks a standardization
introduced for the reference implementation; **[unverified]** marks a claim the research
file could not confirm against a retrieved document. **Every parameter value below is
identical to the value in `product-spec.md`.** The mechanics anchor is the single-carrier
chassis contract [S1] [S2] [S3].

**Relationship to sibling documents.** The *separate-account charge-accrual convention* — a
monthly discretization of daily fund-expense and asset-charge accrual, `(1 + r)(1 − e/12)(1 −
m/12)` — is specified once in `products/variable_ul/technical-notes.md` and reused here. Two
qualifications, because that file is a **life** file: it applies the convention to *subaccount
values* directly and never carries a unit count, whereas the unit ledger `AV = Σ U_i V_i` used
below is written out here in full; and its charge stack includes a **cost of insurance on a net
amount at risk** and an **IRC §7702 corridor**, neither of which exists in a VA — a VA's
guarantees are instead a **GMDB benefit base** and a **GLWB benefit base**, shadow accounts that
never fall with the market. Nothing on the life side's NAAR/corridor path may be carried
across. *Generic GLWB machinery*
is shared with `products/fixed_indexed_annuity/technical-notes.md` (sibling deliverable in
this library) and **referenced rather than restated** where the two products agree — namely
**activation timing** (that file's RMD-clustered activation hazard), **RMD relief**, and the
**post-depletion phase**. Two items on that list are *not* shared and are written out below:
that file carries **no cohort construction** (the cohort method used here is VM-21's [R1]),
and its excess-withdrawal rule reduces the benefit base **pro rata on the excess only**, with
no dollar-for-dollar reduction for the guaranteed portion — whereas the GWB here *is*
reduced dollar-for-dollar by the non-excess portion first [S1]. The one structural difference
is decisive: in an FIA the account value is driven by a floored index-credit formula, whereas
here **separate-account performance drives the account value directly and can fall without
limit**, so the guarantee is far more path-dependent and its cost cannot be obtained from a
deterministic run.

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows — premium, withdrawals, surrender
  proceeds, death benefits, insurer-funded post-depletion GLWB payments, charge income and
  expenses — for a single-contract model point, per scenario. Reserves are not computed
  (see *Valuation and reserve pointers*).
- **Projection frequency: monthly** **[std]**. The base contract charge is contractually
  assessed **daily** as a percentage of the average daily account value of the Investment
  Divisions [S2]; the model applies one-twelfth of the annual rate at each month end
  **[std]**. Do not also compound daily — pick one discretization and document it, because
  reconciling to an admin system requires knowing which was used.
- **Event calendar.** Contract Quarterly Anniversaries fall at the end of months
  t ≡ 0 (mod 3); Contract Anniversaries at the end of months t ≡ 0 (mod 12) **[std]**. Rider
  charges are assessed at the *end* of a contract quarter, following the disclosed rule that
  the first deduction occurs at the end of the first quarter following election [S4] / on the
  three-month anniversary of the rider effective date [S8].
- **Timing convention.** Within month t: policyholder transactions at the beginning of the
  month (BOM); unit value growth over the month; charges, guarantee-base events and
  decrements at the end of the month (EOM) **[std]**.
- **Age basis: age nearest birthday (ANB)** **[std]**. Rationale: VM-21 prescribes the 2012 IAM
  **Basic** Table (improved to Dec. 31, 2017 on Scale G2) for standard-projection mortality
  [R1], and the 2012 IAM **Period** Table it underlies is printed **age nearest birthday**
  [REG-R59]; and the GAWA%, GMDB roll-up and step-up eligibility bands are all attained-age
  lookups [S1] [S3].
- **Model points.** Single-contract model points projected on an expected
  (probability-weighted) basis; survivorship factors multiply per-contract cash flows. No
  aggregation, no cohort splitting except the utilization cohorts described below.
- **Scenarios.** Subaccount gross returns are exogenous per-scenario inputs; see
  *Stochastic requirement*.
- **Rounding.** Full precision carried internally; reported cash flows to cents **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `issue_age` | int (ANB) | 60 **[std]** |
| `sex` | enum {M, F} | M **[std]** |
| `designated_lives` | enum {single, joint} | single **[std]** |
| `tax_status` | enum {NQ, Q} | NQ **[std]** |
| `premium_single` | currency | 100,000 **[std]** |
| `premium_tax_rate` | rate | 0.000 **[std]**, within 0.0%–3.5% [S2] |
| `alloc[i]` | vector, sums to 1 | (0.60, 0.40) **[std]** |
| `fund_expense[i]` | annual rate | (0.0095, 0.0065) **[std]**, within 0.52%–2.28% [S2] |
| `glwb_option` | enum {Value, Core, Plus} | Core [S3] |
| `glwb_stepup_basis` | enum {annual_CV, highest_quarterly_CV} | annual_CV [S3] |
| `gmdb_option` | enum {basic, rollup, HQAV, combination} | rollup [S3] |
| `cdsc_schedule` | vector by completed years since premium receipt | 8.5/7.5/6.5/5.5/5.0/4.0/2.0/0.0 % [S2] |
| `rate_sheet_date` | date (first-class assumption) | 2026-04-27 [S3] |
| `issue_date` | date | — |
| `av_initial`, `gwb_initial`, `bb_initial`, `rb_initial` | currency (in-force cells) | 0 / 0 / 0 / 0 at issue |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `U_i(t)` | units held in subaccount i | on every unit purchase/cancellation |
| `V_i(t)` | unit value of subaccount i | monthly growth |
| `AV(t)` | contract value = Σ_i U_i(t)·V_i(t) | derived |
| `GWB(t)` | Guaranteed Withdrawal Balance (GLWB benefit base) [S1] | premium, withdrawal, bonus, step-up, adjustment |
| `GAWA(t)` | Guaranteed Annual Withdrawal Amount [S1] | fixed at first withdrawal; excess withdrawals, step-ups, bonus, premium |
| `BB(t)` | Bonus Base [S1] | premium, excess withdrawal, step-up |
| `bonus_end(t)` | Contract Anniversary on which the Bonus Period ends [S1] | restarts on a Bonus-Base-increasing step-up |
| `ADJ(t)` | GWB Adjustment amount [S1] | premium; consumed or voided on the GWB Adjustment Date |
| `RB(t)` | GMDB roll-up Benefit Base [S1] | annual roll-up; year-end withdrawal adjustment; premium |
| `NP(t)` | cumulative Net Premiums (a GMDB floor) [S1] | premium |
| `RP(t)` | Remaining Premium (the CDSC basis) [S2] | premium; withdrawal of premium incl. charges |
| `SumW_y` | cumulative withdrawals in the current Contract Year [S1] | withdrawal; reset each anniversary |
| `gawa_pct_fixed` | GAWA% locked at the first withdrawal by attained age [S1] | once |
| `forlife_flag` | For Life Guarantee in effect (true from issue at age 59½+) [S1] | once |
| `depleted_flag` | AV has reached zero with the GLWB in force [S1] | once |
| `phi_G(t)`, `phi_D(t)` | current GLWB / GMDB charge rates | fifth-anniversary reset [S1] |
| `l(t)` | in-force probability at end of month t; `l(0) = 1` | monthly decrements |

---

## Assumption inputs

Three classes are distinguished explicitly, because they behave differently under
governance: (a) cannot be changed by the insurer; (b) can, subject to ASOP No. 2
discipline for non-guaranteed elements, which expressly covers variable deferred annuities
[REG-R26]; (c) is the modeler's view and must be justified under ASOP No. 56 [REG-R32].

### (a) Contractual / guaranteed elements

| Input | Value | Basis |
|---|---|---|
| Maximum base contract asset charge | 1.30% p.a. of average daily separate-account value | [S2] |
| Maximum annual contract maintenance charge | $35, waived at contract value ≥ $50,000 | [S2] |
| CDSC schedule (by completed years since premium receipt) | 8.5 / 7.5 / 6.5 / 5.5 / 5.0 / 4.0 / 2.0 / 0.0 % | [S2] |
| Free withdrawal | 10% of Remaining Premium per Contract Year, minus earnings; earnings out first | [S1] |
| No CDSC on withdrawals within the GLWB annual limit | — | [S1] |
| Excess-withdrawal algebra (GWB, GAWA) | dollar-for-dollar then pro rata | [S1] |
| GMDB withdrawal adjustment | d-f-d up to `ρ × RB(prior anniversary)`, pro rata above, applied at Contract Year end | [S1] |
| Benefit base caps | GWB and Bonus Base capped at $10,000,000 | [S1] |
| GMDB growth cutoff | Contract Anniversary preceding the oldest Covered Life's 81st birthday | [S1] |
| For Life Guarantee trigger | Designated Life 59½ or older | [S1] |
| Guaranteed maximum GMDB charge | 1.80% p.a. of the GMDB Benefit Base | [S2] |
| Guaranteed maximum GLWB charge | 3.00% p.a. of the GWB | **[std]**, observed 1.20%–3.00% by option/vintage [S1] |
| Maximum single GLWB charge increase | +0.25% (Core tier) | [S1] |
| Charge-increase frequency | each fifth Contract Anniversary, with irrevocable opt-out | [S1] |
| Latest Income Date | Contract Anniversary at owner age 95 | [S2] |

### (b) Insurer-declared current elements (snapshot; revisable NGEs [REG-R26])

Snapshot dated **2026-04-27**, the rate sheet date [S3]. Rate sheets carry an
explicit "can be superseded at any time" clause with a 10-day advance-filing commitment
[S3] [S5] [S8], so the rate-sheet date is a first-class model input, not metadata.

| Input | Value | Basis |
|---|---|---|
| Current base contract asset charge | 1.30% p.a. (= the contractual maximum) | [S2] |
| — M&E component `m` | 1.00% p.a. | **[std]** decomposition (see spec footnote 6) |
| — administrative component `α` | 0.30% p.a. | [S7] component; split **[std]** |
| Current GLWB charge `phi_G` | 1.25% p.a. of GWB | [S3] |
| Current GMDB charge `phi_D` | 0.90% p.a. of RB | [S2] [S3] |
| Bonus percentage `b` | 6.00% of Bonus Base | [S3] |
| GMDB roll-up percentage `ρ` | 6.00% (age ≤ 69 at election); 5.00% (age ≥ 70) | [S3] |
| GWB Adjustment percentage `s` | 105% | [S3] |
| GAWA% grid `g(a)` (Single, Core) | 35–59: 4.00%; 60–64: 4.00%; 65–69: 5.55%; 70–74: 5.75%; 75–80: 5.95%; 81+: 6.20% | [S3] |
| Fund expenses `e_i` | 0.95% equity / 0.65% fixed income | **[std]** within 0.52%–2.28% [S2] |

*Optional variant modules, each fully parameterized by cited values.* (i) **VIX-linked fee
reset**: `phi(k) = phi_0 + 0.05% × [avg(VIX²)/33 − 10]`, clipped to ±0.40% p.a. per quarter
and to [0.60%, 2.50%], quarterly deduction = annual ÷ 4 [S4] [S6]. (ii) **Treasury-linked
roll-up rate**: 20-day average 10-year CMT ending the 15th of the last month of the prior
quarter, **+1.00%** (or **+1.50%** before the first withdrawal), rounded to 0.10%, floored
**4%**, capped **8%** [S7]. (iii) **Two-table post-depletion payout**, Table A while
AV > 0 and a lower Table B once AV = 0 [S8].

### (c) Behavioral / experience assumptions (modeler's view; public bases recommended)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality | **2012 IAM Basic Table with Projection Scale G2**, generational, × 100% A/E **[std]**; monitor against the 2020–2024 Individual Payout Annuity Mortality Experience Study (23 parent groups, 3.1m contract-years, 143,190 deaths, results shown against the 2012 IAM basis) | [REG-R59] [REG-R61]; VM-21 prescribes percentages of the 2012 IAM Basic with G2 [R1] [REG-R35] |
| Prescribed-projection mortality | 2012 IAM Basic improved to Dec 31, 2017 using Scale G2, **no further improvement** in the projection | [R1] |
| Mortality basis warning | Do **not** use CSO/VBT life tables — annuitant mortality is a different and generally lighter basis | [REG-R59] |
| Base surrender | VM-21 Table 6.3 "under 50% ITM" column as the base level **[std]**: 4.0% p.a. in the surrender-charge period, 25.0% in the first year after it, 15.0% thereafter | [R1] |
| Moneyness adjustment | VM-21 §7.B.1 Alternative Methodology multiplier (below) | [R1] |
| Withdrawal-year factor | × 60% in any contract year with a projected withdrawal, for GMWB contracts | [R1] |
| Surrender at AV = 0 | 0% for a GMWB contract | [R1] |
| GLWB utilization | Withdrawal Delay Cohort Method with a "never withdraw" cohort weight of **0.20** (non-qualified GMWB) or **0.05** (tax-qualified GMWB); once exercised, withdraw **90%** of the guaranteed maximum each year. The **base run** instead activates at age 70 and withdraws **100%** of GAWA **[std]**, matching the §6.C.3 GAPV construction — see *GLWB utilization* | [R1]; base run **[std]** |
| Utilization caution | The Academy warns a material "never utilize" cohort may understate reserves and suggests shifting it into very-late cohorts (policy year 25/30 or age 95); it cites SOA evidence that fewer than 5% of FIA contract holders age 80+ never utilized | [R5] [REG-R67] |
| Utilization empirical anchor | ~79% of owners taking withdrawals withdrew at or near the maximum (up to 110%), ~55% between 90% and 110%; activation clusters at the RMD age | [REG-R64] [R13] — **[unverified]**, from study summaries, not the paid report |
| Maintenance expense | VM-21 §6.C.2 prescribed: `$100 × 1.025^(valuation year − 2015)` per contract in year 1, inflating 2.5% p.a., **plus 7 bps of projected account value** each year (company-administered) | [R1] |
| Acquisition expense | Not modeled in the base run **[std]** | — |

Two cautions the research file records and this model inherits. First, the detailed SOA/LIMRA
2022–2024 VA behavior study (17 companies, 11.5m contracts, $1.5tn contract value, 625,000+
surrenders, 4m withdrawals totalling $56.7bn) is a **paid data package**; only its landing
page was retrieved [R13] [REG-R64]. Second, the Academy's sample utilization tables are built
for a **non-qualified FIA**, not a VA, and must be applied with care [R5].

---

## Cash flow components and recursions

### Notation (defined once, used throughout and consistent with `product-spec.md`)

| Symbol | Meaning |
|---|---|
| `t` | policy month index, t = 1, 2, …; `y = ceil(t/12)` contract year; `k = ceil(t/3)` contract quarter |
| `x` | issue age (ANB) = 60 **[std]**; attained age `a(t) = x + y − 1` |
| `i` | subaccount index, i ∈ {1, 2} (1 = equity, 2 = fixed income) |
| `U_i(t)`, `V_i(t)` | units and unit value; `SA_i(t) = U_i(t)·V_i(t)`; `AV(t) = Σ_i SA_i(t)` |
| `w_i(t)` | value weight `SA_i(t) / AV(t)` (the pro-rata deduction key) |
| `r_i(t)` | gross fund return of subaccount i over month t (scenario input) |
| `e_i` | annual fund expense ratio (0.0095, 0.0065) **[std]** |
| `m`, `α` | annual M&E 0.0100 **[std]** and administrative asset charge 0.0030 [S7]; `m + α = 0.0130` [S2] |
| `P(t)`, `τ` | gross premium at BOM t; premium tax rate 0.000 **[std]** (range 0–3.5% [S2]) |
| `W(t)` | gross withdrawal, **measured inclusive of withdrawal charges, MVAs, advisory fees and other charges** for all guarantee calculations [S1] |
| `E(t)`, `N(t)` | excess and non-excess portions of `W(t)` [S1] |
| `L(t)` | annual withdrawal limit `= max(GAWA(t), RMD(t))` (RMD term active only for qualified contracts) [S1] |
| `c(t)` | contingent deferred sales charge on `W(t)` [S2] |
| `f_c` | annual contract fee $35, waived at `AV ≥ 50,000` [S2] |
| `phi_G`, `phi_D` | annual GLWB (0.0125) and GMDB (0.0090) charge rates [S3] |
| `b`, `ρ`, `s` | bonus 0.0600, GMDB roll-up 0.0600, GWB Adjustment 1.05 [S3] |
| `g(a)` | GAWA% at attained age a [S3] |
| `M(t)` | in-the-moneyness ratio (benefit base ÷ account value) |
| `λ(t)` | dynamic lapse multiplier |
| `q^d(t)`, `q^w(t)` | monthly mortality and surrender rates; `l(t)` in-force probability |

Monthly conversions **[std]**: asset charges use simple `annual/12` (matching the
average-daily-value accrual [S2]); decrements use `1 − (1 − q_annual)^(1/12)`; the GMDB
roll-up and GLWB bonus are credited **annually at the Contract Anniversary**, matching the
contract [S1].

Dimensional check: `phi_G/4 × GWB` is currency per quarter; `m/12 × SA_i` is currency per
month; `g(a) × GWB` is currency per year; `E(t)/CV` is dimensionless.

### Account value and unit mechanics

    AV(t) = Σ_i U_i(t) · V_i(t)

    Unit value (monthly discretization of a daily accrual [S2]) [std]:
    V_i(t) = V_i(t−1) · (1 + r_i(t)) · (1 − e_i/12) · (1 − (m + α)/12)

Charges assessed **per unit of value** (fund expenses, M&E, administrative asset charge)
live inside `V_i`; charges assessed **per contract or on a benefit base** are collected by
cancelling units, leaving `V_i` untouched — `ΔU_i = C · w_i(t) / V_i(t)`, so `ΔAV = C`
**[std]**. The pro-rata key is cited for the annual contract maintenance charge, "deducted
proportionally" [S2]; extending it to the rider charges is **[std]** (spec footnote 8).

### Charge stack with exact assessment bases

| Charge | Rate | Assessment base | Frequency | Mechanism |
|---|---|---|---|---|
| Fund expense | 0.95% / 0.65% p.a. **[std]** | fund net assets | daily → monthly **[std]** | inside unit value (paid to the fund, not the insurer) |
| M&E risk charge | 1.00% p.a. **[std]** | average daily separate-account value | daily → monthly **[std]** | inside unit value |
| Administrative asset charge | 0.30% p.a. [S7] | average daily separate-account value | daily → monthly **[std]** | inside unit value |
| Annual contract fee | $35, waived at AV ≥ $50,000 [S2] | per contract | Contract Anniversary [S2] | unit cancellation, pro rata [S2] |
| GLWB rider charge | 1.25% p.a. [S3] | **GWB (benefit base), not account value** [S1] [S3] | quarterly at rate/4 [S1] | unit cancellation, pro rata **[std]** |
| GMDB rider charge | 0.90% p.a. [S2] [S3] | **GMDB Benefit Base** [S3] | quarterly at rate/4 **[std]** | unit cancellation, pro rata **[std]** |
| CDSC | 8.5%→0.0% by completed years since premium receipt [S2] | Remaining Premium withdrawn [S2] | on withdrawal | netted from withdrawal proceeds |
| Premium tax | 0.0% base **[std]**, 0.0–3.5% range [S2] | premium | at premium / annuitization [S2] | deducted from premium |

**The single most important structural point about this stack:** the two rider charges are
levied on benefit bases that *rise* when markets fall, so rider income is naturally
counter-cyclical — until account value reaches zero, at which point **the fee stops** [S4]
precisely when the guarantee is paying. A model that keeps charging after depletion
overstates revenue in exactly the scenarios that drive the CTE70 tail.

### Monthly processing order

At BOM of month t:

1. Advance `y`, `k`, `a(t)`; reset `SumW_y` if a new contract year began. If
   `depleted_flag` is set, run the post-depletion routine (step 9) and skip steps 2–7.
2. **Premium.** Net premium `P(t)·(1 − τ)` buys units at `V_i(t−1)` per `alloc[i]`. Then
   [S1]: `GWB += P(1−τ)`; `BB += P(1−τ)`; `NP += P(1−τ)`; `RP += P(t)`;
   `RB += P(1−τ)` (premiums received in the first Contract Quarter are treated as of the
   Issue Date [S1]); if a first withdrawal has already occurred,
   `GAWA += g(a_first) · P(1−τ)`, or `g × ΔGWB` if the $10m cap binds [S1]. `ADJ` increases
   by `s · P(1−τ)` for premiums before the first anniversary after endorsement and by
   `P(1−τ)` for later premiums [S1].
3. **Withdrawal.** Given `W(t)`, **in this order** — the first bullet must run before `L` is
   formed, or a first withdrawal would be tested against `GAWA = 0` and score entirely as
   excess:
   - If this is the first withdrawal, fix `gawa_pct_fixed = g(a(t))` and set
     `GAWA = g(a(t)) · GWB` on the **pre-withdrawal** `GWB` [S1]; mark the year as
     bonus-ineligible [S1]; void `ADJ` [S1].
   - `SumW_y += W(t)`; `L = max(GAWA, RMD)`; `E = min(W, SumW_y − L)` if `SumW_y > L` else
     0; `N = W − E` [S1].
   - **CDSC.** Charge-free amount = earnings `max(0, AV − RP)` plus
     `max(0, 0.10·RP − earnings)`, i.e. 10% of Remaining Premium with earnings coming out
     first [S1]; aged-out premium is free [S1]; **no CDSC applies to cumulative withdrawals
     within `L`** [S1]. On the chargeable portion apply the schedule by completed years
     since receipt of the premium being withdrawn [S2].
   - Cancel units pro rata for `W(t)` (which is gross of all charges [S1]); reduce `RP` by
     the premium portion withdrawn including withdrawal charges [S2].
   - **GLWB base update** (`CV_pre` = AV after `N` has been deducted):

         If SumW_y ≤ L:  GWB ← max(GWB − W, 0);  GAWA unchanged
         If SumW_y > L:  GWB ← max( (GWB − N) · (1 − E / CV_pre) , 0 )
                         GAWA ← min( GAWA · (1 − E / CV_pre) , GWB )
                         BB   ← min( GWB , BB )                        [S1]

   - **GMDB adjustment is accrued, not applied**: record the withdrawal against the
     year-to-date allowance `ρ · RB(prior anniversary)`; the adjustment is applied at the
     **end of the Contract Year** [S1].
4. **Unit value growth** over month t per the formula above.
5. **EOM quarterly charges** (t ≡ 0 mod 3): `Fee_G = (phi_G/4)·GWB`,
   `Fee_D = (phi_D/4)·RB`; cancel units pro rata [S1] [S3].
6. **EOM annual contract fee** (t ≡ 0 mod 12): `f_c` if `AV < 50,000`, cancelled pro rata
   [S2].
7. **EOM anniversary guarantee events** (t ≡ 0 mod 12), in this order **[std]**:
   1. Apply the accrued GMDB withdrawal adjustment: dollar-for-dollar up to
      `ρ · RB(prior anniversary)`, then `RB × (proportional CV reduction from the excess)`
      [S1].
   2. GMDB roll-up: if `a(t)` is at or before the anniversary preceding the oldest Covered
      Life's 81st birthday, `RB ← RB · (1 + ρ)` [S1].
   3. GLWB bonus: if no withdrawal occurred in contract year `y` **and** `y ≤ bonus_end`,
      `GWB ← GWB + b · BB`; if after the first withdrawal,
      `GAWA ← max(g · GWB, GAWA_before_bonus)` [S1]. The bonus does not change `BB` or
      `ADJ` [S1].
   4. Step-up: if `AV > GWB`, then `GWB ← AV`; `BB ← max(GWB, BB)`; restart the Bonus
      Period (`bonus_end ← y + 10`) if the step-up occurs on or before the anniversary
      following the Designated Life's 80th birthday [S1]; if after the first withdrawal,
      `GAWA ← max(g · GWB, GAWA)` [S1].
   5. GWB Adjustment Date test — at the later of the anniversary on/after age 70 and the
      12th Contract Anniversary, if no withdrawal has ever been taken then
      `GWB ← max(GWB, ADJ)` and the provision terminates [S1].
   6. If `forlife_flag` is false and `GWB < GAWA`, set `GAWA = GWB` [S1].
   7. Cap `GWB` and `BB` at $10,000,000 [S1].
8. **Depletion test.** If `AV ≤ 0` and the GLWB is in force, set `depleted_flag`. If the
   GAWA% has not yet been fixed, fix it at the percentage for the attained age when
   contract value hits zero [S1]. All other endorsements terminate without value and **no
   death benefit is payable on subsequent death** [S1].
9. **Post-depletion routine.** With `forlife_flag` true, pay `GAWA` at each Contract
   Anniversary for the life of the Designated Life [S1]. Without it, pay `GAWA` until the
   earlier of death and `GWB` depletion, truncating the final payment to the remaining
   `GWB` and decrementing `GWB` by each payment [S1].
10. **EOM decrements** — death first, then surrender **[std]**:
    `l(t) = l(t−1) · (1 − q^d(t)) · (1 − q^w(t))`.

**Step-order caveat.** The research file does not settle whether the year-end bonus is
credited before or after the anniversary step-up test [S1]. The **[std]** order above
(bonus, then step-up) yields `GWB_new = max(GWB_old + bonus, AV)`; the reverse yields
`max(GWB_old, AV) + bonus`, which is strictly more generous. The [std] choice follows the
one design in the set that states the interaction explicitly, where "an Enhancement and an
Account Value Step-up cannot both occur in the same year; if the step-up is ≥ the
Enhancement, the Enhancement is not applied" [S8]. Treat the alternative as a
first-order sensitivity, not a rounding issue.

### Guaranteed minimum death benefit

    DB(t)          = max( AV(t) , NP(t) , RB(t) )                          [S1]
    GuaranteeClaim = max( 0 , GMDB_guarantee(t) − AV(t) )
                   = max( 0 , max(NP(t), RB(t)) − AV(t) )

`DB(t)` is the **gross** claim outflow; `GuaranteeClaim` is the **net general-account
strain**. Both are needed and they are not interchangeable — projecting only the guarantee
excess as the claim understates gross benefit outgo and breaks reconciliation with
statutory exhibits, while projecting both double counts. The full argument is set out once
in `products/variable_ul/technical-notes.md`; its logic carries over, but that file states
it for a life contract, where the gross outflow is the **death benefit less policy debt** and
the net strain is the **net amount at risk**. A VA has neither policy debt nor a NAAR: the gross
outflow here is `DB(t)` and the net strain is `max(0, guarantee − AV)`, as set out above.

The three GMDB guarantee forms and their recursions **[std] naming; mechanics cited**:

| Form | Recursion | Withdrawal treatment | Source |
|---|---|---|---|
| Return of premium (proportional) | `G(t) = G(t−1) + P(1−τ)` | `G ← G · (1 − W/AV_pre)` — proportional, **not** dollar-for-dollar | [S1] [S2]; same design at [S4] [S7] |
| Annual ratchet / highest anniversary value | `G(t) = max(G(t−1), AV(t))` at each anniversary (quarterly anniversaries in the HQAV variant), growth ceasing at the age cutoff | proportional | [S1] (HQAV, quarterly, to age 81); [S4] (Maximum Anniversary Value); [S7] (to age 85) |
| Fixed roll-up (representative) | `RB(t) = RB(t−1) · (1 + ρ)` at each anniversary until the cutoff | d-f-d up to `ρ · RB(prior anniv.)`, pro rata above, applied at year end | [S1] [S3] |
| Combination | `max(roll-up component, ratchet component)`, each as above | as above | [S1] |

### Cash flow outputs (per contract, month t, before survivorship weighting)

| Cash flow | Formula | Sign |
|---|---|---|
| Premium income | `P(t)` | + |
| Charge income — M&E and admin | `Σ_i SA_i^{pre-charge}(t) · (m+α)/12` | + |
| Charge income — rider fees | `(phi_G/4)·GWB + (phi_D/4)·RB` at quarter ends | + |
| Charge income — contract fee | `f_c` at anniversaries when `AV < 50,000` | + |
| Charge income — CDSC | `c(t)` | + |
| Death benefit (gross) | `DB(t)` | − |
| Death benefit (net GA strain, memo) | `max(0, max(NP, RB) − AV)` | memo |
| Surrender proceeds | `AV(t) − CDSC on surrender` | − |
| Withdrawal proceeds | `W(t) − c(t)` | − |
| Post-depletion GLWB payments | `GAWA` at each anniversary while in the depleted state | − |
| Maintenance expense | `[100 · 1.025^(vy−2015)]/12 + (0.0007/12)·AV(t)` [R1] | − |

Aggregate expected flows weight by `l(t−1)` (charges, premiums, expenses),
`l(t−1)·q^d(t)` (death) and `l(t−1)·(1 − q^d(t))·q^w(t)` (surrender) **[std]**.

---

## Stochastic requirement — the scenario interface

**Guarantee cost cannot be valued deterministically.** VM-21 makes this structural: the
Alternative Methodology is available only for a group of variable deferred annuity contracts
with either no guaranteed benefits or **only GMDBs** — never for a GLWB block [R1]. The base
deterministic run specified in the worked example below is a **mechanics demonstration only**;
it verifies the recursion, not the value of the guarantees.

**Real-world scenarios — for liability cash flow projection.** The interface is a set of
per-scenario, per-subaccount, per-month gross returns `r_i(t, ω)`. VM-21 requires each
variable subaccount to be mapped to an appropriately crafted **proxy fund**, normally a
linear combination of recognized market indices, sub-indices or funds reflecting
efficient-frontier characteristics [R1]. Projections of accumulated deficiency **ignore
federal income tax** in both cash flows and discount rates and must reflect company expenses
including overhead and investment expense, fund expenses, contractual fees and charges,
revenue-sharing income net of expenses, and reinsurance and hedging cash flows; cash flows
from any fixed account options, and any market value adjustment on projected withdrawals or
surrenders, must also be included [R1].

**Risk-neutral scenarios — for hedging and fair value.** A separate, market-consistent set
is required for hedge valuation under a Clearly Defined Hedging Strategy (VM-21 §9)
[REG-R35] and for the fair value of the GLWB/GMDB as **market risk benefits** under LDTI
[REG-R34 — source not fetched (fasb.org 403); summary-based](#uslib-reg-r34) **[unverified]** [REG-R71].
The two sets are not interchangeable; the model exposes the scenario basis as an input,
never as a hard-coded assumption.

**Reserve layer, cited not reproduced.** CTE70 for the reserve, CTE(98) for capital, on the
same projection [R1] [R3] [REG-R35]; see *Valuation and reserve pointers*.

**Prescribed-assumption anchor.** VM-21 §6.C's Guarantee Actuarial Present Value is the
regulator's own moneyness construction and the most useful public calibration anchor
available: assume immediate or continued exercise if the benefit is exercisable, otherwise
exercise at the earliest possible time; once a GMWB is exercised, withdraw **100%** of the
guaranteed maximum annual amount each subsequent year; account value growth **0% net of all
fees**; any market index held constant; mortality on the 2012 IAM Basic Table improved to
December 31, 2017 with Scale G2 and no further improvement; discounting at the **10-year
Treasury bond rate on the valuation date** [R1].

---

## Policyholder behavior modeling

All dynamic forms below are **[std]** compositions of cited components.

### Dynamic lapse on moneyness — the single most important behavioral assumption

Define the **in-the-moneyness ratio** as benefit base ÷ account value:

    M_G(t) = GWB(t) / AV(t)                    (living benefit)
    M_D(t) = max(NP(t), RB(t)) / AV(t)         (death benefit — the guarantee actually
                                                floored under `DB`, not `RB` alone)

Apply the only closed-form dynamic lapse formula the Valuation Manual publishes for VAs —
the VM-21 §7.B.1 Alternative Methodology multiplier, stated there with `GV/AV` where `GV`
is the GMDB [R1]:

    λ(M) = min[ U , max( L , 1 − Mult · (M − D) ) ],
           with U = 1.00, L = 0.50, Mult = 1.25, D = 1.10                  [R1]

    q^w_annual(t) = min[ 1 , q^w_base(y) · λ*(t) · κ(t) ]                  [std composition]

    where λ*(t) = min( λ(M_G(t)) , λ(M_D(t)) )   — the contract carries both a VAGLB and a
        GMDB, and VM-21 §6.C.6 directs that such contracts use the **lower** of the two
        ITM-based rates [R1];
    and   κ(t) = 0.60 in any contract year with a projected withdrawal, else 1.00 [R1];
    and   q^w_annual(t) = 0 whenever AV(t) = 0 [R1].

`q^w_base(y)` is the VM-21 Table 6.3 "under 50% ITM" column **[std]**: 4.0% p.a. during the
surrender-charge period (contract years 1–7 here [S2]), 25.0% in the first year after it
(year 8), 15.0% thereafter [R1]. Monthly conversion `1 − (1 − q^w_annual)^{1/12}` **[std]**.

Caution: the multiplier and the table are two *different* cited constructions of the same
effect. The multiplier floors suppression at 50%, whereas Table 6.3's own ITM grading runs
from 25.0% to 4.0% between the "<50%" and ">200%" rows in the first year after the
surrender charge period — an 84% suppression [R1]. Compose them as here, or replace the
multiplier with a direct table lookup; do not apply both gradings at once. The economic
anchor for the size of the effect is the FIA experience split: in the year the surrender
charge expires, surrender was roughly **10% with a GLWB rider versus 33% without**
[REG-R62 — from press coverage of the 2019–20 study](#uslib-reg-r62) **[unverified]**.

### GLWB utilization

The **activation-timing** machinery — an RMD-clustered activation hazard — is documented in
`products/fixed_indexed_annuity/technical-notes.md` and reused here. The **cohort**
construction below is VM-21's [R1], not that file's: it carries no cohort machinery.
Parameterized here by:

- **First-withdrawal age.** Base run **[std]**: age 70, on the finding that activation
  clusters at the RMD age [REG-R64](#uslib-reg-r64) **[unverified]** [REG-R57] [REG-R58]. The prescribed
  alternative is VM-21's Withdrawal Delay Cohort Method, which splits the contract into
  cohorts weighted by differences in a revised GAPV across candidate initial withdrawal
  ages, discarding cohorts below the attained age and rescaling [R1].
- **Never-withdraw cohort.** VM-21 prescribes 0.20 non-qualified and 0.05 tax-qualified for
  GMWB contracts [R1]; the Academy cautions that a material never-utilize cohort may
  understate reserves and suggests reassigning it to very-late cohorts [R5] [REG-R67].
- **Withdrawal intensity.** Base run **[std]**: 100% of GAWA once activated, matching the
  GAPV construction [R1]; the prescribed partial-withdrawal assumption is **90%** of the
  guaranteed annual amount for lifetime GMWBs and **70%** for non-lifetime GMWBs [R1].
- **Bonus interaction.** *Any* withdrawal in a Contract Year kills that year's bonus [S1],
  so utilization timing and benefit-base growth are coupled; a utilization model that
  ignores the forfeiture will systematically mis-time activation.

### Other behavior

- **Excess withdrawals** are not modeled in the base run **[std]**; the algebra is
  implemented and exercised by a switch, since the Academy notes GLB utilization is
  inefficient "at both ends of the spectrum" — taking less than the maximum *and* taking
  excess withdrawals [R5].
- **Charge-increase opt-out.** At each fifth Contract Anniversary the base run assumes the
  insurer does not increase the charge and the owner does not opt out **[std]**; opting out
  forfeits bonus, step-up and GWB Adjustment and blocks future premium [S1], so a rational
  opt-out model is a joint decision, not an independent lapse-style rate.
- **Annuitization.** 0% at all projection intervals for contracts without a GMIB, per the
  prescribed assumption [R1]; the representative contract has no GMIB.

---

## Worked example — one month, two subaccounts, charge stack, GMDB claim test

Anchor cell: male, issue age 60, single Designated Life, non-qualified; single premium
$100,000 at issue with premium tax 0.00% **[std]**; allocation 60/40 **[std]**; the
single-life Core GLWB (`phi_G` = 1.25%, `b` = 6.00%, annual CV step-up, `s` = 105%) [S3] and
Roll-up GMDB (`phi_D` = 0.90%, `ρ` = 6.00%) [S3]; `m + α` = 1.30% [S2]; `e_1` = 0.95%, `e_2` = 0.65%
**[std]**. No withdrawals to date.

Carried state at the beginning of month 27 (contract year 3; month 27 is the 9th Contract
Quarterly Anniversary). The guarantee bases follow from the anniversary events:
`GWB` = 100,000 → +6,000 bonus at anniversary 1 = 106,000 (contract value 104,000 **[std]
illustrative**, below GWB, so no step-up) → +6,000 bonus at anniversary 2 = 112,000, then
stepped up to the anniversary contract value of **112,500** **[std illustrative]**, which
sets `BB` = 112,500 and restarts the Bonus Period [S1]. `RB` = 100,000 × 1.06² = **112,360**
[S1] [S3]. `NP` = `RP` = 100,000. Scenario month: `r_1` = +1.20%, `r_2` = −0.30% **[std]**.

| Step | Item | SA₁ (equity) | SA₂ (bond) | Total AV |
|---|---|---|---|---|
| 1 | BOM balances | 66,000.00 | 44,000.00 | 110,000.00 |
| 2–3 | No premium, no withdrawal | — | — | 110,000.00 |
| 4 | Growth factors: SA₁ 1.0120 × (1 − 0.0095/12) × (1 − 0.0130/12) = 1.0101034; SA₂ 0.9970 × (1 − 0.0065/12) × (1 − 0.0130/12) = 0.9953805 | 66,666.82 | 43,796.74 | 110,463.56 |
| 5 | Rider fees at the quarterly anniversary: GLWB (0.0125/4) × GWB 112,500.00 = 351.56; GMDB (0.0090/4) × RB 112,360.00 = 252.81; total 604.37 cancelled pro rata (w₁ = 0.603519, w₂ = 0.396481) | −364.75 | −239.62 | −604.37 |
| 6 | Annual contract fee: not an anniversary month; and AV ≥ $50,000 so it would be waived [S2] | — | — | 0.00 |
| — | **EOM balances** | **66,302.07** | **43,557.12** | **109,859.19** |
| — | Memo: M&E + admin collected inside unit value = (66,000 × 1.0111988 + 44,000 × 0.9964600) × 0.0130/12 = 72.30 + 47.50 | — | — | 119.80 |
| — | Memo: fund expense collected by the funds (not insurer revenue) = 52.88 + 23.76 | — | — | 76.64 |
| — | Memo: **insurer charge income this month** = 604.37 + 119.80 | — | — | **724.17** |
| — | **GMDB test:** DB = max(AV 109,859.19, NP 100,000.00, RB 112,360.00) = **112,360.00**; guarantee claim = 112,360.00 − 109,859.19 = **2,500.81**; gross claim outflow = 112,360.00 | — | — | — |
| — | Memo: in-the-moneyness M_G = 112,500.00 / 109,859.19 = 1.0240, M_D = 1.0228; λ = min[1, max(0.5, 1 − 1.25(1.0240 − 1.10))] = 1.000 [R1] → no lapse suppression; base annual surrender 4.0% (in the CDSC period) [R1] → monthly 0.3396% **[std]** conversion | — | — | — |
| — | Memo: CDSC if surrendered now — completed years since premium receipt = 2 → 6.5% band [S2]; earnings = 9,859.19, so the charge-free amount is 10% × RP = 10,000.00 [S1] | — | — | — |
| — | Memo: GAWA% is not yet fixed; a first withdrawal now at attained age 62 would fix `g` = 4.00% (band 60–64, Core) [S3] and set GAWA = 4.00% × 112,500.00 = 4,500.00 | — | — | — |

Trace check on step 5: 110,463.56 − 604.37 = 109,859.19 ✓. Note that the account fell
$140.81 over the month while the guarantee bases did not move at all — the mechanical
source of moneyness drift, and the reason the rider fee income rises as the account
declines.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**. Reserve and capital layers consume
them and are cited, not reproduced:

- **VM-21** — the statutory standard and, in its scope, **CARVM itself**: aggregate reserve
  = Stochastic Reserve (CTE70 of scenario reserves) + additional standard projection amount
  + any Alternative Methodology reserve, determined both pre- and post-reinsurance-ceded
  [R1] [REG-R35]. Sections 9–12 carry hedging under a Clearly Defined Hedging Strategy,
  contract holder behavior, prudent-estimate mortality and contract-level allocation
  [REG-R35]. **AG 43 is not superseded** — through reference in AG 43 those requirements
  also reach contracts issued before January 1, 2017, and the populations may be aggregated
  [R1] [REG-R38].
- **AP&P Appendix A item A-250, and AG 33 — the formulaic layer, cited for what it does *not*
  contain.** A-250 (variable annuities) has been read in full and carries **no reserve method**: a
  definition, a per-account asset-coverage floor and a delegation of the reserve to **A-820**,
  whose ¶15 is CARVM [REG-R156] [REG-R153]. AG 33, also read in full, reaches "all annuity
  contracts subject to CARVM" carrying elective benefits but is displaced here by the
  product-specific instrument under its own precedence clause — a clause that **names no
  guideline**, so the AG 43 pairing is **[std, derived]** [REG-R151]. Neither item changes a
  number in this model; both are cited so that the formulaic layer under VM-21 is stated
  rather than assumed.
- **C-3 Phase II RBC** — the same projection at **CTE(98)** per LR027, with TAR =
  pre-phase-in VM-21 reserve + C-3 amount, the C-3 amount then grossed up by
  `1 / (1 − enacted maximum federal corporate income tax rate)` [R3]; VM-21 §§4.A–4.E and the
  RBC requirements are identical apart from the elective federal income tax treatment
  [REG-R35], so one projection serves both. The older C-3 Phase II instructions package still
  prints the **pre-reform CTE 90 TAR** and a 35% tax rate [REG-R47] — structure only; the
  current level is CTE(98) [R3] [R4].
- **VM-22 / VM-V §1** — where the **post-depletion GLWB payment stream** lands: fixed income
  streams from guaranteed living benefits after account exhaustion are named in VM-22's
  Reserving Categories and VM-V §1's scope [REG-R36] [REG-R37]. VM-22 does not cover the
  variable contract itself.
- **Tax reserve** — IRC §807: the greater of net surrender value and 92.81% of the
  NAIC-prescribed method (CARVM, i.e. VM-21), capped at statutory [REG-R16]; the LB&I
  examination directive on AG 43/VM-21 tax reserves is [unverified] (irs.gov 404) [REG-R72].
- **U.S. GAAP** — the GLWB and GMDB are the paradigm **market risk benefits** at fair value
  through earnings under LDTI [REG-R34 — ASU 2018-12 not fetched
  (fasb.org 403); summary-based](#uslib-reg-r34) **[unverified]**, with ASOP No. 10 as the professional counterpart, which
  *was* retrieved and supplies the MRB definition and classification test [REG-R71].
- **Standards for the modeling work** — ASOP Nos. 7 [REG-R27], 22 [REG-R29], 56 [REG-R32],
  2 (non-guaranteed elements, expressly covering variable deferred annuities, so governing
  the rider-charge reset) [REG-R26] and 54 [REG-R70]. **There is no ASOP for VM-21**: ASOP
  No. 52 is scoped to VM-20 life products, so any claim that it governs VM-21 is
  [unverified] and, on the retrieved ASB text, wrong [R11] [R12] [REG-R31]. The nearest
  guidance is the Academy's non-binding VM-21 practice note supplement, whose eight sections
  (Transition, Standard Projection, Asset Modeling & Discount Rates, Scenarios, Hedging, C-3
  Phase 2 RBC, Disclosures, Miscellaneous) map onto the decisions this model must make
  [R4] [REG-R66].

---

## Key sensitivities and model risks

**Dominant assumptions, in order of impact on guarantee cost.**

1. **Dynamic lapse on moneyness** — the single most important behavioral assumption, since
   it determines how many deeply in-the-money contracts persist to become claims. The
   multiplier bounds `[0.5, 1.0]` and Table 6.3's implied 84% suppression [R1] span the
   plausible range; test both.
2. **GLWB utilization — timing first, intensity second.** Activation age drives the GAWA%
   locked in [S3], the number of bonus years earned [S1] and the discount period. The
   never-withdraw cohort weight (0.20 non-qualified [R1]) is a direct multiplier on
   guarantee cost, and the Academy's warning that it may understate reserves [R5] is a live
   model risk, not boilerplate.
3. **Equity return distribution, not just its mean.** Step-up plus bonus makes the benefit
   base convex: markets up ratchet the guarantee permanently and restart the 10-year Bonus
   Period [S1]; markets down leave it intact and raise the fee base. Volatility is worth
   more than drift here.
4. **The bonus/step-up ordering [std]** — it moves the benefit base by a full year's bonus
   in every ratcheting year.
5. **Rider fee reset.** A five-yearly discretionary +0.25% step with a forfeiting opt-out
   [S1] behaves nothing like a quarterly VIX²-driven rate inside a [0.60%, 2.50%] corridor
   [S4].
6. **Post-depletion longevity.** Once the account is exhausted the liability is a pure
   life-contingent annuity at GAWA [S1]; the 2012 IAM Basic/Scale G2 basis and its A/E
   deviation [REG-R59] [REG-R61] become the whole story.

**Known modeling pitfalls.**

- **Gross vs net death claim.** Project `DB(t)` as the outflow and derive
  `max(0, guarantee − AV)` as the general-account strain — never the reverse, never both
  (see `products/variable_ul/technical-notes.md`).
- **The fee stops at AV = 0** [S4]. Accruing rider income after depletion systematically
  flatters the CTE70 tail.
- **Withdrawals are measured gross of charges** for every guarantee calculation [S1]; using
  net proceeds understates the benefit-base reduction.
- **Excess-withdrawal ordering.** The non-excess portion reduces the base dollar-for-dollar
  **first**, and the proportional factor for the excess is computed against the contract
  value *after* that reduction [S1]. Reversing the order changes both GWB and GAWA.
- **Any withdrawal kills the year's bonus** — including automatic withdrawals and RMDs [S1];
  pro-rating the bonus for partial-year withdrawals is wrong.
- **The Bonus Period restarts on a Bonus-Base-increasing step-up** up to the anniversary
  following age 80 [S1]. A hard-coded 10-year window from issue materially understates the
  guarantee in rising markets.
- **GMDB withdrawal adjustments are applied at Contract Year end**, not at the withdrawal
  [S1]; applying them immediately changes the base the roll-up compounds on.
- **Growth cutoffs are age-based, not duration-based** — roll-up and ratchet growth stop at
  the anniversary preceding the oldest Covered Life's 81st birthday [S1], so an issue-age-60
  cell gets 20 roll-up credits and an issue-age-75 cell gets 5.
- **Charge-base confusion.** M&E and admin are on **account value**, the rider fees on
  **benefit bases**, the contract fee **per contract**, the CDSC on **Remaining Premium**.
  Four bases in one stack; putting the rider fee on account value is the most common and
  most consequential error.
- **Fixed account and MVA are absent by design** — the Roll-up GMDB election removes Fixed
  Account Options [S1]. If a variant re-enables them, note that **no closed-form MVA factor
  was found in any of the four prospectuses read**: the chassis discloses a rate-differential
  rule with a 0.25% dead band and a Fixed Account Minimum Value floor [S1], so any algebraic
  MVA formula in a model would be **[unverified]** [S1] — **and that flag stays**, because the
  contract formula itself was never disclosed in closed form. What has changed is that the
  absence is now *explained* rather than merely recorded: **A-255**, the AP&P Appendix A item for
  modified guaranteed annuities, requires the separate account liability to be at least the surrender
  value produced by **the contract's own market-value-adjustment formula** and **prints neither
  a formula nor a parameter for one** [REG-R157]. No MVA formula is prescribed in the appendix
  at all, so a model's MVA algebra can only ever come from the contract. A-255 ¶1's four-element
  definition — deferred annuity, individual or group; assets in a separate account; values
  guaranteed if held for specified periods; nonforfeiture values on an MVA formula if held for
  shorter periods, with the assets in a separate account "during the period or periods when the
  contract holder can surrender the contract" — is also the test **VM-21 §2.A.2** uses to
  exclude contracts falling under VM-A item A-255, so such a variant faces a **scope** question
  before it faces a formula question; **that exclusion is VM-21's text, not A-255's**
  [REG-R157] [REG-R35].
- **Rate-sheet vintage.** Every current parameter above is dated 2026-04-27 [S3]; historical
  tables show bonus percentages moving 5/6/7% → 4/5/6% → 5/6/7% and the GWB Adjustment
  200% → 105% within six years [S1]. An in-force model must carry the vintage.
- **Discretization drift.** Monthly unit-value compounding of a daily charge [S2], annual
  crediting of roll-up and bonus [S1] and quarterly fee assessment [S1] are three different
  clocks; changing any one changes the answer. Document all three.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_annuity-r1
[R11]: #uslib-variable_annuity-r11
[R12]: #uslib-variable_annuity-r12
[R13]: #uslib-variable_annuity-r13
[R3]: #uslib-variable_annuity-r3
[R4]: #uslib-variable_annuity-r4
[R5]: #uslib-variable_annuity-r5
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R156]: #uslib-reg-r156
[REG-R157]: #uslib-reg-r157
[REG-R16]: #uslib-reg-r16
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[REG-R35]: #uslib-reg-r35
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R38]: #uslib-reg-r38
[REG-R47]: #uslib-reg-r47
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R59]: #uslib-reg-r59
[REG-R61]: #uslib-reg-r61
[REG-R64]: #uslib-reg-r64
[REG-R66]: #uslib-reg-r66
[REG-R67]: #uslib-reg-r67
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[REG-R72]: #uslib-reg-r72
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
