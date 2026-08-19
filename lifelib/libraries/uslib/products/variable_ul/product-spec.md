# Product Specification

**Status:** Draft, 2026-08-03; cross-product [REG-R#] citations extended 2026-08-06 with
the AP&P Manual appendix items read at first hand. Product sources [S#]/[R#] were
accessed 2026-08-03; the [REG-R#] entries carry their own access dates per entry in
`sources.md`. This document is a standardized composite
specification for reference liability-model implementation. It does not describe any
single insurer's product. Tags [S#] and [R#] cite the product research notes
(`_research/variable-ul.md`); [REG-R#] cites the cross-product reference library
(`references/regulatory-and-actuarial-references.md`; research provenance in
`_research/regulatory-actuarial.md`, same R-numbering). **[std]** marks a
standardization introduced for the reference implementation (not a sourced fact);
every **[std]** table row carries a footnote with rationale and the observed range.
Facts the research notes flag as [unverified] remain flagged here.

## Product overview and market role

Variable universal life (VUL) is a flexible-premium individual life insurance
contract whose account value is allocated by the policyholder between (a) variable
investment options — subaccounts of a registered separate account, each investing in
a corresponding registered fund — and (b) one or more general-account fixed options
[S1] [S2] [S3] [S4]. Death benefits and account values reflect investment experience;
guarantees are backed by the insurer's general-account claims-paying ability
[S1] [S4]. For statutory purposes, variable life is life insurance whose amount or
duration varies with separate-account investment experience [R7].

VUL is a security: the separate account registers as a unit investment trust and the
contract registers on SEC Form N-6 [R1]; cash value is invested in
policyholder-selected portfolios, investment return is not guaranteed, and FINRA
regulates the selling firms and professionals [R13]. Prospectuses follow the N-6 item
structure (Key Information, standardized fee tables, Standard Death Benefits, Loans,
Lapse) [R1] [S1] [S2] [S3] [S4], with summary-prospectus delivery permitted under rule
498A since July 1, 2020 [R2].

The representative design below is the mainstream retail archetype (the pattern of
two of the four filings surveyed [S1] [S2]): front premium load plus multi-year
per-$1,000 surrender charge, monthly deductions (COI on net amount at risk,
per-policy fee, per-$1,000 face charge), an asset-based M&E risk charge on
separate-account assets, death benefit options A/B with the §7702 corridor, a
general-account fixed option with an interest floor, spread loans, and monthly
deductions ceasing at age 121 [S1] [S2] [S4]; low-load designs exist as a variation
[S3] (see "Variations across insurers").

## Representative specification

### Issue rules and policy term

| Parameter | Representative value | Basis |
|---|---|---|
| Policy form | Flexible-premium variable universal life; account value in separate-account subaccounts plus a fixed option | [S1] [S2] [S3] [S4] |
| Issue ages | 0–85 | [S2] |
| Minimum face amount | $100,000 | **[std]** (1) |
| Underwriting classes | Preferred best through standard, smoker-distinct; substandard via flat extras | [S1] |
| Maturity | None; on the policy anniversary at insured attained age 121, premiums are no longer accepted and monthly deductions cease; the policy continues to death or surrender (asset-based M&E and fund expenses continue) | [S1] [S2] [S4] |
| Renewal / conversion | Not applicable (permanent coverage; no renewal or conversion mechanism) | **[std]** (2) |

Footnotes:
1. **[std]** Minimum face. Observed: $75,000 for issue ages 18–75, $50,000 (0–17),
   $100,000 (76–80), $250,000 (81+) [S1]; a possible $10,000 policy minimum noted in
   footnotes [S2]. $100,000 chosen as a single round figure inside the observed band
   for retail protection/accumulation VUL.
2. **[std]** Statement of absence. The retrieved filings describe no renewal or
   conversion features for the base policy [S1] [S2] [S3] [S4]; recorded here as an
   explicit modeling boundary.

### Premiums and premium loads

| Parameter | Representative value | Basis |
|---|---|---|
| Premium flexibility | Flexible amount/timing after required initial premium; minimum subsequent premium $25 | [S1] |
| Premium refusal rights | Insurer may refuse premium that would increase death benefit under §7702 by more than it increases the fund, or that exceeds the Guideline Premium Limit; premium creating MEC status must be removed timely | [S1] [R3] [R4] |
| Premium load — guaranteed maximum | 6.0% of each premium | [S2] |
| Premium load — current | 4.0% of each premium, all years | **[std]** (3) |

Footnotes:
3. **[std]** Current load level/shape. Observed: 6% until two sales-load target
   premiums paid, then 4% [S2]; sales charge max 6% (current 3% years 1–5, 2.25%
   years 6–10, 0 after) plus premium-based admin charge max 7.5% (current 3.75%)
   [S1]; max 6.50% [S4]; no premium load at all [S3]. The composite collapses these
   to a single flat current 4% load under a 6% guaranteed ceiling — one filing's
   long-run current rate [S2] — to avoid modeling duration-graded and two-part load
   schedules.

### Monthly deductions (taken at each monthiversary from account value)

| Parameter | Representative value | Basis |
|---|---|---|
| Cost of insurance (COI) | Monthly rate per $1,000 of net amount at risk (NAAR = death benefit − account value, floored at zero); rates vary by sex, class, attained age, band, duration | [S1] [S2] [S4] (floor: **[std]** (4)) |
| COI guaranteed maximum basis | 2017 CSO, sex-distinct smoker/nonsmoker ultimate ANB tables | [S2] [S4] [R12] |
| COI rate cap | $83.34 per $1,000 per month (observed $83.33–$83.34 across filings; ≈ 1/12 of $1,000 — the monthly rate that fully consumes the NAAR near attained age 120/121; interpretation [unverified]) | [S1] [S2] [S3] [S4] |
| COI current scale | Input scale; default placeholder = 50% of guaranteed 2017 CSO maxima; representative disclosed anchor: male 45 standard nonsmoker year 1 — guaranteed $0.22, current $0.04 per $1,000 | **[std]** (5); anchor [S4] |
| Per-policy administrative charge | $10.00 per month, all years | [S2] [S4] |
| Per-$1,000 face charge | $0.20 per $1,000 of initial face amount per month, all years; current = guaranteed | [S2] (level), duration/current basis **[std]** (6) |

Footnotes:
4. **[std]** NAAR floor at zero. Sources define the net amount at risk (NAAR) as death benefit − account value
   [S2]; the explicit floor at zero (corridor keeps DB ≥ AV in normal operation) is a
   modeling standardization.
5. **[std]** Current COI proxy. Full current COI tables by age/sex/class/duration are
   not publicly disclosed — only min/max/representative rates appear in prospectuses;
   actual scales live in policy data pages and actuarial memoranda; a model needs a
   proxy such as a percentage of 2017 CSO [unverified, recorded as a research gap].
   Observed representative points: current $0.02–$83.34 (rep female 43 preferred best
   $0.13) [S1]; $0.01–$83.34 (rep male 35 elite $0.08) [S2]; max $83.33333/min
   $0.02667 (rep max $0.17771) [S3]; guaranteed $0.01–$83.34 (rep male 45 std NT yr 1:
   gtd $0.22, curr $0.04) [S4]. 50%-of-CSO is a placeholder for the current scale, to
   be replaced per model point; disclosed year-1 current/guaranteed ratios are much
   lower (select effect).
6. **[std]** Per-$1,000 charge shape. Level $0.20 is one filing's representative
   charge on initial base face, payable all years [S2]. Observed range: $0.07–$8.21
   per $1,000 (rep $0.21; current first 7 years only) [S1]; $0.15–$0.47 (rep $0.20)
   [S2]; up to $0.31263 (rep $0.1262) [S3]; guaranteed $0.09–$11.39, current
   $0.00–$3.81 plus a $29–$40 coverage charge [S4]. Setting current = guaranteed =
   $0.20 all years avoids a second NGE dimension.

### Asset-based charges (separate-account assets)

| Parameter | Representative value | Basis |
|---|---|---|
| M&E risk charge — current | 0.45% effective annual rate, deducted daily against variable investment options (reference model approximates monthly) | [S1] (monthly approx. **[std]** (7)) |
| M&E risk charge — guaranteed maximum | 0.60% effective annual | **[std]** (8) |
| Fund operating expenses | Per-subaccount expense ratios borne via unit values; observed lineup range 0.29%–1.18% | [S1] (9) |

Footnotes:
7. **[std]** Deduction frequency. S1 deducts daily via unit values; S2/S3/S4 deduct
   monthly [S2] [S3] [S4]. The reference model applies the asset charge in the monthly
   unit-value factor (see technical notes) — a monthly approximation of daily accrual.
8. **[std]** Guaranteed M&E ceiling. Observed: 0.45% (S1, level not split
   current/guaranteed in the fee-table extract) [S1]; 1.00% years 1–10 / 0.50%
   after [S2]; 0.6% maximum, guaranteed for policy years 1–20 [S3]; 0.36% max /
   0.20% current [S4]. 0.60% adopts the S3 ceiling as a mid-range guaranteed
   maximum over the S1-based 0.45% current rate.
9. Cross-insurer fund-expense ranges: 0.55%–2.88% gross / 0.54%–2.57% net [S2];
   0.46%–2.54% [S3]; 0.08%–1.93% [S4]. The reference model collapses the lineup to
   two representative subaccounts (equity 0.75%, bond 0.55% expense ratios) —
   **[std]**, chosen inside the observed ranges; see technical notes.

### Surrender charges and transaction fees

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender charge period | First 14 policy years; applies on lapse, full surrender, or face decrease (pro rata on decreases) | [S1] [S2] |
| Surrender charge level | Initial $18.00 per $1,000 of face, declining linearly to zero at the end of policy year 14 | **[std]** (10) |
| Withdrawal fee | $25 per withdrawal; minimum withdrawal $500 | [S1] |
| Transfer fee | 12 free transfers per year; $25 each thereafter | [S1] [S4] |

Footnotes:
10. **[std]** Surrender charge scale. Complete per-$1,000 schedules by issue
    age/class are in contract data pages, not prospectus bodies (research gap); only
    ranges, representative values, and durations (10/14/15 years) were extractable.
    Observed: initial $5.31–$54.56 per $1,000 (rep female 43: $17.55), 14 years [S1];
    $11.40–$48.50 (rep male 35: $18.29), 10 years (+10 after face increases) [S2];
    none [S3]; max $49.72, 15 years per coverage layer [S4]. $18/1,000 sits on the
    two representative observed points; linear runoff is a standardized shape.

### Death benefit options and §7702 mechanics

| Parameter | Representative value | Basis |
|---|---|---|
| Option A (Type A / Option 1) | DB = face amount (level); NAAR shrinks as fund grows | [S1] [S2] [S4] |
| Option B (Type B / Option 2) | DB = face amount + account value | [S1] [S2] [S3] [S4] |
| Corridor minimum | DB ≥ corridor factor × account value; representative GPT factors 250% (ages ≤40), 215% (45), 185% (50), 150% (55), 130% (60), grading to 100% at ages 90–95 | [S2] (factors); [R3] (statute); interpolation **[std]** (11) |
| §7702 test | Guideline Premium Test (GPT) for the baseline model point; CVAT/GPT elected at issue in practice | Election [S1]; baseline choice **[std]** (12) |
| DB option changes | Permitted subject to approval; face adjusted so total DB is unchanged at the change date | [S1] |
| Automatic DB increase | Insurer may increase DB to preserve §7702 qualification and refuse premium breaching guideline limits | [S1] [S2] |
| DB offsets | Death benefit payable reduced by outstanding policy debt and, during grace, amounts needed to keep the policy in force | [S1] [S3] |

Footnotes:
11. **[std]** Corridor interpolation. S2 quotes quinquennial representative factors;
    §7702(d) prescribes 250% for attained ages 0–40 declining to 100% at ages 90–95
    [R3]. The reference model linearly interpolates between the quoted ages and
    grades to 100% at 95.
12. **[std]** Test election. Both tests are observed; GPT chosen for the baseline
    because the corridor-factor mechanics are fully specified by the sourced factor
    table [S2] [R3]. CVAT variation: alternate DB = account value × reciprocal of the
    net single premium at 2% interest and 2017 CSO mortality (101% above age 99)
    [S2]; the 2% rate traces to the post-2020 §7702(f)(11) "insurance interest rate"
    with its 2021 transition rate [R3].

### Fixed option and policy loans

| Parameter | Representative value | Basis |
|---|---|---|
| Fixed option crediting | General-account option, credited daily at a declared effective annual rate; guaranteed minimum 1.0% | [S1] |
| Current declared rate (baseline) | 1.0% (= floor) | **[std]** (13) |
| Fixed-option transfer-out limit | Greater of 25% of option value or $2,000 per contract year | [S1] |
| Loan value | 99% of cash value in variable options plus 100% of the remainder | [S1] |
| Standard loan (years 1–9) | Charged 2.0% effective annual; loaned amount credited 1.0% (net spread 1.0%) | [S1] |
| Preferred loan (from 10th anniversary) | All loans: charged 1.05% vs credited 1.0% (net spread 0.05%) | [S1] |
| Loan interest | Due each contract anniversary; capitalized if unpaid | [S1] |
| Loan collateral | Loaned amounts moved from investment options to a general-account loan account | [S3] |
| Excess-debt default | Debt ≥ fund less surrender charge triggers default | [S1] |

Footnotes:
13. **[std]** Declared rate. Current declared fixed-account crediting rates are
    nonguaranteed and not stated numerically in the filings beyond floors (research
    gap). Baseline sets declared = floor; observed floors: 1.0% [S1], 1.5% [S2],
    2.0% [S4], loan account ≥0.25% [S3].

### Grace, lapse, reinstatement

| Parameter | Representative value | Basis |
|---|---|---|
| Default test | Policy in default when fund less surrender charge less debt ≤ 0 (or debt ≥ fund less surrender charge), unless a no-lapse guarantee applies | [S1] |
| Grace period | 61 days from notice; notice premium ≈ 3 months of deductions; death benefit during grace equals the death benefit in effect (net of amounts due) | [S1] [R8] |
| Reinstatement | Within 3 years of termination with evidence of insurability and payment covering ≈3 months of deductions plus premium charge | [S2] |

## Contractual mechanics

Notation here matches the technical notes (`technical-notes.md`); formulas are stated
per policy month t with monthiversary processing.

**Premium provisions.** Premiums are flexible in amount and timing after the required
initial premium; minimum subsequent premium $25 [S1]. Each premium P is reduced by
the premium load γ (current 4.0% **[std]**, guaranteed ≤ 6.0% [S2]) and the net
premium P·(1−γ) is allocated to subaccounts and the fixed option per the
policyholder's allocation percentages (whole-percentage allocations; a model-point
attribute). The insurer may refuse premiums that would breach §7702 guideline limits
or force a death-benefit increase, and MEC-creating premium must be removed timely
[S1] [R3] [R4].

**Account value.** Account value AV = Σᵢ subaccount values + fixed-option value +
loan-account value [S1] [S2] [S3] [S4]. Subaccount values evolve with unit values driven
by gross fund performance less fund operating expenses less the asset-based M&E
charge (daily in the contract [S1]; monthly approximation in the model **[std]**).
The fixed option accrues daily interest at the declared rate, floor 1.0% [S1].

**Monthly deduction.** At each monthiversary, the insurer deducts from account value:

    MD_t = COI_t + e_pol + e_face · F_0/1000
    COI_t = c_t · NAAR_t / 1000,  NAAR_t = max(0, DB_t − AV_t)

with e_pol = $10.00 [S2] [S4], e_face = $0.20 per $1,000 of initial face F_0 [S2],
and c_t the current monthly COI rate per $1,000, bounded by the 2017 CSO guaranteed
maximum [S2] [S4] [R12] and capped at $83.34 [S1] [S2] [S4]. The deduction is taken from
unloaned accounts pro rata **[std]**. Current charges are nonguaranteed elements: the
insurer may raise them up to guaranteed maxima, by class, and cannot recoup prior
losses or distribute prior gains [S1] [R11].

**Death benefit.** Option A: DB_t = max(F_t, κ_t·AV_t). Option B:
DB_t = max(F_t + AV_t, κ_t·AV_t). κ_t is the GPT corridor factor at attained age
[S2] [R3]. The amount payable at death is DB_t minus outstanding policy debt and any
amounts required during grace [S1] [S3].

**Charges and credits.** The asset-based M&E charge (current 0.45% p.a. [S1],
guaranteed max 0.60% **[std]**) and fund expense ratios reduce unit values; all other
charges are explicit deductions. The baseline excludes insurer-specific credits —
one filing's persistency credit (0.40% p.a. of unloaned fund from the 9th
anniversary) [S1] and another's investment-expense reduction (≥0.15% daily
unit-value credit) [S2] are documented as variations **[std]**.

**Loans.** A loan up to the loan value (99% of variable cash value + 100% of the
remainder [S1]) moves collateral from the investment options into a general-account
loan account [S3]. Interest is charged at 2.0% (standard) or 1.05% (preferred, from
the 10th anniversary) and the loan account is credited 1.0% [S1]; interest is due
each anniversary and capitalized if unpaid [S1]. Debt reduces the death benefit and
surrender proceeds; debt ≥ fund less surrender charge triggers excess-debt default
[S1]. Overloan protection riders exist (exercise charges 3.5% of fund [S1];
1.12%–4.52% of accumulated value [S4]) but are out of the baseline.

**Withdrawals.** Minimum $500, $25 fee; remaining cash surrender value must cover two
months of deductions [S1]. Under Option A a withdrawal reduces the face amount
(proportionate reduction [S2]) and can trigger a pro-rata surrender charge [S1].

**Grace, lapse, reinstatement.** Default occurs when AV − surrender charge − debt
≤ 0 unless a no-lapse guarantee applies [S1]; a 61-day grace period follows notice,
with a notice premium of ≈3 months of deductions [S1], consistent with the Model 270
minimum grace and DB-during-grace requirements [R8]. Reinstatement within 3 years
requires evidence of insurability and ≈3 months of deductions plus premium charge
[S2].

**Age 121.** From the anniversary at attained age 121: no further premiums accepted,
no monthly deductions; asset-based charges and fund expenses continue; the policy
continues to death or surrender; lapse only from excess debt [S1] [S2] [S4].

## Riders

In scope (specified; excluded from the baseline projection **[std]**):

- **No-lapse guarantee (NLG) rider** — documented as a variation, not in the
  baseline. Observed forms: built-in 5-year limited guarantee plus premium-funded
  lapse protection rider from year 6 [S1]; age-graded no-charge rider guaranteeing
  15 years at issue ages 0–70 grading to 5 years at 80+, subject to specified
  guarantee premiums, terminating if debt exceeds account value [S2]; premium-test
  no-lapse provision [S3]; priced flexible-duration rider ($0.00–$0.15 per $1,000
  NAAR monthly, rep $0.05) tracked via a shadow fund with notional 5.50% no-lapse
  premium load and 10% excess premium load, funds floored at zero [S4]. For
  shadow-account mechanics see the guaranteed-UL technical notes
  (`products/guaranteed_ul/technical-notes.md`; research provenance
  `_research/guaranteed-ul.md`); statutory note: VUL with secondary guarantees is
  a distinct valuation category (code 090) in the ULSG reserving category under
  VM-20 [R7].
- **Overloan protection rider** — prevents lapse from excess debt; one-time exercise
  charge 3.5% of the fund [S1] or 1.12%–4.52% of accumulated value (rep male 85:
  2.97%) [S4]; one filing instead offers a loan extension endorsement forcing DB
  option A [S2]. Interacts with loan mechanics; excluded from baseline.

Out of scope (listed only; observed charges recorded in the research notes):
accelerated death benefit / chronic & terminal illness riders (two forms each in
[S1] [S2] [S4]); layered term riders (annual renewable, scheduled and corporate-term
forms [S4]); disability waiver riders [S1] [S2]; children's term [S1] [S2];
accidental death [S1]; guaranteed insurability [S2]; enhanced early cash value
riders [S1] [S2]; charitable legacy [S2]; index-linked account options on the VUL
chassis [S2] [S4].

## Variations across insurers

1. **Load structure.** Two archetypes: (a) front-loaded + back-loaded traditional
   VUL — premium loads 6%–7.5% max (current 3%–4%) plus 10–15 year surrender charge
   [S1] [S2] [S4]; (b) low-load/no-load — no premium load, no surrender charge,
   compensated through asset-based and per-$1,000 charges [S3]. The baseline follows
   (a) because it remains the dominant retail pattern.
2. **M&E / asset charge.** 0.20% current/0.36% max monthly [S4]; 0.45% daily [S1];
   0.6% max monthly [S3]; 1.00%/0.50% duration-tiered monthly [S2]. Baseline: flat
   0.45% current under a 0.60% ceiling — mid-range, avoids duration tiering.
3. **COI basis.** All quote per-$1,000-NAAR monthly rates capped near $83.33–$83.34;
   guaranteed maxima moved from 2001 CSO (older generations, e.g., S1) to 2017 CSO
   [S2] [S4]; two-tier COI structures and face-amount banding exist [S1];
   gender-neutral policies use an 80% male/20% female blended 2017 CSO table [S2].
   Baseline: 2017 CSO sex-distinct, no banding — the current-generation norm.
4. **Death benefit options.** A and B universal [S1] [S2] [S3] [S4]; return-of-premium
   Option C (DB = face + premiums − withdrawals, subject to a limit) in only one of
   the four filings [S4]; another pivots on a Target Age with an expected
   Option 2 → Option 1 switch [S3]. Baseline: A and B only.
5. **Secondary guarantees.** From short built-in guarantees [S1] [S3], age-graded
   15→5-year riders [S2], to priced flexible-duration shadow-fund riders [S4].
   Baseline excludes the NLG (see Riders) so that base-contract lapse mechanics stay
   clean; the guarantee is a documented variation.
6. **Fixed/indexed options.** Floors 1% [S1], 1.5% [S2], 2% [S4]; indexed accounts
   bolted onto the VUL chassis [S2] [S4]. Baseline: single fixed option, 1% floor —
   S1's fixed option, whose transfer-out and loan mechanics the baseline already
   adopts; indexed options are separately-prospectused add-ons out of scope.
7. **Loans.** Net spreads 0.05%–1.0% duration-dependent [S1]; Moody's-linked charged
   rate, spread 1% → 0% from year 11 [S2]; flat 0.25% [S3] [S4]. Baseline: S1's fixed
   2.0%/1.0% then 1.05%/1.0% — fully specified numerically in the source.
8. **Credits.** Persistency credit 0.40% from year 9 [S1]; unit-value expense
   reductions [S2]; duration step-downs of loads/M&E [S1] [S2]. Excluded from the
   baseline for parsimony; material for calibration to any specific insurer.

## Regulatory context

**Federal securities law.** VUL contracts are securities registered on Form N-6 by
separate accounts organized as unit investment trusts [R1]; the 2020 amendments
(rule 498A) allow summary-prospectus delivery with the statutory prospectus online
[R2]. FINRA regulates the distributing firms and representatives; suitability
framing applies [R13].

**NAIC variable life regulation.** Model 270 (Variable Life Insurance Model
Regulation) sets insurer qualification, policy requirements (including grace-period
minimums — flexible-premium grace ending not less than 61 days after specified
notice, with DB during grace equal to the DB in effect), separate-account rules, and
requires reserves for variable benefits to be held in the separate account on a
basis consistent with the Standard Valuation Law [R8]; it appears as A-270 among the
valuation requirements in the Valuation Manual appendices [R7]. That AP&P print,
**A-270**, has since been read alongside A-585 in the free *As of March 2026* manual,
but **no reference id was assigned to it**, so nothing in this library is stated or
cited from its text; everything above rests on Model 270 itself [R8]. The UL Model
Regulation (Model 585) applies to individual UL *except* variable UL, which is
carved out to the variable-products rules and federal securities law [REG-R5] —
**but the AP&P appendix print does not carry that carve-out.** A-585 prints
definitions and valuation requirements only, no scope section and no applicability
threshold of any kind, and its ¶7 definition of a universal life insurance policy
turns solely on separately identified interest credits and mortality and expense
charges, saying nothing about a separate account [REG-R155]. The carve-out is Model
#585's own text [REG-R5], and Model #585 was not re-read against the appendix print,
so **whether the A-585 CRVM adaptation reaches a variable contract is open**, not
settled [REG-R155].

**Statutory reserves (VM-20).** VUL is individual life subject to VM-20
principle-based reserves for policies issued on/after the Valuation Manual operative
date: minimum reserve = NPR floor plus the excess of max(DR, SR) over aggregate NPR
(less due/deferred premium asset), with exclusion tests; variable life cannot use
the SET certification method [R7]. That operative date is **1 January 2017**, now
carried at first hand by the AP&P print of the SVL: A-820 ¶3 applies the
principle-based ¶¶23–27 to policies issued on or after it, and ¶4 keeps earlier issues
on ¶¶5–22, to which the principle-based provisions "shall not apply" [REG-R153]. VUL
without secondary guarantees is valued in the
"All Other" category (product code 080); with secondary guarantees, in the ULSG
category (code 090) [R7] — but that **category is VM-20's own and does not carry the
XXX secondary-guarantee construction with it**: A-830 excludes variable life and
variable universal life outright (¶3.a.iii, ¶3.a.iv), so that appendix does not reach
this product at all [REG-R154]. The formulaic layer under the NPR is **A-820**, which
reaches a varying-amount, varying-premium contract through its ¶13.a extension of CRVM
[REG-R153], plus the **A-585** universal life adaptation if it reaches a variable
contract — an open question, see above [REG-R155]. GMDB reserves for variable life are
addressed by AG XXXVII, separate-account investments by AG XXIII [R7]. Current edition:
Valuation Manual, Jan. 1, 2026 [REG-R3]; the SVL is Model 820 [REG-R1].

**Illustrations.** The Life Insurance Illustrations Model Regulation (Model 582)
explicitly excludes variable life [REG-R4]; VUL sales illustrations are instead
governed by the securities disclosure regime (N-6/498A) [R1] [R2] and FINRA
communications rules (Rule 2211 identified but not fetched) [R13].

**Federal tax — product qualification.** §7702 requires CVAT or GPT-plus-corridor
qualification, with the post-2020 dynamic "insurance interest rate" (2% transition
for 2021 issues) [R3]; §7702A applies the 7-pay test, with MEC status triggering
less-favorable distribution taxation and material changes restarting the test [R4].
Separate-account diversification under §817(h) and Treas. Reg. §1.817-5 (55/70/80/90
quarterly tests, look-through for insurance-dedicated funds) is a condition of
life-insurance treatment [R5] [R6].

**Nonguaranteed elements.** Current COI scales, loads, declared rates, and credits
are NGEs governed by ASOP No. 2: determination policy, policy classes reflecting
anticipated experience, and scales based on reasonable expectations of future
experience, not recouping past losses or distributing past gains [R11].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_ul-r1
[R11]: #uslib-variable_ul-r11
[R12]: #uslib-variable_ul-r12
[R13]: #uslib-variable_ul-r13
[R2]: #uslib-variable_ul-r2
[R3]: #uslib-variable_ul-r3
[R4]: #uslib-variable_ul-r4
[R5]: #uslib-variable_ul-r5
[R6]: #uslib-variable_ul-r6
[R7]: #uslib-variable_ul-r7
[R8]: #uslib-variable_ul-r8
[REG-R1]: #uslib-reg-r1
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R155]: #uslib-reg-r155
[REG-R3]: #uslib-reg-r3
[REG-R4]: #uslib-reg-r4
[REG-R5]: #uslib-reg-r5
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
