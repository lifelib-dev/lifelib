# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

Scope note: these notes standardize a liability cash flow projection model for the
representative GUL product defined in `product-spec.md` (same directory). They use the
same representative parameter values as the specification. Tags: [S#]/[R#] cite
`_research/guaranteed-ul.md`; [REG-R#] cites the cross-product reference library
`references/regulatory-and-actuarial-references.md` (research provenance:
`_research/regulatory-actuarial.md`, same R-numbering); **[std]** marks standardizations introduced
for the reference implementation; [unverified] flags facts the research file could not
verify from a retrieved document.

---

## Model scope and conventions

- **Product**: flexible-premium UL, level death benefit only, single shadow-account
  secondary guarantee (AG 38 8E Policy Design #1 [R1]; VM-01 shadow-account
  definition [R2]). The cumulative-premium-test variation is handled by a documented
  swap (see "Cumulative-premium variation").
- **Base chassis**: the monthiversary processing order and the NAAR discount
  convention (DB discounted one month at the guaranteed rate, floored at zero)
  follow the universal-life reference notes
  (`products/universal_life/technical-notes.md`); the shadow account runs the
  same recursion with its own parameter set. Documented deviation **[std]**: these
  notes measure the account value for the NAAR after the expense charges but before
  COI (the UL base measures AV before the entire monthly deduction) — immaterial at
  the modeled charge levels, but kept explicit for reconciliation.
- **Projection frequency**: monthly, on policy monthiversaries, from issue (or
  in-force date) to attained age 121, at which point charges and premiums cease and
  coverage continues [S7]. Maximum projection length: (121 − issue age) × 12 months.
- **Timing** **[std]**: monthiversary (BOM) processing — premium receipt, expense
  charges, COI deduction in that order at the start of the policy month; interest
  credited over the month; decrements (death, lapse/surrender, ROP exercise) at end
  of month (EOM) after interest. Deaths are processed before lapses at EOM.
- **Age basis**: age nearest birthday (ANB) **[std]** — chosen because the sourced
  products underwrite on ANB [S2]], [[S4]], [[S6] and the 2017 CSO / 2015 VBT are published
  in ANB variants [REG-R17]], [[REG-R18]. Attained age advances on policy anniversaries.
- **Model points**: single-policy model points; results are expected (probability-
  weighted) cash flows per policy in force at projection start. No stochastic
  decrement simulation in the base model **[std]**.
- **Rate conversions** **[std]**: annual effective interest i → monthly factor
  (1+i)^(1/12). Contractual COI: monthly rate per $1,000 = annual q per $1,000 / 12
  (simple-twelfth; see "Pitfalls"). Experience decrements: monthly rate
  = 1 − (1 − annual rate)^(1/12).
- **Currency/rounding**: USD; internal calculations unrounded, cash flows reported to
  the cent **[std]**.

## Model point attributes

| Attribute | Type | Example (used throughout these notes) |
|---|---|---|
| `policy_id` | str | "GUL-000001" |
| `issue_age` | int (ANB) | 60 |
| `sex` | enum {M, F} | M |
| `risk_class` | enum (4 NT + 2 T classes [S4]) | NT Standard |
| `face_amount` | float (≥ 100,000 [S4]], [[S6]) | 500,000 |
| `guarantee_age` | int in [90, 121] [S1]], [[S2]], [[S9] | 121 (lifetime) |
| `premium_pattern` | enum {level, single_pay, ten_pay} **[std]** | level |
| `annual_premium` | float — solved no-lapse premium P* for level pattern | 10,800.00 **[std]** (illustrative solve output) |
| `premium_mode` | enum {A, S, Q, M-EFT} [S2] | A |
| `duration_months` | int — elapsed policy months at projection start | 300 |
| `av_init` | float — base account value at projection start | 2,400.00 |
| `sg_init` | float — shadow account value at projection start | 118,000.00 |
| `loan_init` | float | 0.00 |
| `rop_elected` | bool (built-in endorsement [S1]) | True |

Premium pattern is a first-class model point attribute because funding pattern drives
both MEC status [R5] and observed lapse behavior (higher lapses for level-pay, lower
for single-pay [R8]; premium persistency study basis [REG-R21]).

## State variables

| Variable | Meaning | Initial value |
|---|---|---|
| `t` | policy month index (1, 2, …) | `duration_months` + 1 |
| `AV_t` | base account value, EOM, floored at 0 | `av_init` |
| `SG_t` | shadow account value, EOM, NOT floored (negative = catch-up shortfall) | `sg_init` |
| `L_t` | loan balance including accrued interest | `loan_init` |
| `DB_t` | death benefit = max(F, κ(x_t)·AV_t) [S2, S4; R4 corridor](#uslib-guaranteed_ul-s2) | — |
| `l_t` | in-force probability (survivorship from all decrements) | 1.0 |
| `g_t` | grace-period counter, months (0 = not in grace) [S7] | 0 |
| `D_t` | monthly deduction forgone because AV = 0 under active guarantee | 0 |
| `CumPrem_t` | cumulative premiums paid (drives ROP refund [S1] and MEC testing [R5]) | per model point |
| `SC_t` | surrender charge = 18/1000 · F · max(0, (180 − t)/180) **[std]** | — |
| `C_t` | catch-up premium required to restore guarantee = max(0, −(SG_t − L_t))/(1 − π^g) **[std]** | 0 |

## Assumption inputs

The model distinguishes three assumption classes. Class (a) is contractual and fixed;
class (b) is a snapshot of insurer-declared scales; class (c) is behavioral/experience
and belongs to the assumption-governance layer (see [REG-R25] for governance
patterns; ASOP 2 governs insurer NGE determination itself [REG-R26]).

### (a) Contractual / guaranteed elements (from the specification)

| Element | Value | Basis |
|---|---|---|
| Base premium load π | 25% | [S3], [S7] |
| Base per-policy charge | $5.50/month to age 121 | [S3], [S7] |
| Base per-unit charge | $0.20 per $1,000 initial face /month | **[std]** (spec note) |
| Guaranteed max COI | 2017 CSO sex/smoker-distinct ANB, monthly = annual/12 | **[std]** structure; [R3] (stated maxima required); [REG-R17] |
| Guaranteed credited rate | 2.0% annual effective | [S3], [S5], [S7] |
| Shadow premium load π^g | 8% | **[std]** |
| Shadow credited rate i^g | 5.5% annual effective (guaranteed) | **[std]**; AG 38 8E cap context [R1] |
| Shadow COI | 55% of 2017 CSO maximum | **[std]** |
| Shadow per-unit charge | $0.05 per $1,000 initial face /month; no per-policy charge | **[std]** |
| Loan rates | 5.0% charged in arrears / 3.0% credited on loaned AV, guaranteed | [S4] |
| Surrender charge | 15-year linear schedule, $18/$1,000 initial level | **[std]** (spec note) |
| ROP endorsement | 50% of CumPrem at anniversary 20, 100% at 25; cap 40% of face; 60-day windows | [S1]; [S3], [S4] (windows) |
| Grace period | 61 days | [S7] |

### (b) Current non-guaranteed scales (insurer-declared snapshot)

| Element | Value | Basis |
|---|---|---|
| Current COI scale | 65% of guaranteed maximum, all durations | **[std]** (spec note; scales not published — research Gaps) |
| Current credited rate i^c | 3.5% annual effective | **[std]** (spec note) |
| Current loan credited rate | 3.0% (= guaranteed [S4]) | [S4] |

The base model holds current scales level for the projection **[std]**; re-rating
logic (current scales moving within guaranteed bounds) is out of scope but the
guaranteed bounds above define the admissible envelope [R3; REG-R26](#uslib-guaranteed_ul-r3).

### (c) Behavioral / experience assumptions

| Assumption | Recommended public basis | Reference model values |
|---|---|---|
| Best-estimate mortality | 2015 VBT primary tables (sex/smoker-distinct, ANB) [REG-R18], with company A/E positioning informed by the ILEC 2012–2019 study [REG-R19] | 100% of 2015 VBT **[std]** |
| Mortality improvement | — | 1.0%/yr to attained age 85, grading linearly to 0% at 95, applied for max 20 years **[std]** |
| Base lapse (annual) | SOA/LIMRA UL lapse studies: 2009–2013 persistency update [REG-R20]; 2015–2021 UL lapse/surrender study ([R7]; [REG-R21]) | Duration 1: 4.0%; 2: 3.0%; 3: 2.5%; 4–5: 2.0%; 6–10: 1.5%; 11–20: 1.0%; 21+: 0.75% **[std]** |
| Lifetime-guarantee lapse multiplier | Lifetime-SG lapse rates are 45% lower than non-lifetime-SG rates (count and amount bases, 2015–2021) [R7] | 0.55 × base at all durations when `guarantee_age` = 121 **[std]** (level derived from the [R7] finding; duration shape [std]) |
| Dynamic lapse | 63% of surveyed ULSG writers use dynamic lapse; lapse and tail investment returns rated the most critical ULSG assumptions [R8] | formulas below, **[std]** |
| Premium persistency | 2015–2021 UL premium persistency study [REG-R21]; premium-pattern-dependent lapse [R8] | level-pay: scheduled premium paid with 98% annual probability, missed premiums not made up **[std]**; single-pay/ten-pay: as scheduled |
| ROP exercise | no public study in research file | 5% of eligible in-force exercise in the year-20 window; 10% in the year-25 window **[std]** |
| Loan/withdrawal utilization | — | 0 in the base model point **[std]** (sensitivity only) |
| Maintenance expense | — | $75/policy/year, inflated 2.5%/yr **[std]** |
| Acquisition expense | — | year 1: $300/policy + 90% of first-year premium (commissions + issue) **[std]** |
| Claim expense | — | $300 per death **[std]** |

The detailed duration-by-duration ULSG lapse tables sit in the paid SOA/LIMRA
Standard Data Package [R7]; all lapse levels above are therefore **[std]** shapes
anchored to the public highlights findings.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `F` | face amount |
| `P_t` | premium received at BOM of month t (0 in non-premium months) |
| `π`, `π^g` | base (0.25) and shadow (0.08) premium loads |
| `e_pol` | per-policy charge, $5.50/month |
| `e_u`, `e_u^g` | per-unit charges: 0.20 and 0.05 per $1,000 initial face /month |
| `m_t^max` | guaranteed max monthly COI rate per $1,000 (2017 CSO annual/12) |
| `m_t = 0.65·m_t^max` | current monthly COI rate per $1,000 |
| `m_t^g = 0.55·m_t^max` | shadow monthly COI rate per $1,000 |
| `j_c, j_g, j^g` | monthly factors − 1 for current 3.5%, guaranteed 2.0%, shadow 5.5%: 0.0028709, 0.0016516, 0.0044717 |
| `NAAR_t` | base net amount at risk |
| `AV_t', AV_t''` | base AV after premium+expenses; after COI |
| `SG_t', SG_t''` | shadow analogues |
| `W_t` | withdrawal amount (plus $25 fee) |
| `q_t^d, w_t` | monthly best-estimate death and lapse rates (converted from annual) |
| `l_t` | in-force probability at BOM of month t |
| `κ(x)` | GPT corridor factor at attained age x [R4; REG-R13](#uslib-guaranteed_ul-r4) |

### Monthly processing order **[std]**

1. **Status check.** If `g_{t−1} > 0` (in grace) and cumulative grace ≥ 61 days
   without the required payment, the policy lapses at BOM with no value
   (`CSV ≤ 0` in grace by construction) [S7].
2. **Premium.** `CumPrem_t = CumPrem_{t−1} + P_t`. Base credit `(1 − π)·P_t`; shadow
   credit `(1 − π^g)·P_t`. (Catch-up premiums route identically **[std]**.)
3. **Expense charges.**
   `AV_t' = AV_{t−1} + (1−π)P_t − e_pol − e_u·F/1000 − W_t − 25·1{W_t>0}`
   `SG_t' = SG_{t−1} + (1−π^g)P_t − e_u^g·F/1000 − W_t`  (withdrawal reduces shadow
   dollar-for-dollar **[std]**, spec note).
4. **Death benefit and NAAR.** `DB_t = max(F, κ(x_t)·max(AV_t',0))`;
   `NAAR_t = max(DB_t/(1+j_g) − max(AV_t', 0), 0)`;
   `NAAR_t^g = max(DB_t/(1+j^g) − max(SG_t', 0), 0)` **[std]** (discount convention;
   the account inputs are floored at zero so that a deficit — AV in the
   guarantee-support regime, SG in catch-up territory — never inflates NAAR above the
   discounted DB).
5. **COI.** `COI_t = m_t · NAAR_t/1000`; `COI_t^g = m_t^g · NAAR_t^g/1000`.
   `AV_t'' = AV_t' − COI_t`; `SG_t'' = SG_t' − COI_t^g`.
6. **Insufficiency handling (the low-AV regime).** If `AV_t'' < 0`:
   - if the guarantee is active (`SG_t'' − L_{t−1} > 0`): set `D_t = −AV_t''`,
     `AV_t'' = 0`. The forgone deduction `D_t` is NOT a receivable — the insurer
     funds the negative "account" economics; coverage continues with `AV = 0` and
     `NAAR ≈ DB` [S2, S3, S9 guarantee behavior; accounting treatment **[std]**](#uslib-guaranteed_ul-s2).
   - else: enter/continue grace, `g_t = g_{t−1} + 1`; required grace payment =
     amount curing the deduction shortfall **[std]**.
7. **Interest.** Unloaned base AV grows at `j_c` (floor `j_g`); loaned AV at the
   loaned credited monthly rate (3.0% annual [S4]):
   `AV_t = AV_t''·(1+j_c)` (split loaned/unloaned when `L > 0`).
   `SG_t = SG_t''·(1+j^g)` — no floor at zero.
8. **Loan interest.** `L_t = L_{t−1}·(1 + (1.05)^{1/12} − 1)` (5% in arrears [S4],
   accrued monthly **[std]**).
9. **In-force test.** Guarantee active iff `SG_t − L_t > 0` [S4; S2, S9](#uslib-guaranteed_ul-s4). The policy
   is in force iff (base account can cover deductions, i.e., not in expired grace)
   OR the guarantee is active. Lapse occurs ONLY if all three hold: (i) base AV net
   of charges failed (step 6 else-branch), (ii) `SG_t − L_t ≤ 0`, (iii) the 61-day
   grace expires without cure [S7; S2, S9 mechanics; conjunction **[std]**](#uslib-guaranteed_ul-s7).
10. **Catch-up requirement.** `C_t = max(0, −(SG_t − L_t))/(1 − π^g)` **[std]**;
    paying `C_t` restores `SG − L` to 0⁺ and the guarantee with it [S7; R1 ex. 7](#uslib-guaranteed_ul-s7).
11. **Decrements (EOM), deaths first.** With monthly rates `q_t^d` then `w_t`
    applied to `l_t`:
    - death CF: `l_t·q_t^d·(DB_t − L_t)` + claim expense
    - surrender CF: `l_t·(1−q_t^d)·w_t·CSV_t`, `CSV_t = max(AV_t − SC_t − L_t, 0)`
    - ROP exercise (window months only): rate `w^ROP` **[std]**, benefit
      `min(ρ·CumPrem_t, 0.40·F) − L_t`, ρ ∈ {50%, 100%} [S1]; exercise is a full
      surrender [S1]], [[S3].
    - `l_{t+1} = l_t·(1−q_t^d)·(1−w_t)·(1−w_t^ROP)`
12. **Age/duration update**; at attained age 121 all charges and premiums cease,
    recursion continues with `COI = expenses = P = 0` and interest only [S7].

### Cash flow outputs (per month, expected per initial policy)

- Premium income: `l_t·φ_t·P_t` where `φ_t` = premium persistency probability
  (class (c)).
- Death claims: as step 11 (net of loan repayment from proceeds — standard UL
  treatment **[std]**; see spec, "Loans").
- Surrender/ROP benefits: as step 11.
- Expenses: acquisition (month 1), maintenance /12 monthly, claim expense.
- Loan cash flows (drawdown/repayment): 0 in base model point **[std]**.
- Internal transfers (loads, COI, expense charges, interest credits, shadow-account
  entries) are NOT external cash flows; they drive `AV`, `CSV` and the in-force test
  only. This is the gross-liability convention of the library **[std]**.

### Funding-premium solve (level no-lapse premium P*)

Objective: the smallest level annual premium such that the guarantee never fails
before the elected guarantee age:

```
g(P) = min over t in [1, (guarantee_age − issue_age)·12] of (SG_t(P) − L_t)
P*   = min { P : g(P) > 0 }
```

`SG_t(P)` is monotone non-decreasing in P (every premium enters the shadow account
at `(1 − π^g)` and accumulates at `i^g` net of charges that do not increase with P
while `DB = F`; at extreme funding levels a corridor-driven DB increase would raise
shadow COI, so cap the search domain at the guideline premium limitation [R4],
inside which the corridor does not bind for this thin-AV design), so `g` is
monotone and bisection is safe on that domain **[std]**:

1. Bracket: `P_lo = 0` (g < 0 for any nontrivial guarantee), `P_hi` = the premium
   that funds the guarantee as a single-pay net single premium on shadow parameters
   (guaranteed sufficient); double `P_hi` until `g(P_hi) > 0`.
2. Bisect on `g(P) > 0` to tolerance $0.01 of annual premium **[std]**; ~40
   iterations. A secant step on `g` accelerates convergence near the root; fall back
   to bisection when the secant iterate leaves the bracket **[std]**.
3. Full-projection evaluation of `g` per iterate (steps 1–12 with decrements off —
   the solve is contractual, not behavioral **[std]**).

Shorter guarantee ages solve the same way with the earlier stopping time; single-pay
and n-pay premiums solve identically over their premium vectors.

### Calibration **[std]**

No public document discloses shadow-account parameters (research Gaps). The [std]
shadow parametrization (π^g = 8%, i^g = 5.5%, COI^g = 55% CSO, $0.05/unit) is
calibrated so that solved level lifetime premiums fall in the range of observed
market premiums for lifetime GUL. The research file records competitive positioning
but no premium tables [S2]; the calibration target is therefore itself a
standardization, and implementations should re-calibrate against current market
quotes before using outputs comparatively. The illustrative solve output used in
these notes (P* = $10,800 for male 60 NT Standard, $500,000, lifetime) is **[std]**.

### Cumulative-premium variation (main design alternative)

To model the cumulative-premium-test design [R1 8E Design #2; S4 initial NLG; S5](#uslib-guaranteed_ul-r1):
replace `SG_t` with the pair (`CumPrem_t^net`, `ReqPrem_t`), where
`CumPrem_t^net = Σ premiums − Σ withdrawals − L_t` [S4] and `ReqPrem_t` is the
contractual required accumulated premium schedule; guarantee active iff
`CumPrem_t^net ≥ ReqPrem_t` [S4]], [[S5]. All other machinery (grace, catch-up = the
schedule shortfall, solve on the required schedule) is unchanged. Note the harsher
observed loan treatment in this family: one design voids the guarantee entirely on
any loan [S5].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]**; the empirical anchors are [R7] (lifetime-SG
lapse 45% lower), [R8] (dynamic lapse used by 63% of writers; premium-pattern
dependence; median 40% of policies assumed sustained by the guarantee after 31 years
in tail scenarios) and [REG-R20]/[REG-R21] (public study bases).

Total monthly lapse: `w_t = min(0.5, b(d) · G · Φ(pattern) · Ψ_t) /12-converted`,
where `b(d)` is the base annual table (class (c)), and:

- `G` (guarantee-duration factor): 0.55 if `guarantee_age` = 121 [R7-anchored],
  1.0 otherwise **[std]**.
- `Φ` (premium pattern): single-pay 0.6; ten-pay 0.8; level 1.0 **[std]**
  (direction per [R8]: higher lapses for level-pay, lower for single-pay).
- `Ψ_t` (funding-status dynamic factor) **[std]**:
  - guarantee active and AV > 0: 1.0
  - guarantee active and AV = 0 (pure guarantee support): 0.6 — the policy is
    deep in the money to the policyholder; empirical anchor: sustained-by-guarantee
    fractions in tail scenarios [R8]
  - guarantee terminated (`SG − L ≤ 0`) and policy surviving on AV: 2.0 (shock)
  - annual floor after the dynamic factor: 0.3% **[std]**
- ROP windows: additional exercise rates 5% (year-20 window) / 10% (year-25
  window) **[std]** applied as full surrenders at the window months; rationale: the
  100% refund dominates CSV for a thin-AV product, but exercising forfeits a
  now-cheap guarantee, so observed exercise should stay modest. No public exercise
  study was found (research file has none).
- Premium persistency: level-pay premiums paid with annual probability 98%
  **[std]**; a missed premium permanently reduces `SG` trajectory (no automatic
  catch-up); catch-up behavior is not modeled in the base run **[std]**.

Anti-selective interaction: mortality of lapsers vs. persisters is NOT adjusted in
the base model **[std]** (no selective-lapse load); this understates claims if
healthy lives disproportionately lapse or exercise ROP — flagged under model risks.

---

## Worked example **[std]** (all figures illustrative)

Model point: male 60 ANB NT Standard, F = $500,000, lifetime guarantee, level
P* = $10,800 paid annually; projection months 301–305 (policy year 26, attained age
85, anniversary premium in month 301). Illustrative COI rates at age 85: guaranteed
max monthly `m^max` = 8.615 per $1,000 **[std]**; current `m` = 5.60 (65%); shadow
`m^g` = 4.74 (55%). Monthly interest factors: base current 1.0028709; shadow
1.0044717. Opening: AV = 2,400.00; SG = 118,000.00; L = 0. Deductions column =
expenses + COI. Decrements are suppressed for clarity (contract-mechanics view).

| Mo. | Prem | Base net prem | Base deductions | Base int. | AV (EOM) | Shdw net prem | Shdw deductions | Shdw int. | SG (EOM) | Status |
|----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|---|
| 301 | 10,800.00 | 8,100.00 | 2,842.68 | 21.98 | 7,679.30 | 9,936.00 | 1,778.15 | 564.13 | 126,721.98 | in force |
| 302 | 0 | 0 | 2,858.47 | 13.84 | 4,834.67 | 0 | 1,783.90 | 558.66 | 125,496.74 | in force |
| 303 | 0 | 0 | 2,874.40 | 5.63 | 1,965.90 | 0 | 1,789.71 | 553.16 | 124,260.19 | in force |
| 304 | 0 | 0 | 2,890.47 → 1,965.90 taken; 924.57 forgone | 0.00 | **0.00** | 0 | 1,795.57 | 547.62 | 123,012.24 | in force — guarantee |
| 305 | 0 | 0 | 2,900.89 forgone (AV = 0) | 0.00 | 0.00 | 0 | 1,801.49 | 542.01 | 121,752.76 | in force — guarantee |

Reading the table: the base account exhausts in month 304 — monthly deductions
(~$2,900, dominated by COI on a ~$497K NAAR) exceed the annual net premium spread
over the year, and the residual $924.57 of month-304 deductions is forgone by the
insurer (`D_304`), not carried as a receivable. The policy does NOT enter grace:
the shadow account, charged at the lighter [std] shadow parameter set and credited
at 5.5%, stands at ~$123K, so the in-force test `SG − L > 0` holds and coverage
continues with `NAAR ≈ DB = $500,000`. From month 305 onward the insurer is funding
the full mortality cost of the guarantee — the "negative account economics" regime
that dominates late-duration GUL liability cash flows. Arithmetic: net premium =
P × (1 − load); deductions = per-policy 5.50 + per-unit 100.00 + COI m·NAAR/1000
(base; shadow analogues 0/25.00/m^g·NAAR^g/1000); NAAR = 499,176 − max(AV′, 0)
(base — the floor binds in month 305, where AV′ = −105.50 but COI is charged on the
full 499,176 NAAR), 497,774 − SG′ (shadow; SG′ > 0 throughout); interest = balance
after deductions × monthly factor − 1.
Independent recomputation may differ by cents due to rounding.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**; reserve layers consume those
cash flows and are cited, not reproduced:

- **VM-20 (PBR, post-2017 issues)**: ULSG is its own reserving category; reserve =
  NPR floor plus excesses of deterministic (DR) and stochastic (SR) reserves. The
  ULSG NPR during the SG period is the greater of a non-SG amount and
  `min(ASG/FFSG, 1)·NSP − E` with the amortized expense allowance
  (x1 = level gross premium; y2–5 = 10% of it; z1 = $2.50/$1,000) and the prescribed
  funding-ratio-driven lapse `L = R·1% + (1−R)·0.5%·r` [R2]. Note the model's
  `SG_t` IS the "actual secondary guarantee" (ASG) input, and the fully-funded
  value FFSG is a backward solve on the same shadow recursion [R2]. See also the
  Academy practice note [R9; REG-R23](#uslib-guaranteed_ul-r9) and the Valuation Manual itself [REG-R3].
  Material-SG business cannot use the life PBR exemption [R2; R9](#uslib-guaranteed_ul-r2).
- **AG 38 / A-830 (pre-PBR issues and in-force)**: the formulaic layer underneath
  AG 38 is now sourced at first hand. A-830 **¶¶29–32** — not "Section 7"; the AP&P
  print is a flat ¶¶1–32 with no Sections — makes the basic reserve the **segmented
  reserve over the secondary guarantee period** computed on specified (else minimum)
  premiums with **no unitary leg**, the ¶22 deficiency on the same substitution, and a
  floor at the greater of that sum and an **unnamed** "other appendices governing
  universal life plans" limb; several unexpired guarantees are valued **stand-alone and
  the greatest taken** [REG-R154 ¶¶29–32](#uslib-reg-r154). A-830's own basic reserves, deficiency
  comparator and maximum valuation interest rates are cross-references into **A-820
  ¶¶11–13, ¶¶19–20 and ¶¶7–10** [REG-R153]. On top of that, AG 38 supplies what A-830
  contains nothing of: funding-ratio interpolation between basic+deficiency reserves
  and the net single premium for the guarantee, prescribed lapse caps and
  surrender-charge offsets; Section 8E Method I
  defines minimum gross premiums off this very shadow recursion [R1; REG-R6;
  REG-R7](#uslib-guaranteed_ul-r1).
- **Reserve financing**: Model 787 / AG 48 Primary Security requirements are
  VM-20-based (greater of DR and NPR; greatest of DR/SR/NPR if the stochastic
  exclusion fails) [R6; REG-R11; REG-R12](#uslib-guaranteed_ul-r6).
- **Tax reserves**: greater of net surrender value and 92.81% of the NAIC-method
  reserve, capped at statutory [REG-R16].
- **Professional standards**: ASOP 52 (PBR work) [R10; REG-R31](#uslib-guaranteed_ul-r10); ASOP 7 (cash flow
  analysis) [REG-R27]; ASOP 56 (model governance — applies to this reference
  implementation itself) [REG-R32].

## Key sensitivities and model risks

**Dominant assumptions (in order):**

1. **Lapse.** First-order by a wide margin: GUL is lapse-supported. Every lapse of a
   funded guarantee releases the insurer from a deeply in-the-money claim; lifetime-SG
   experience already runs 45% below non-lifetime SG [R7], insurers rate lapse among
   the two most critical tail assumptions, and the median tail assumption keeps 40%
   of policies in force purely on the guarantee after 31 years [R8]. PV of claims is
   convex in the ultimate lapse rate near zero — sensitivity runs must include
   ultimate lapse 0% **[std]** recommendation.
2. **Mortality level and improvement at high attained ages.** With `NAAR ≈ DB` for
   decades in the guarantee-support regime, claims PV moves nearly linearly with
   85+ mortality; improvement assumptions compound [REG-R18, REG-R19 bases](#uslib-reg-r18).
3. **Premium persistency / funding pattern mix.** Single-pay vs. level-pay changes
   both the guarantee trajectory and lapse behavior [R8; REG-R21](#uslib-guaranteed_ul-r8); a 98% vs. 100%
   payment probability materially shifts guarantee failure times for exactly-funded
   level payers **[std]** observation.
4. **ROP exercise.** Exercise at the 100% window is an option against the insurer
   whose cost depends on cumulative premiums vs. reserve released; mis-set exercise
   rates distort years 20–26 cash flows [S1 design; rates [std]](#uslib-guaranteed_ul-s1).

**Known modeling pitfalls:**

- **NAAR discount convention.** `DB/(1+j_g)` vs. `DB` un-discounted changes COI by
  ~0.17% per month at 2%; be consistent between base and shadow accounts and
  against any carrier illustration being matched **[std]** convention here.
- **Monthly COI conversion.** annual/12 vs. 1−(1−q)^(1/12) differs materially at
  ages 85+ (q > 0.10); this model fixes annual/12 **[std]** — do not mix.
- **Flooring.** `AV` floors at 0 only while the guarantee is active; `SG` never
  floors (its negative part is the catch-up requirement). Flooring `SG` at 0
  destroys the catch-up computation and misprices restoration [R1 ex. 7 logic](#uslib-guaranteed_ul-r1).
- **Forgone deductions are not receivables.** `D_t` must not accrue against future
  premiums or `AV` recoveries **[std]**; treating it as a receivable understates
  the guarantee cost.
- **Order of tests.** Run the guarantee test AFTER the full monthly deduction
  attempt; testing before deductions lets a policy lapse a month early (or late)
  and shifts claim timing at exactly the durations where NAAR ≈ DB.
- **ANB/ALB mismatch.** 2017 CSO and 2015 VBT each exist in ANB and ALB variants
  [REG-R17]], [[REG-R18]; this model is ANB throughout **[std]** — a mixed basis shifts
  COI and expected claims by up to half a year of mortality.
- **Guarantee-age grid.** The solve target `SG > 0` strictly; a `≥ 0` target with
  monthly grids can leave the guarantee failing on the final monthiversary.
- **Shadow parameters are standardized.** All shadow-account parameters are [std]
  calibrations, not observed contract values (research Gaps: no specimen policy
  form retrieved; no carrier publishes shadow parameters). Conclusions that depend
  on the shadow parametrization (funding ratios, catch-up costs, VM-20 ASG/FFSG
  inputs) carry that calibration risk.
- **Out-of-model features.** 7702/7702A testing (GPT premium limits, MEC status
  [R4]], [[R5]), terminal-illness acceleration (treated as CF-neutral **[std]**),
  selective-lapse mortality adjustment, and NGE re-rating are not modeled in the
  base run; each is a documented extension point.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-guaranteed_ul-r1
[R2]: #uslib-guaranteed_ul-r2
[R3]: #uslib-guaranteed_ul-r3
[R4]: #uslib-guaranteed_ul-r4
[R5]: #uslib-guaranteed_ul-r5
[R7]: #uslib-guaranteed_ul-r7
[R8]: #uslib-guaranteed_ul-r8
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R17]: #uslib-reg-r17
[REG-R18]: #uslib-reg-r18
[REG-R19]: #uslib-reg-r19
[REG-R20]: #uslib-reg-r20
[REG-R21]: #uslib-reg-r21
[REG-R25]: #uslib-reg-r25
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R3]: #uslib-reg-r3
[REG-R32]: #uslib-reg-r32
[S1]: #uslib-guaranteed_ul-s1
[S2]: #uslib-guaranteed_ul-s2
[S3]: #uslib-guaranteed_ul-s3
[S4]: #uslib-guaranteed_ul-s4
[S5]: #uslib-guaranteed_ul-s5
[S6]: #uslib-guaranteed_ul-s6
[S7]: #uslib-guaranteed_ul-s7
[S9]: #uslib-guaranteed_ul-s9
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
