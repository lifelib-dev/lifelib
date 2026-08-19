# Technical Notes

**Status:** Draft, 2026-08-03; cross-product [REG-R#] citations extended 2026-08-06
with the AP&P Manual appendix items read at first hand. Product sources [S#]/[R#] were
accessed 2026-08-03; the [REG-R#] entries carry their own access dates per entry in
`sources.md`. Companion to `product-spec.md` in this
directory; both use identical parameter values. This is a standardized composite for
reference modeling, not any single insurer's product. [S#]/[R#] cite
`_research/variable-ul.md`; [REG-R#] cites the cross-product reference library
`references/regulatory-and-actuarial-references.md` (research provenance:
`_research/regulatory-actuarial.md`, same R-numbering); **[std]** marks standardizations introduced
for the reference implementation. Facts flagged [unverified] in the research notes
stay flagged here.

## Model scope and conventions

- **Scope.** Single-policy seriatim projection of gross liability cash flows for the
  representative VUL contract of `product-spec.md`, baseline without riders or
  no-lapse guarantee **[std]**. Reserve calculations are out of scope (see
  "Valuation and reserve pointers").
- **Base chassis.** The monthiversary processing order (premium → withdrawal/loan →
  DB and NAAR → monthly deduction → growth → EOM decrements, deaths before lapses)
  follows the universal-life reference notes
  (`products/universal_life/technical-notes.md`). One sourced deviation from that
  base chassis: the VUL prospectuses define the NAAR as death benefit − account
  value with no one-month discount [S2], so this model omits the one-month
  guaranteed-rate discount used in the fixed-UL base recursion.
- **Projection frequency.** Monthly, on policy monthiversaries; contractual daily
  accruals (M&E, fund expenses, fixed-option interest [S1]) are approximated by
  monthly factors **[std]**.
- **Timing.** Beginning-of-month (BOM) monthiversary processing: premium receipt,
  withdrawals, loan activity, and the monthly deduction occur at the monthiversary;
  investment growth accrues over the month; decrements (death, lapse/surrender) and
  claim/surrender payments occur at end of month (EOM), deaths before lapses
  **[std]**.
- **Age basis.** Age nearest birthday (ANB) **[std]**, consistent with the 2017 CSO
  ultimate ANB tables cited for guaranteed COI maxima [S2] [S4]. Attained age
  advances on policy anniversaries.
- **Model points.** One policy per model point; decrements applied as probabilities
  (in-force measure l_t), not stochastic lives **[std]**. Cash flows are
  probability-weighted per unit policy in force at issue (or at the projection start
  for in-force points).
- **Compliance mechanics.** The corridor is enforced in the DB formula [S2] [R3].
  Guideline premium limits and 7-pay/MEC testing [R3] [R4] are not enforced in the
  baseline; premiums are assumed within limits **[std]**.

## Model point attributes

| Attribute | Type | Example |
|---|---|---|
| policy_id | str | "VUL-000001" |
| issue_age (ANB) | int | 45 |
| sex | enum {M, F} | M |
| risk_class | enum | standard nonsmoker |
| face_amount F_0 | currency | 500,000 |
| db_option | enum {A, B} | A |
| s7702_test | enum {GPT, CVAT} | GPT (baseline **[std]**) |
| planned_premium (annualized) | currency | 6,000 |
| premium_mode | enum | monthly |
| premium_allocation α = (α_1, α_2, α_F) | vector, Σ = 1 | (0.60, 0.40, 0.00) |
| duration_inforce (months, for in-force points) | int | 24 |
| initial_subaccount_values | vector | (30,000, 20,000) |
| initial_fixed_value | currency | 0 |
| initial_loan_balance | currency | 0 |
| nlg_rider | bool | false (baseline **[std]**) |

The two-subaccount lineup (1 = equity, fund expense e_1 = 0.75% p.a.; 2 = bond,
e_2 = 0.55% p.a.) is a **[std]** collapse of observed menus; observed fund-expense
ranges 0.29%–1.18% [S1], 0.55%–2.88% gross [S2], 0.46%–2.54% [S3], 0.08%–1.93% [S4].

## State variables

| Variable | Meaning |
|---|---|
| t | policy month index (t = 0 at issue or projection start) |
| x_t | attained age (ANB), advancing on anniversaries |
| SA_{i,t} | value of subaccount i (separate account) |
| FA_t | fixed-option value (general account) |
| LA_t | loan-account (collateral) value (general account) [S3] |
| D_t | outstanding policy debt (principal + capitalized interest) |
| AV_t | total account value = Σ_i SA_{i,t} + FA_t + LA_t [S1] [S2] [S3] [S4] |
| F_t | face amount (reduced by Option A withdrawals [S1] [S2]) |
| DB_t | death benefit per option and corridor |
| NAAR_t | net amount at risk = max(0, DB_t − AV_t) [S2] (floor **[std]**) |
| SC_t | surrender charge (per schedule, **[std]** scale) |
| CSV_t | cash surrender value = AV_t − SC_t − D_t [S1] |
| l_t | probability policy is in force at start of month t |
| status | in force / grace / lapsed / matured (age 121) |

## Assumption inputs

Three classes are distinguished explicitly; a model implementation should keep them
in separate input structures.

### (a) Contractual / guaranteed elements (from the spec; cited)

| Item | Value | Basis |
|---|---|---|
| Premium load ceiling | 6.0% of each premium | [S2] |
| COI guaranteed maxima | 2017 CSO sex-distinct S/NS ultimate ANB, monthly per $1,000 NAAR; cap $83.34 (observed $83.33–$83.34) | [S2] [S4] [R12]; cap [S1] [S2] [S3] [S4] |
| Per-policy charge | $10.00/month | [S2] [S4] |
| Per-$1,000 face charge | $0.20 per $1,000 of F_0 per month (current = guaranteed **[std]**) | [S2] |
| M&E guaranteed max | 0.60% p.a. | **[std]** (spec footnote 8) |
| Fixed-option floor | 1.0% effective annual | [S1] |
| Loan charged/credited rates | 2.0%/1.0% years 1–9; 1.05%/1.0% from year 10 | [S1] |
| Surrender charge | $18.00 per $1,000 initial, linear to 0 over 14 years | **[std]** (spec footnote 10) |
| Corridor factors κ | 250% (≤40), 215% (45), 185% (50), 150% (55), 130% (60), to 100% at 90–95; linear interpolation | [S2] [R3]; interpolation **[std]** |
| Grace / default | default when AV − SC − D ≤ 0; 61-day grace | [S1] [R8] |
| Age-121 rule | no premiums or monthly deductions after attained age 121; asset charges continue | [S1] [S2] [S4] |

### (b) Current non-guaranteed scales (insurer-declared; snapshot)

Governed as NGEs under ASOP No. 2 (by class; no recouping of past losses) [R11].

| Item | Value | Basis |
|---|---|---|
| Premium load — current | 4.0% flat | **[std]** (spec footnote 3) |
| COI — current scale | input vector c_t; default placeholder 50% of guaranteed 2017 CSO; disclosed anchor male 45 std NS year 1: current $0.04 (gtd $0.22) | **[std]** (spec footnote 5); anchor [S4] |
| M&E — current | 0.45% p.a. | [S1] |
| Declared fixed rate | 1.0% (= floor; declared rates not public) | **[std]** (spec footnote 13) |
| Credits (persistency credit, expense reductions) | none in baseline | **[std]**; variations [S1] [S2] |

### (c) Behavioral / experience assumptions

| Item | Recommended public basis | Basis |
|---|---|---|
| Best-estimate mortality | 2015 VBT (sex/smoker-distinct, RR tables for preferred fit), calibrated with ILEC 2012–2019 A/E experience | [REG-R18] [REG-R19] |
| Base lapse/surrender | LIMRA/SOA U.S. Individual Life Persistency (2009–2013, includes VUL plans); 2015–2021 UL lapse/surrender study for modern levels (VUL not broken out separately — applied to VUL by analogy, flagged) | [REG-R20] [REG-R21] |
| Premium persistency | 2015–2021 UL premium persistency study (flexible-premium payment behavior); VUL by analogy | [REG-R21] |
| Dynamic behavior | fund-performance-sensitive multipliers, see "Policyholder behavior modeling" | **[std]** |
| Insurer expenses | $75/policy/year maintenance + 2% of premium collection expense (placeholders; internal expense assumptions are not public) | **[std]** |
| Decrement mortality vs COI | Note: the COI charge uses the *current COI scale* (class (b), revenue); the death decrement uses *best-estimate mortality* (this class). They must never be conflated. | **[std]** convention |

VUL-specific policyholder-behavior studies were not retrieved; premium persistency
and dynamic lapse for VUL remain unsourced [unverified] — hence the **[std]**
placeholders below.

## Cash flow components and recursions

### Notation (defined once; used in both documents)

- t: policy month; x_t: attained age; l_t: in-force probability at BOM.
- P_t: premium paid at monthiversary t; γ: premium load rate (current 0.04).
- α_i: allocation share to account i (subaccounts i = 1,2; F = fixed).
- SA_{i,t}, FA_t, LA_t, D_t, AV_t, F_t, DB_t, NAAR_t, SC_t, CSV_t: state above.
- r_{i,t}: gross fund return of subaccount i in month t (scenario input).
- e_i: fund expense ratio (annual); m: M&E rate (annual; current 0.45% = 0.0045);
  i_fix: declared fixed rate; i_L, i_C: loan charged/credited rates.
- c_t: current monthly COI rate per $1,000 NAAR; e_pol = 10; e_face = 0.20.
- κ_t: corridor factor at x_t.
- q^d_t: best-estimate monthly mortality; q^w_t: monthly lapse; ρ_t: premium
  persistency factor.
- Monthly conversions: q^d_t = 1 − (1 − q^d,annual)^{1/12}; likewise lapse
  **[std]**.

### Monthly processing order (monthiversary t → t+1)

1. Advance to monthiversary t; on an anniversary, advance x_t and the policy-year
   dependent parameters (loan tier, SC_t, corridor κ_t). If x_t ≥ 121: skip steps
   2–4 and 6 (no premiums, no monthly deduction) [S1] [S2] [S4].
2. **Premium.** P_t = ρ_t × planned modal premium. Load: γ·P_t to insurer. Net
   premium allocation: SA_{i,t} += α_i·(1−γ)·P_t; FA_t += α_F·(1−γ)·P_t.
3. **Withdrawal** (if modeled): reduce accounts by withdrawal + $25 fee; Option A
   reduces F_t proportionately [S1] [S2]. Baseline: none **[std]**.
4. **Loan activity** (if modeled): new loans/repayments move value between
   investment options and LA_t [S3]; D_t accrues at i_L, LA_t at i_C, monthly
   compounding (1+i)^{1/12} **[std]** (contractually interest is due/capitalized
   annually [S1]).
5. **Death benefit and NAAR** (post-premium values):
   - Option A: DB_t = max(F_t, κ_t·AV_t)
   - Option B: DB_t = max(F_t + AV_t, κ_t·AV_t)
   - NAAR_t = max(0, DB_t − AV_t)
6. **Monthly deduction.**
   - COI_t = c_t · NAAR_t / 1000, with c_t ≤ min(2017 CSO max, 83.34)
     [S2] [S4] [R12]
   - MD_t = COI_t + e_pol + e_face·F_0/1000
   - Allocated pro rata across unloaned accounts **[std]**: each unloaned account j
     pays MD_t · V_j / Σ_unloaned V (loan account LA is excluded).
7. **Investment growth** over the month:
   - Subaccounts (unit-value dynamics): SA_{i,t+1} = SA'_{i,t} · (1 + r_{i,t}) ·
     (1 − e_i/12) · (1 − m/12), where SA' is the post-deduction value. In the
     contract, fund expenses and (for S1) M&E accrue daily in the unit value
     [S1]; the monthly product form is a **[std]** approximation. Insurers deducting
     M&E monthly [S2] [S3] [S4] are captured by the same factor.
   - Fixed option: FA_{t+1} = FA'_t · (1 + i_fix)^{1/12}, i_fix ≥ 1.0% [S1].
   - Loan account: LA_{t+1} = LA_t · (1 + i_C)^{1/12}; debt D_{t+1} = D_t ·
     (1 + i_L)^{1/12} **[std]** monthly accrual.
8. **EOM decrements and payments** (deaths before lapses **[std]**; balances here
   are EOM values after step 7, so outstanding debt is D_{t+1}):
   - Death: probability l_t·q^d_t; claim outflow = DB_t^{EOM} − D_{t+1} (debt
     repaid internally) [S1] [S3], where DB_t^{EOM} recomputes the option/corridor
     formula on EOM account values **[std]**.
   - Surrender/lapse: probability l_t·(1 − q^d_t)·q^w_t; outflow = CSV_t^{EOM} =
     AV_{t+1} − SC_t − D_{t+1} [S1].
   - Maintenance expense outflow: l_t · (75/12) **[std]**; premium expense 2%·P_t
     at step 2 **[std]**.
   - Survivorship: l_{t+1} = l_t · (1 − q^d_t) · (1 − q^w_t).
9. **Status checks.** If CSV_t ≤ 0 (and no NLG): default → grace; the baseline
   model lapses the policy at the next monthiversary if not cured, collapsing the
   61-day grace and notice mechanics [S1] [R8] into a one-month lag **[std]**. At
   x_t = 121, switch to the age-121 regime [S1] [S2] [S4].

### Scenario requirement

Subaccount gross returns r_{i,t} are exogenous scenario inputs. The reference model
runs either (a) deterministic scenarios (level or path-specified gross returns —
e.g., illustration-style level returns net of specified charges), or (b) stochastic
sets of gross-return paths. For statutory use, VM-20 defines a Deterministic
Reserve (Section 4) and a Stochastic Reserve (Section 5), with economic scenarios
addressed in its Appendix 1 [R7]; GAAP
long-duration (LDTI) measurement consumes the same projected cash flows with
different assumption-update and discounting overlays [REG-R34 — source not fetched;
summary-based, flagged](#uslib-reg-r34). Declared fixed-option rates would in practice vary with
general-account yields; the baseline holds i_fix at the 1.0% floor **[std]**.

### Separate-account vs general-account cash flow split

Account location: SA_{i,t} are separate-account assets; FA_t and LA_t are
general-account liabilities/assets [S1] [S3]. The model reports two views:

- **Gross (policyholder) view — the reference model's primary projection [std].**
  - Inflow: premiums l_t·P_t (full premium; the net premium is a pass-through into
    the accounts, the load is insurer revenue).
  - Outflows: death claims l_t·q^d_t·(DB_t^{EOM} − D_{t+1}); surrenders
    l_t(1−q^d_t)q^w_t·CSV_t^{EOM}; withdrawals; insurer expenses.
- **Net-of-account (general-account strain) view — derived report.**
  - Insurer margins collected: premium loads γP_t, monthly deductions MD_t, M&E
    collected via unit values, loan spread (i_L − i_C on D_t), surrender charges
    SC_t on surrender.
  - Net mortality cost: l_t·q^d_t·NAAR_t^{EOM} — the general-account cost of a
    death after seizing the account.
  - Account transfers (memo): on death, Σ_i SA_{i,t} moves separate account → general
    account; FA/LA release internally; on surrender the separate account liquidates
    to fund CSV.

Projected output columns (per month t, per scenario; probability-weighted by l_t)
**[std]** naming:

| Column | Definition | View |
|---|---|---|
| prem_gross | l_t · P_t | gross inflow |
| load_income | l_t · γ · P_t | net (margin) |
| md_income | l_t · MD_t (COI + per-policy + per-$1,000) | net (margin) |
| me_income | l_t · M&E collected via unit values | net (margin) |
| loan_spread | l_t · (i_L − i_C) accrual on D_t | net (margin) |
| claim_gross | l_t · q^d_t · (DB_t^{EOM} − D_{t+1}) | gross outflow |
| claim_net | l_t · q^d_t · NAAR_t^{EOM} | net (GA strain) |
| surr_outgo | l_t (1−q^d_t) q^w_t · CSV_t^{EOM} | gross outflow |
| sc_income | l_t (1−q^d_t) q^w_t · SC_t | net (margin) |
| expense | l_t · (maintenance + premium expense) | both |
| sa_transfer | account transfers separate ↔ general (memo) | memo |
| av_eop, naar, l_t | state snapshots for reconciliation | memo |

Reconciliation identity (per month): net GA cash flow = load_income + md_income +
me_income + loan_spread + sc_income − claim_net − expense; the gross view must
reproduce it after adding back the account pass-throughs (net premiums in,
account releases out) **[std]**.

**Warning — a common specification error:** "death benefit paid = DB − AV from the
separate account" is NOT the insurer's claim cash flow. The insurer's liability
outflow is the **full death benefit** (less policy debt); seizing the account value
is the *funding* of part of that outflow, and DB − AV (= NAAR) is the net
general-account strain. Projecting only DB − AV as the claim understates gross
benefit outgo and breaks reconciliation with statutory exhibits; projecting full DB
*and* separately expensing NAAR double counts. The reference model projects the
gross view and derives the net view arithmetically from the same run **[std]**.

## Policyholder behavior modeling

All dynamic formulas are **[std]**: no public VUL-specific dynamic-behavior study
was retrieved [unverified gap], so forms are standardized with rationale, calibrated
to the base tables in assumption class (c).

- **Funding ratio.** φ_t = AV_t / AV*_t, where AV*_t is the account value projected
  at issue under the pricing path (level 6% gross subaccount return, current
  charges, planned premiums) **[std]**. φ_t < 1 means performance/funding shortfall.
- **Dynamic lapse.** q^w_t = q^w,base_t · λ_t, λ_t = min(2.0, max(0.5,
  1 + β·(1 − φ_t))), β = 0.5 **[std]**. Rationale: in a protection-oriented VUL a
  performance shortfall raises the premium required to sustain coverage, pushing
  marginal policyholders to lapse (and underfunded policies drift toward the
  default test of step 9); overfunded policies are stickier. Bounds prevent extreme
  extrapolation.
- **Premium persistency.** ρ_t = ρ^base_t · min(1.3, max(0.7, φ_t^{−δ})), δ = 0.25
  **[std]**; ρ^base_t from the UL premium persistency study levels [REG-R21]
  (placeholder grading: 1.00 year 1 → 0.85 year 5 → 0.80 thereafter **[std]**).
  Rationale: shortfalls induce catch-up funding by retained policyholders
  (φ < 1 ⇒ ρ up); strong performance induces premium holidays (φ > 1 ⇒ ρ down) —
  the signature flexible-premium behavior the UL studies measure [REG-R21].
- **Surrender at surrender-charge cliff.** Optional spike multiplier on q^w in the
  month after SC_t reaches zero (end of year 14) **[std]**; magnitude an input.
- **No dynamic mortality.** Anti-selective lapse interaction (lapse-supported
  effects) is not modeled in the baseline **[std]**.

## Worked example — one month, two subaccounts

Model point: male 45 standard nonsmoker, F_0 = 500,000, Option A, GPT; policy year 3
(SC factor 12/14); planned premium $500/month paid; allocation 60/40; no fixed
balance, no debt; current scales as above (γ = 4%; c = $0.04 per $1,000 [S4] —
illustrative current rate at the disclosed representative point; e_1 = 0.75%,
e_2 = 0.55%, m = 0.45% [S1]); scenario month: r_1 = +1.00%, r_2 = −0.50% gross.
Premium level is illustrative only **[std]**. Corridor κ(45) = 215% [S2].

| Step | Item | SA_1 (equity) | SA_2 (bond) | Total AV |
|---|---|---|---|---|
| 0 | BOM balances | 30,000.00 | 20,000.00 | 50,000.00 |
| 2 | Premium 500.00; load 4% = 20.00; net 480.00 split 60/40 | +288.00 | +192.00 | 50,480.00 |
| 5 | DB = max(500,000; 2.15 × 50,480 = 108,532.00) = 500,000.00; NAAR = 449,520.00 | — | — | — |
| 6 | COI = 0.04 × 449.520 = 17.98; expense = 10.00 + 0.20 × 500 = 110.00; MD = 127.98, pro rata 60/40 | −76.79 | −51.19 | 50,352.02 |
| 7 | Growth factor: (1+r)(1−e/12)(1−m/12) → SA_1: 1.0100 × 0.999375 × 0.999625 = 1.008990; SA_2: 0.9950 × 0.999542 × 0.999625 = 0.994171 | ×1.008990 → 30,482.82 | ×0.994171 → 20,023.41 | 50,506.23 |
| — | Memo: M&E collected via unit values ≈ 11.44 + 7.51 = 18.95; insurer margin this month = 20.00 + 127.98 + 18.95 = 166.93 | — | — | — |
| — | Memo: SC = 18.00 × (12/14) × 500 = 7,714.29; CSV = 50,506.23 − 7,714.29 = 42,791.94 | — | — | — |
| — | Memo: EOM DB = 500,000.00; EOM NAAR = 449,493.77 (net GA strain if death this month; gross claim outflow = 500,000.00) | — | — | — |

EOM decrements (step 8) then weight the claim, surrender, and survivorship flows by
l_t·q^d_t and l_t(1−q^d_t)q^w_t; they are omitted from the table, which tracks the
account recursion per policy in force.

## Valuation and reserve pointers

This library projects gross liability cash flows; reserve layers are cited, not
reproduced. Statutory: VM-20 minimum reserve = NPR floor plus excess of max(DR, SR)
over aggregate NPR (less due/deferred premium asset); VUL without secondary
guarantees is in the "All Other" reserving category (product code 080), with
secondary guarantees in the ULSG category (code 090); variable life may not use the
SET certification method [R7]. GMDB reserves per AG XXXVII; separate-account
investment rules per AG XXIII (both texts still unretrieved, cited through [R7]);
**Model 270** requires reserves for variable
benefits held in the separate account on a basis consistent with the Standard
Valuation Law [R7] [R8] [REG-R1] — its AP&P print, **A-270**, has been read but carries
**no reference id**, so nothing is stated from it. The formulaic appendix items sitting
under the NPR are **A-820** [REG-R153], the **A-585** UL adaptation whose reach to a
variable contract is unresolved [REG-R155], and **A-830**, which excludes VUL by its
own terms [REG-R154]. Current Valuation Manual edition: Jan. 1, 2026
(VM-01/02/20/31, VM-C/M/G/V) [REG-R3]. Practice guidance: ASOP 52 (VM governs in
conflict) [R9]; AAA VM-20 practice note [R10]; ASOP 7 (cash flow analysis)
[REG-R27]; ASOP 56 (model governance for this implementation itself) [REG-R32]. Tax
reserves: greater of net surrender value and 92.81% of the NAIC-method reserve,
capped at statutory [REG-R16]. GAAP: LDTI (ASU 2018-12) overlays measurement on the
same projected cash flows [REG-R34 — not fetched; summary-based, flagged](#uslib-reg-r34).

## Key sensitivities and model risks

Dominant assumptions (roughly in order):

1. **Separate-account return scenario** (level and volatility): drives AV, hence
   NAAR, COI revenue, M&E revenue, corridor DB, and the default/lapse dynamics —
   the defining VUL sensitivity. Results are scenario-distributions, not points.
2. **Current COI scale** (the 50%-of-CSO placeholder **[std]**): COI is the largest
   charge; disclosed year-1 current/guaranteed ratios (e.g., 0.04/0.22 [S4]) show
   the placeholder is conservative early and the select-to-ultimate shape matters.
3. **Premium persistency ρ_t**: flexible premiums are the UL-family assumption with
   the widest behavioral range [REG-R21]; funding level feeds back into lapse and
   default.
4. **Lapse and dynamic lapse (λ_t)**: level from dated/analogous studies
   [REG-R20] [REG-R21] with the dynamic form unsourced **[std]** [unverified].
5. **Best-estimate mortality** vs 2015 VBT/ILEC [REG-R18] [REG-R19]; NAAR-weighted,
   so it interacts with the return scenario.

Known modeling pitfalls:

- Conflating COI-scale mortality (charge) with decrement mortality (experience).
- Projecting DB − AV as the death outflow (see the warning above).
- Forgetting the NAAR floor at zero, or letting corridor factors create
  discontinuous DB jumps at quinquennial ages instead of interpolating **[std]**.
- Applying M&E both in the unit-value factor and as a monthly deduction (double
  counting across insurer conventions — pick one; this model uses the unit-value
  factor **[std]**).
- Pro-rata deduction allocation breaking on zero unloaned balances (guard the
  denominator; deduction shortfall triggers the default test).
- Ignoring the loan account: loaned value earns i_C, not fund returns; debt
  compounds at i_L; DB and CSV are debt-reduced [S1] [S3].
- Missing the age-121 regime switch (charges stop; asset drags continue)
  [S1] [S2] [S4].
- Grace-period collapse **[std]** accelerates lapses by up to two months versus the
  contractual 61-day mechanics [S1] [R8] — immaterial for most uses, material for
  short-horizon liquidity studies.
- The NLG variation changes the risk profile qualitatively (lapse floor under poor
  performance → higher NAAR persistence); see
  `products/guaranteed_ul/technical-notes.md` for shadow-account mechanics and
  [S4] for the rider's notional-load design.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #uslib-variable_ul-r10
[R11]: #uslib-variable_ul-r11
[R12]: #uslib-variable_ul-r12
[R3]: #uslib-variable_ul-r3
[R4]: #uslib-variable_ul-r4
[R7]: #uslib-variable_ul-r7
[R8]: #uslib-variable_ul-r8
[R9]: #uslib-variable_ul-r9
[REG-R1]: #uslib-reg-r1
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R155]: #uslib-reg-r155
[REG-R16]: #uslib-reg-r16
[REG-R18]: #uslib-reg-r18
[REG-R19]: #uslib-reg-r19
[REG-R20]: #uslib-reg-r20
[REG-R21]: #uslib-reg-r21
[REG-R27]: #uslib-reg-r27
[REG-R3]: #uslib-reg-r3
[REG-R32]: #uslib-reg-r32
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
