# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`_research/universal-life.md`; [REG-R#] tags refer to the cross-product reference
library `references/regulatory-and-actuarial-references.md` (its own R-numbering;
research provenance in `_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation. Parameter values are
identical to those in `product-spec.md`; the implementation anchor for mechanics is
the Pacific Life Versa-Flex PRO specimen policy [S3].

**Revision note, 2026-08-06.** The reserve material under "Valuation and reserve
pointers" was revised when the AP&P Manual appendix items were read at first hand from
the free *As of March 2026* download: **A-585** (universal life) [REG-R155], **A-820**
with A-821 and A-822 [REG-R153] and **A-830** [REG-R154]. The shared reference
numbering now runs **R1–R157**, with most of the **R73–R149** block unused.
Nothing outside those paragraphs was re-dated, and **no [std] or [unverified] marker
elsewhere in this file was upgraded**: every standardization here is a
product-parameter choice made because insurers do not publish current scales [S3] [S5],
a limit the appendix reading does not touch.

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows (premiums, death claims, surrender
  and withdrawal payments, expenses, loan flows optional) for a single-policy model
  point of current-assumption fixed UL, on a monthly grid. Reserves are not computed
  (see Valuation and reserve pointers).
- **Projection frequency.** Monthly. The contract credits interest daily on a 365-day
  year [S3]; the model discretizes to monthly compounding **[std]**: one month of
  interest is applied at the end of each policy month to the post-deduction balance.
- **Timing / monthiversary processing.** All policy transactions are processed on the
  monthiversary (the monthly payment date — the same day each month as the policy
  date [S3]), at the beginning of the policy month (BOM); interest accrues over the
  month and is credited at end of month (EOM) **[std]**. The monthly deduction taken
  at BOM pays for that policy month's coverage (the specimen states the deduction
  provides coverage for the following policy month [S3]; with BOM indexing the
  deduction at the start of month t covers month t).
- **Age basis.** Age nearest birthday (ANB) **[std]**. Rationale: the specimen's
  nonforfeiture basis is 2001 CSO ANB [S3], the SOA/LIMRA UL study methodology is ANB
  [R7], and the 2017 CSO/2015 VBT families provide ANB variants [R4] [REG-R18].
- **Model points.** Single-policy model points, projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  No aggregation logic is specified here.
- **Decrement order within a month.** Contractual transactions first (BOM), then
  decrements (death, lapse) treated as EOM events **[std]** (see processing order).
- **Rounding.** Intermediate values carried at full precision; cash flows reported to
  cents **[std]**. (Production admin systems round per-transaction; the specimen is
  silent on model rounding.)

---

## Model point attributes

| Attribute | Type | Example (anchor cell [S3]) |
|---|---|---|
| `issue_age` | int (ANB) | 35 |
| `sex` | enum {M, F} | M |
| `risk_class` | enum (6 classes, spec table) | Standard NT |
| `face_amount` | currency | 100,000 |
| `db_option` | enum {A, B} | A |
| `qual_test` | enum {GPT} (CVAT out of scope) | GPT |
| `issue_date` / `policy_month_offset` | date / int | month 1 |
| `planned_premium_annual` | currency | 1,800 **[std]** |
| `premium_pattern` | enum {level, single, target} | level **[std]** |
| `premium_mode` | enum {monthly, annual} | monthly **[std]** |
| `av_initial` | currency (0 at issue; >0 for in-force cells) | 0 |
| `loan_balance_initial` | currency | 0 |
| `sc_layer_table` | schedule per $1,000 | $9.00 initial, 9-yr **[std]** |
| `guideline_single_premium` | currency (compliance input) | 34,138.15 [S3, incl. riders](#uslib-universal_life-s3) |
| `guideline_level_premium` | currency (compliance input) | 2,825.52 [S3, incl. riders](#uslib-universal_life-s3) |
| `seven_pay_premium` | currency (compliance input) | 6,702.10 [S3, incl. riders](#uslib-universal_life-s3) |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `AV(t)` | Account value (the specimen's "accumulated value") at end of policy month t | monthly recursion |
| `F(t)` | Total face amount (after any option changes/withdrawal-driven reductions) | on events |
| `DB(t)` | Death benefit in month t after corridor test | monthly |
| `NAAR(t)` | Net amount at risk for COI in month t | monthly |
| `SC(t)` | Surrender charge in month t | monthly amortization |
| `L(t)` | Policy loan balance (with capitalized interest) | monthly |
| `CumPrem(t)` | Cumulative premiums less withdrawal offsets (GPT/7-pay tracking) | monthly |
| `l(t)` | In-force probability at end of month t (survivorship) | monthly decrements |
| `grace_flag(t)` | In-grace indicator and months-in-grace counter | monthly |
| `wd_used_year` | Free-withdrawal usage in current policy year | on withdrawal |

---

## Assumption inputs

Three classes are distinguished explicitly. Class (a) is contractual and cannot be
changed by the insurer; class (b) is the insurer-declared current scale (an NGE under
ASOP 2 [R8]); class (c) is the modeler's view of policyholder/insurer experience.

### (a) Contractual / guaranteed elements (from the spec)

| Input | Value | Basis |
|---|---|---|
| Guaranteed minimum annual interest `i_guar` | 2.00% | pick from 2%–3% range [S1] [S2] [S3]; **[std]** |
| Guaranteed max COI rates `q_coi_guar(s)` per $1,000/month | specimen table by policy year s (spec, charges table) | [S3]; interpolation **[std]** |
| Guaranteed max premium load | 9% | [S1]; composite **[std]** |
| Per-policy charge (guaranteed = current) | $7.50/month to age 121 | [S3]; composite **[std]** |
| Per-unit charge | $0.26/$1,000/mo yrs 1–10; $0.156 to age 121 | [S3]; composite **[std]** |
| Surrender charge schedule | $9.00/$1,000 initial, linear monthly runoff, 0 from year 10 | pattern [S1] [S2], mechanics [S3], amount **[std]** |
| Corridor factors (GPT) | specimen table 250% (ages 0–40) → 101% (94+) | [S3] [R2] |
| Loan spread (charged − credited on loaned AV) | 0.75% | [S3]; level **[std]** |
| Grace | 61 days; required payment 3xMD + load | [S2] [S3] |
| Charges cease / premiums stop | attained age 121 | [S2] [S3] |

### (b) Current non-guaranteed scales (snapshot; revisable NGEs [R8])

| Input | Value | Basis |
|---|---|---|
| Current credited annual rate `i_cr` | 4.00% | **[std]** — current declared rates are not public; the one rates page attempted returned HTTP 403 [S5] |
| Current COI scale | 60% x guaranteed max, all durations | **[std]** — current COI scales are not public; only guaranteed maxima appear in the specimen [S3] |
| Current premium load | 6% | [S1]; composite **[std]** |
| Current per-policy charge | $7.50/month | [S3]; composite **[std]** |

NGE revision logic (optional module): under ASOP 2, scales are revised only on changes
in anticipated experience factors, with no recouping of past losses and prospective
profitability not materially greater than original [R8]. A simple reference rule:
`i_cr(t) = max(i_guar, earned_rate(t) − spread)` with a constant spread **[std]**;
the base projection holds the snapshot scales level.

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality | 2015 VBT (sex/smoker-distinct, ANB) x 100% A/E **[std]** factor; monitor against ILEC 2012–2019 A/E experience | [REG-R18] [REG-R19]; factor **[std]** |
| Mortality improvement | None in base **[std]** | — |
| Guaranteed-element mortality reference | 2017 CSO (cap for guaranteed COI; valuation/nonforfeiture basis for new issues) | [R4] [REG-R17]; COI-cap role [unverified — search-result context] |
| Base lapse/surrender | SOA/LIMRA UL studies (2015–2021 UL persistency & lapse; 2009–2013 all-product persistency); detailed tables are behind the paid package, so the reference table below is **[std]** | [R7] [REG-R21] [REG-R20] |
| Premium persistency | SOA/LIMRA 2015–2021 UL study: premium persistency (paid/planned) highest in year 1 (dump-ins); current-assumption products highest ongoing persistency | [R7]; reference factors **[std]** |
| Maintenance expense | $75/policy/year, inflating 2.5%/year | **[std]** |
| Premium tax / percent-of-premium expense | 2.5% of premium | **[std]** |

Reference base lapse table **[std]** (annual rates, all calibration to be replaced by
the user's experience; shape informed qualitatively by [R7] [REG-R20]):

| Policy year | 1 | 2 | 3–9 | 10 | 11+ |
|---|---|---|---|---|---|
| Annual lapse `w_base` | 6% | 5% | 4% | 4% x shock (below) | 3% |

Reference premium persistency factors `pp(y)` **[std]** (fraction of planned premium
actually paid, level-pay pattern): 100% in year 1, declining 2 percentage points per
year to a 70% floor (year 2: 98%, year 3: 96%, ..., floor from year 16).

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month index, t = 1, 2, ... (t=1 is the issue month); y = policy year = ceil(t/12); x = issue age; attained age = x + y − 1 (ANB) |
| `F` | total face amount (per policy) |
| `U` | units of face = F / 1000 |
| `GP(t)` | gross premium received at BOM of month t |
| `pl` | current premium load rate (0.06) |
| `NP(t)` | net premium = GP(t) x (1 − pl) |
| `W(t)` | partial withdrawal amount at BOM of month t (plus fee `wf` = $25 when W>0) |
| `e_pol` | per-policy charge ($7.50/month) |
| `e_unit(y)` | per-unit charge per $1,000/month (0.26 yrs 1–10; 0.156 yrs 11 to age 121; 0 after) |
| `rc(t)` | rider charges (0 in base model) |
| `q_coi(s)` | current monthly COI rate per $1,000 NAAR at policy year s = 0.60 x q_coi_guar(s) |
| `i_guar` | guaranteed annual effective rate (0.02) |
| `i_cr` | current credited annual effective rate (0.04) |
| `i_m` | monthly credited rate = (1 + i_cr)^(1/12) − 1 = 0.0032737 (derived) |
| `i_gm` | monthly guaranteed rate = (1 + i_guar)^(1/12) − 1 = 0.0016516 (derived) |
| `cf(a)` | GPT corridor factor at attained age a (spec table) [S3] [R2] |
| `AV'(t)` | AV after premium and withdrawal, before monthly deduction |
| `MD(t)` | monthly deduction |
| `NAAR(t)` | net amount at risk |
| `DB(t)` | death benefit after corridor test |
| `SC(t)` | surrender charge; `CSV(t) = AV(t) − SC(t)`; `NCSV(t) = CSV(t) − L(t)` |
| `L(t)` | loan balance; `r_L` charged loan rate (0.0275); loaned AV credited at i_guar |
| `q_m(t)` | best-estimate monthly mortality rate; `w_m(t)` monthly lapse rate |
| `l(t)` | in-force probability at end of month t; l(0) = 1 |

Dimensional check: `q_coi` is per $1,000 per month, so COI charge = q_coi/1000 x NAAR
is in currency; `e_unit x U` is currency; all MD components are currency/month.

### Monthly processing order (monthiversary, per the specimen [S3]; discretization [std])

At BOM of month t (skip steps 2–7 from attained age 121: charges cease, premiums not
accepted [S2] [S3]):

1. Set policy year y, attained age a. Amortize surrender charge:
   `SC(t) = max(0, (9.00 − t/12) x U)` (per-layer if face increases are modeled)
   **[std amount; mechanics [S3]]**.
2. Premium: `GP(t)` per the premium pattern and persistency assumption; check GPT
   guideline limit and 7-pay limit (compliance side-calculation — see below); deduct
   load; credit `NP(t)` to AV. (If L(t−1) > 0, unallocated payments repay the loan
   first unless designated premium [S3] — base model designates all as premium.)
3. Withdrawal: deduct `W(t) + wf`; apply free-amount rule (10% of AV per policy year
   **[std]**); under Option A reduce F if the withdrawal would otherwise increase
   NAAR beyond the free amount [S3].
   After steps 2–3: `AV'(t) = AV(t−1) + NP(t) − W(t) − wf x 1{W>0}`.
4. Death benefit and corridor:
   `DB(t) = max(optionDB(t), cf(a) x AV'(t))` where `optionDB = F` (Option A) or
   `F + AV'(t)` (Option B) [S1] [S3]; corridor per GPT [S3] [R2].
5. NAAR (specimen discounting convention — DB discounted one month at the guaranteed
   rate; AV measured before the deduction [S3]):
   `NAAR(t) = DB(t) / (1 + i_gm) − AV'(t)`, floored at 0.
   (The specimen states this as DB / NAAR-factor with factor 1.03^(1/12) = 1.0024663
   at its 3% guarantee [S3]; at the composite 2% guarantee the factor is
   1.02^(1/12) = 1.0016516, derived.)
6. Monthly deduction:
   `MD(t) = e_pol + e_unit(y) x U + rc(t) + q_coi(y)/1000 x NAAR(t)` [S3].
7. Shortfall test: if `AV'(t) − L(t−1) < MD(t)`, enter grace [S2] [S3] (see grace
   logic); otherwise deduct: AV after deduction = `AV'(t) − MD(t)`.
8. Interest (EOM): credit one month at the current rate on unloaned AV and at the
   guaranteed rate on the loaned portion; accrue loan interest at r_L **[std
   discretization of daily crediting [S3]]**:
   `AV(t) = (AV'(t) − MD(t) − L(t−1)) x (1 + i_m) + L(t−1) x (1 + i_gm)`
   `L(t) = L(t−1) x (1 + r_L)^(1/12)` (capitalized annually per contract [S3];
   monthly compounding **[std]**).
9. Decrements (EOM): deaths at `q_m(t)`, lapses/surrenders at `w_m(t)` applied to
   survivors; update `l(t) = l(t−1) x (1 − q_m(t)) x (1 − w_m(t))` **[std order:
   death before lapse]**.

With no loans and no withdrawals, steps 2–8 collapse to the core recursion:

    AV(t) = [ AV(t−1) + NP(t) − MD(t) ] x (1 + i_m)

with `NP(t) = GP(t) x (1 − pl)`, matching the contractual roll-forward in which the
policy-date AV equals net premium minus the first monthly deduction [S3].

### Grace and lapse-for-insufficiency logic

- Trigger (month t): `AV'(t) − L(t−1) < MD(t)` on a monthiversary [S2] [S3]. (Model 585
  default defines lapse at NCSV = 0 with >= 30-day grace [R1]; the composite follows
  the specimen trigger.)
- During grace (61 days ≈ 2 policy months **[std]**): coverage continues; deductions
  accrue as due-and-unpaid; if death occurs, claim = DB − L − overdue deductions [S3].
- Required cure payment: >= 3 x MD due plus premium load [S3]. In the deterministic
  base model, planned-premium payers are assumed to cure if `pp(y) x planned >= cure`
  **[std]**; otherwise the policy lapses at the end of the second month in grace with
  zero payment (terminates without value [S3]).
- Reinstatement is not modeled (contractual provision only [S3]) **[std scope]**.

### Cash flow outputs (per policy, month t, before survivorship weighting)

| Cash flow | Formula | Sign |
|---|---|---|
| Premium income | GP(t) | + |
| Death claims | DB(t) − L(t−1) − overdue deductions (in grace) [S3] | − |
| Surrender outgo | NCSV(t) = AV(t) − SC(t) − L(t) | − |
| Withdrawal outgo | W(t) (fee wf retained by insurer) | − |
| Maintenance expense | 75/12 x (1.025)^(y−1) **[std]** | − |
| Percent-of-premium expense | 0.025 x GP(t) **[std]** | − |
| Loan flows (optional) | new loans −, repayments + | +/− |

Aggregate expected cash flows multiply each row by the appropriate in-force factor:
premiums/expenses by l(t−1); death claims by l(t−1) x q_m(t); surrenders by
l(t−1) x (1 − q_m(t)) x w_m(t) **[std timing]**.

### MEC / 7-pay and guideline premium tests (compliance side-calculations)

The GPT limit (cumulative premiums less a portion of withdrawals may not exceed
max(GSP, cumulative GLP)) and the 7-pay MEC test are tracked as compliance
side-calculations that cap or refuse premiums [S3] [R2] [R3] [REG-R13] [REG-R14]; they
generate no cash flow of their own — a refused premium simply never enters the model,
and MEC status changes policyholder taxation, not insurer liability cash flows [R3
consequence detail [unverified] beyond the statutory cross-reference](#uslib-universal_life-r3). The base model
verifies `CumPrem(t) <= max(GSP, GLP x years elapsed)` and flags (does not project)
7-pay failures.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; calibration sources are
cited where they exist.

- **Premium patterns [std].** `level`: GP(t) = planned/12 x pp(y) each month (pp per
  the persistency table); `single`: one premium at issue capped at GSP, no further
  premiums; `target`: GP as level but capped so CumPrem stays within the GPT limit.
  Qualitative anchors: year-1 premium persistency is highest (dump-ins), and
  current-assumption products show the highest ongoing paid-to-planned ratios after
  early years [R7].
- **Base lapse [std].** Annual `w_base(y)` per the table above, converted monthly:
  `w_m = 1 − (1 − w_annual)^(1/12)`.
- **Surrender-charge-expiry shock [std].** During policy year 10 (the first year with
  SC = 0): `M_sc = 2.0`; else 1.0. Rationale: the surrender charge suppresses
  surrender while it is positive; its expiry is a known industry lapse-shock point
  (product-specific studies are proprietary; shape assumption).
- **Interest-sensitive (dynamic) lapse [std].**
  `M_rate(t) = min(3.0, 1 + 5 x max(0, r_comp(t) − i_cr(t) − 0.01))`
  where `r_comp` is a competitor/market new-money rate input. Base deterministic run:
  `r_comp = i_cr`, so M_rate = 1.
- **Total lapse.** `w_annual(y,t) = min(0.35, w_base(y) x M_sc(y) x M_rate(t))`
  **[std cap]**.
- **Premium suspension [std].** Implicit in pp(y) < 1; no separate paid-up state is
  modeled.

---

## Worked example

Anchor cell: Male 35 Standard NT, F = $100,000 (U = 100), Option A, GPT; GP = $150/mo;
pl = 6% → NP = $141.00; e_pol = $7.50; e_unit = 0.26 → $26.00/mo; guaranteed COI year
1 = 0.10090 [S3], current = 60% → q_coi = 0.060540 per $1,000/mo **[std]**;
i_m = 0.0032737 (from i_cr = 4.00% **[std]**); 1 + i_gm = 1.0016516 (from i_guar =
2.00% **[std]**); DB/(1+i_gm) = 100,000 x 0.9983511 = 99,835.11; corridor 250% x AV'
never binds at these AV levels [S3]. No withdrawals or loans. All figures in dollars,
rounded to cents for display (full precision carried).

| Month t | AV(t−1) | NP | AV' | DB | NAAR = 99,835.11 − AV' | COI = 0.06054xNAAR/1000 | MD = 7.50+26.00+COI | AV'−MD | Interest (x i_m) | AV(t) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 141.00 | 141.00 | 100,000 | 99,694.11 | 6.04 | 39.54 | 101.46 | 0.33 | 101.80 |
| 2 | 101.80 | 141.00 | 242.80 | 100,000 | 99,592.32 | 6.03 | 39.53 | 203.27 | 0.67 | 203.93 |
| 3 | 203.93 | 141.00 | 344.93 | 100,000 | 99,490.18 | 6.02 | 39.52 | 305.41 | 1.00 | 306.41 |

Trace, month 1: AV' = 0 + 141.00; corridor min = 2.50 x 141.00 = 352.50 < 100,000 so
DB = 100,000; NAAR = 99,835.11 − 141.00 = 99,694.11; COI = 0.060540/1000 x 99,694.11
= 6.0355 (displayed 6.04); MD = 7.50 + 26.00 + 6.0355 = 39.5355 (displayed 39.54);
AV(1) = (141.00 − 39.5355) x 1.0032737 = 101.80. Month-1 shortfall test: AV' (141.00)
>= MD (39.54), no grace. This reproduces
the contractual policy-date rule AV = net premium − first monthly deduction [S3],
followed by one month's interest.

---

## Valuation and reserve pointers

This library projects gross liability cash flows; reserve layers consume them and are
NOT reproduced here:

- **Statutory (pre-PBR / formulaic).** The UL CRVM adaptation as printed at AP&P
  Appendix **A-585**: Guaranteed Maturity Premium / Guaranteed Maturity Fund
  construction, the funding ratio — `r = min(1, policy value/GMF)` here **only because
  this chassis is flexible premium**, `r ≡ 1` unconditionally for a fixed premium UL —
  and the ¶¶12–13 alternative minimum reserve, with every rate, table and factor
  delegated to A-820 by year of issue [REG-R155 ¶¶8, 12–13](#uslib-reg-r155) [REG-R153]. Nonforfeiture
  floor: **Model 585 Section 6A** retrospective minimum CSV — A-585 carries no
  nonforfeiture provisions at all, so that floor stays with the model regulation
  [R1] [REG-R5] [REG-R155].
- **Statutory (PBR).** VM-20 minimum reserve for life products (net premium reserve
  plus deterministic/stochastic excess subject to exclusion tests), per the Valuation
  Manual (operative 2017-01-01; accreditation standard 2020-01-01 — both verbatim at
  [R5], now also the shared [REG-R150]) [REG-R3];
  implementation guidance in the AAA VM-20 practice note [REG-R23]. Prescribed NPR
  mortality: 2017 CSO family via VM-M [REG-R3] [REG-R17; exact table mapping
  [unverified]](#uslib-reg-r17).
- **Tax.** IRC 807: greater of net surrender value and 92.81% of the NAIC-method
  reserve, capped at statutory [REG-R16].
- **Standards for the modeling work itself.** ASOP 7 (life cash flow analysis)
  [REG-R27]; ASOP 52 (PBR reserves) [REG-R31]; ASOP 56 (modeling: validation,
  documentation, model risk) [REG-R32]; NGE determination under ASOP 2 [R8].

---

## Key sensitivities and model risks

Dominant assumptions (in rough order for a cash-value-oriented block):

1. **Credited-rate spread and current COI scale (the NGE pair).** They set the AV
   growth net of charges and hence funding adequacy, surrender values, and the
   grace/lapse cascade. Both are [std] snapshots here because insurers do not publish
   them [S3] [S5]; sensitivity-test the 60% COI factor and the 4.00% credited rate
   first.
2. **Premium persistency.** UL cash flows are premium-behavior-driven; paid/planned
   ratios vary by product focus and duration [R7]. Underfunding accelerates
   shortfall-driven lapse; dump-ins interact with GPT/7-pay limits.
3. **Lapse/surrender, especially at surrender-charge expiry.** Current-assumption UL
   charge structures can be lapse-supported; the year-10 shock multiplier materially
   moves the value of later-duration COI margins.
4. **Mortality at high attained ages.** COI rates grade to 1000/12 at ages 112–120
   and to zero at 121+ while coverage continues [S3]; late-age mortality assumptions
   drive the cost of the post-121 charge-free period.

Known modeling pitfalls:

- **Deduction/interest ordering.** The recursion applies interest to the
  post-deduction balance; reversing the order overstates AV by roughly one month's
  interest on MD each month and compounds over decades.
- **NAAR convention.** The specimen discounts DB one month at the *guaranteed* rate
  and measures AV *before* the deduction [S3]. Using the current rate in the
  discount, or AV after deduction (which makes COI implicit and requires iteration),
  produces small but systematic COI errors.
- **Corridor circularity under Option B.** DB depends on AV' and NAAR depends on DB;
  with the BOM ordering above there is no simultaneity, but corridor-active cells
  (heavily funded, older ages) are sensitive to where in the order AV is measured.
- **Daily-vs-monthly interest.** The contract credits daily on a 365-day year [S3];
  monthly discretization is a [std] approximation — do not also compound daily, and
  document the convention when reconciling to admin-system values.
- **ANB vs ALB mismatch.** Mortality/corridor lookups must match the [std] ANB basis;
  the 2017 CSO/2015 VBT families ship both variants [R4] [REG-R18].
- **Era mixing.** The guaranteed COI table is a 2001 CSO-era specimen table [S3]
  paired here with a 2%-guarantee-era interest assumption **[std]**; a production
  model for post-2020 issues should substitute a 2017 CSO-capped guaranteed table
  (not publicly obtained — research gap) [R4] [unverified].
- **Grace-period timing.** The 61-day grace spans two monthiversaries; skipping the
  due-and-unpaid deduction accrual understates death claims in grace [S3].
- **MEC/GPT are not cash flows.** Modeling them as charges or refunds distorts
  premium income; they are caps/flags only [S3] [R2] [R3].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-universal_life-r1
[R2]: #uslib-universal_life-r2
[R3]: #uslib-universal_life-r3
[R4]: #uslib-universal_life-r4
[R5]: #uslib-universal_life-r5
[R7]: #uslib-universal_life-r7
[R8]: #uslib-universal_life-r8
[REG-R13]: #uslib-reg-r13
[REG-R14]: #uslib-reg-r14
[REG-R150]: #uslib-reg-r150
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R155]: #uslib-reg-r155
[REG-R16]: #uslib-reg-r16
[REG-R17]: #uslib-reg-r17
[REG-R18]: #uslib-reg-r18
[REG-R19]: #uslib-reg-r19
[REG-R20]: #uslib-reg-r20
[REG-R21]: #uslib-reg-r21
[REG-R23]: #uslib-reg-r23
[REG-R27]: #uslib-reg-r27
[REG-R3]: #uslib-reg-r3
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[REG-R5]: #uslib-reg-r5
[S1]: #uslib-universal_life-s1
[S2]: #uslib-universal_life-s2
[S3]: #uslib-universal_life-s3
[S5]: #uslib-universal_life-s5
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
