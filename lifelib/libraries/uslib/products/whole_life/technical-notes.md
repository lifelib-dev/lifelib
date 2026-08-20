# Technical Notes

**Status:** Draft, 2026-08-03 (underlying research accessed 2026-08-03).

Scope note: these notes specify a reference liability cash flow projection model
(lifelib/modelx style) for the standardized composite products defined in `product-spec.md`
("RefWL-Par" participating whole life; "RefWL-FE" non-par final-expense whole life). They do
not describe any single insurer's model. [S#]/[R#] tags cite the product research file
(`_research/whole-life.md`); [REG-R#] tags cite the cross-product reference library
(`references/regulatory-and-actuarial-references.md`; research provenance in
`_research/regulatory-actuarial.md`, same R-numbering). **[std]** marks standardizations introduced for the
reference implementation. Parameter values are identical to those in `product-spec.md`.

---

## Model scope and conventions

- **Projection frequency: annual**, on policy years (anniversary to anniversary) **[std]**.
  Rationale: the contract's cash flow drivers — level annual premium, annual dividend
  declaration, anniversary loan-interest capitalization [S1] — are all annual. No
  monthiversary processing is performed; monthly modal premiums would enter only as a
  premium-income refinement via modal factors [S1] and are excluded by the annual-mode
  standardization (product-spec Table 2 note (f)).
- **Timing conventions [std]:** premiums and premium-linked expenses at the beginning of the
  policy year (BOY); death claims, dividends, surrenders, and maturity at the end of the
  policy year (EOY), in the processing order given below. State variables are stored at EOY
  (= policy anniversary t).
- **Age basis: age nearest birthday (ANB)** **[std]** (product-spec Table 1 note (a)); the
  2017 CSO set provides ANB tables [R8]. Attained age at anniversary t is `x + t`.
- **Projection horizon:** to the anniversary at attained age 100, where the model pays a
  maturity benefit and terminates **[std]**. The contract itself matures at 121 [S1], but the
  guaranteed CV equals face at 100 and PUA CV equals PUA face at 100 [S1] [S3], so from age 100
  the policy is economically an endowment at face; truncating at 100 changes only the timing
  of the terminal payment between ages 100–121 (mortality vs. maturity), not its amount per
  survivor.
- **Model points:** single-policy model points, projected seriatim; results scale linearly in
  face within a band-free specification **[std]**. Amounts are U.S. dollars per policy;
  probabilities are per policy year.
- **Decrement model:** annual rates; deaths before surrenders at EOY; dividends credited to
  policies in force at EOY before surrender processing **[std]** (order list below).
- **Sex-distinct** rates throughout (unisex only as a variant) [S1] [S3].

## Model point attributes

| Attribute | Type | Example |
|---|---|---|
| `policy_id` | str | "WLPAR-000001" |
| `product` | enum {WL_PAR, WL_FE_LEVEL, WL_FE_GRADED} | WL_PAR |
| `premium_period` | enum {TO_100, PAY_10, PAY_20, TO_65} | TO_100 **[std]** (product-spec Table 1 note (b); menu [S1] [S3]) |
| `issue_age` (x) | int | 45 |
| `sex` | enum {M, F} | M |
| `risk_class` | enum {PREF_NT, STD_NT, TOB} **[std]** | STD_NT |
| `face_amount` (F) | float | 100,000 **[std]** |
| `annual_premium` (G) | float | 1,800.00 **[std illustrative]** (product-spec Table 2 note (c)) |
| `dividend_option` | enum {CASH, REDUCE_PREM, ACCUM, PUA} | PUA (default [S1] [S2]) |
| `pua_rider_premium` (A_t) | float per year | 0.00 |
| `term_blend_target` | float (0 = off) | 0.00 (variant: 2 × F **[std]**) |
| `loan_utilization` | float in [0,1] | 0.00 (variant: 0.20 **[std]**) |
| `duration_inforce` (t0) | int (0 for new business) | 0 |
| `puaf_inforce` | float (PUA face at t0) | 0.00 |
| `loan_inforce` | float | 0.00 |

## State variables

| Variable | Meaning | Initialization |
|---|---|---|
| `l_t` | Probability in force at anniversary t (per issued policy) | `l_0 = 1` |
| `CV_t` | Guaranteed cash value per policy (base), EOY t | table input; `CV_{100−x} = F` [S1] [S3] |
| `PUAF_t` | Paid-up additions face in force, EOY t | `PUAF_0 = puaf_inforce` |
| `PUACV_t` | PUA cash value, EOY t | `PUAF_t · NSP_{x+t}` **[std]** |
| `DA_t` | Dividend accumulation balance (ACCUM option only) | 0 |
| `L_t` | Loan balance incl. capitalized interest, EOY t | `L_0 = loan_inforce` |
| `DB_t` | Death benefit payable on death in year t | formula below |
| `D_t` | Dividend credited at EOY t | recursion below |

## Assumption inputs

The model distinguishes three assumption classes. Keeping them in separate input structures is
deliberate: (a) is locked by contract, (b) is an insurer-declared snapshot that re-rates
annually, (c) is the modeler's experience basis.

### (a) Contractual / guaranteed elements (from the product spec)

| Input | Value | Basis |
|---|---|---|
| Guarantee interest `i_g` | 4.00% | [S1]; Model 808 floor [R1] |
| Guarantee mortality `q^g_{x+t}` | 2017 CSO composite, sex-distinct, ANB | [S1] [R3] [R8]; ANB **[std]** |
| Guaranteed CV schedule `CV_t` | Table input per model point (generated on the above basis) | [S1] [R1]; see below |
| Gross premium `G` | Model point input (level, guaranteed) | [S1] [S3] |
| Loan rate `i_L` | 6.00% fixed, in arrears | [S1] |
| Endowment/maturity | `CV = F` at age 100; model maturity at 100 | [S1] [S3]; truncation **[std]** |
| FE premium rates | Per $1,000 rate table + $36 fee | [S7] |
| FE graded DB | 110% of premiums paid, natural death in years 1–2 | [S6] [S7] |

### (b) Current non-guaranteed scale (insurer-declared; snapshot)

| Input | Value | Basis |
|---|---|---|
| Dividend interest rate `i_d` | 6.00% (2026-scale snapshot) | **[std]**, within observed 5.75%–6.60% [S4] [S14] |
| Experience mortality in scale `q^{sc}_{x+t}` | `AE^{sc} · q^{2015VBT}_{x+t}` with `AE^{sc} = 0.70` of 2017 CSO in the worked example | **[std illustrative]**; structure per [S4] [R6], tables [REG-R18] |
| Expense margin in scale `e^{m}_t` | $25 per policy per year | **[std]** |
| Dividend floor | `D_t ≥ 0` | **[std]** (dividends are non-negative distributions of surplus [R6]) |
| PUA purchase basis | `NSP_{x+t}` on 2017 CSO / 4%, unloaded (dividend purchases); 10% load on rider payments | **[std]** / [S3] (product-spec Table 3 note (k), Riders) |
| Accumulation option credit rate | `i_d` | [S2] rate declared annually; reuse of DIR **[std]** |

Non-guaranteed scales are constrained in illustration use by the disciplined-current-scale and
self-support / lapse-support machinery of Model 582 [R2] and ASOP 24 [REG-R30]; the model's
"current scale" should be interpreted as a currently-payable-scale snapshot, not a projection
of future scale changes.

### (c) Behavioral / experience assumptions (modeler-set; recommended public bases)

| Input | Recommended base | Reference value |
|---|---|---|
| Best-estimate mortality `q^e_{x+t}` | 2015 VBT (sex/smoker-distinct, ANB) × company A/E; industry A/E from the ILEC 2012–2019 study | tables [REG-R18], experience [R9]/[REG-R19]; A/E factor 0.70 × 2017 CSO in the worked example **[std illustrative]** |
| Base lapse `w_t` | LIMRA/SOA U.S. Individual Life Persistency study (WL by duration/size/mode) | [REG-R20] for the study; rates below **[std]** (study figures not recorded in the research file) |
| Lapse schedule **[std]** | 5.0% year 1, grading linearly to 2.0% at year 10, level 2.0% thereafter; 0 within 1 year of maturity | **[std]** — "low and level" pattern consistent with mature par WL persistency; source study [REG-R20] |
| Premium persistency | 1 (premiums are fixed and guaranteed; premium cessation = lapse/RPU) | [S1] [S3]; convention **[std]** |
| Maintenance expense | $60 per policy per year, inflating 2.0%/yr | **[std]** |
| Acquisition expense | 90% of first-year premium + $250 per policy | **[std]** |
| Premium tax | 2.0% of premium | **[std]** |
| Loan utilization | 0% base; 20% of CV variant | **[std]** |

All experience values marked **[std]** are reference placeholders: no carrier experience data
is public in the research base; assumption governance patterns are per the Academy's PBR
Assumptions Resource Manual [REG-R25] and ASOP 56 model governance [REG-R32].

## Cash flow components and recursions

### Notation (defined once, used throughout)

```
x           issue age (ANB)                     t   policy year, t = 1 … 100 − x
F           base face amount                    G   gross annual premium
i_g         guaranteed interest (4.00%)         i_d dividend interest rate (6.00%)
i_L         policy loan rate (6.00%)            v_g = 1 / (1 + i_g)
q^g_{y}     2017 CSO rate at attained age y     q^e_{y}  best-estimate rate at age y
w_t         lapse rate in policy year t         l_t  in-force probability at EOY t
CV_t        guaranteed cash value (base), EOY t
NSP_y       net single premium per 1 of paid-up (endow-at-100) WL face at age y,
            on 2017 CSO / 4%:  NSP_y = A_{y:(100−y)|}  (endowment insurance to 100)
ä_{y:n|}    annuity-due, n years, on 2017 CSO / 4%
D_t         dividend credited at EOY t          PUAF_t, PUACV_t  PUA face / cash value
DA_t        dividend accumulation balance       L_t  loan balance at EOY t
DB_t        death benefit for deaths in year t  E_t  expense outgo in year t
```

### Guaranteed cash value: conceptual formula and practical treatment

Conceptual (Standard Nonforfeiture Law minimum, adjusted-premium / nonforfeiture-net-level-
premium method) [R1]:

```
NNLP      = F · NSP_x / ä_{x:(100−x)|}                       (net level premium, NF basis)
EA        = 0.01 · F + 1.25 · min(NNLP, 0.04 · F)            (expense allowance)  [R1]
P_adj     such that  P_adj · ä_{x:m|} = F · NSP_x + EA       (m = premium period)  [R1]
CV_t^min  = F · NSP_{x+t} − P_adj · ä_{x+t:(m−t)|}           (t < m; second term 0 for t ≥ m)
```

on 2017 CSO / 4% [S1] [R1] [R3]. Properties to verify: `CV_{100−x}^min = F` (since
`NSP_100 = 1`), and smooth progression by duration [R1].

Practical treatment **[std]**: the reference implementation reads `CV_t` (per $1,000 of face)
from a table input, because contractual CV tables are policy-form documents not publicly
available for the surveyed carriers (research gap noted in `_research/whole-life.md`). The
shipped table is generated from the formula above; an implementer replacing it with a carrier
table changes no other logic. Contractual `CV_t ≥ CV_t^min` always [R1].

### Dividend recursion (three-factor contribution formula)

Anchor (published mechanics of one surveyed carrier) [S4]:

```
D_t = ( CV_{t−1} + G − MEC_t ) · (1 + i_d) − CV_t
```

where `MEC_t` is the mortality-and-expense charge based on actual company results — i.e., the
dividend is the excess of an experience-basis accumulated value over the guaranteed value [S4].

Reference parametrization **[std]** (exact carrier factor formulas are proprietary; this is the
classic three-factor contribution decomposition consistent with [S4] and the contribution
principle [R6]):

```
D_t = D^int_t + D^mort_t + D^exp_t ,   floored at 0
D^int_t  = (i_d − i_g) · (CV_{t−1} + NP_g)                       (interest margin)
D^mort_t = (q^g_{x+t−1} − q^{sc}_{x+t−1}) · (F − CV_t)           (mortality margin)
D^exp_t  = e^m_t                                                  (expense margin)
```

with `NP_g = NNLP` (the nonforfeiture net level premium, so the interest margin applies to the
guaranteed fund including the year's net premium) **[std]**, `q^{sc}` the scale's experience
mortality (class (b)), and `e^m_t` the per-policy expense margin (class (b)). Dimensions: every
term is dollars per policy per year. Refinements observed in practice — interest on the
mortality margin, premium-timing adjustments, banded factors [S1] [S3] — are absorbed into the
calibration of `q^{sc}` and `e^m_t` **[std]**.

Dividends on the PUA block (PUAs are dividend-eligible [S14]) **[std]**:

```
D^PUA_t = (i_d − i_g) · PUACV_{t−1} + (q^g_{x+t−1} − q^{sc}_{x+t−1}) · (PUAF_{t−1} − PUACV_{t−1})
```

No dividend is credited for policy year 1 (`D_1 = D^PUA_1 = 0`) **[std]** (product-spec Table
3 note (j); one carrier pays none [S1], another pays a first-year dividend [S3]).

Direct recognition (loaned values) **[std]** parametrization of [S1] [S3]: replace `i_d` with
`i_L` on the loaned portion:

```
D^int_t (adjusted) = (i_d − i_g) · (CV_{t−1} + NP_g − L_{t−1}) + (i_L − i_g) · L_{t−1}
```

With `i_L = 6.00%` [S1] and the snapshot `i_d = 6.00%` **[std]** the adjustment is zero — a
coincidence of the snapshot, not a model property.

### Dividend application (by option)

- **PUA (default [S1] [S2]):** `ΔPUAF_t = (D_t + D^PUA_t) / NSP_{x+t}`; `PUAF_t = PUAF_{t−1} +
  ΔPUAF_t`; `PUACV_t = PUAF_t · NSP_{x+t}` **[std]** (valuing all PUA face at the attained-age
  NSP on the guarantee basis; exact at issue of each layer and at age 100, approximate between
  **[std]**). At age 100, `NSP_100 = 1` so `PUACV = PUAF` [S1].
- **CASH:** dividend paid out; policyholder cash flow at EOY.
- **REDUCE_PREM:** offsets next year's BOY premium: `G^{net}_{t+1} = max(G − D_t, 0)`, excess
  to PUAs **[std]** (excess-to-PUA per one carrier's reduce-premium option [S3]).
- **ACCUM:** `DA_t = DA_{t−1} · (1 + i_d) + D_t`; balance adds to death and surrender
  proceeds [S1] [S2].

### PUA rider (in-scope rider)

Rider payment `A_t` (BOY, within limits set at issue [S3] [S11]):
`ΔPUAF^rider_t = A_t · (1 − 0.10) / NSP_{x+t−1}` — 10% load **[std]** from the observed
7.5%–10% range [S3]. Rider PUAs merge into `PUAF_t`.

### Term-blend rider (in-scope rider, simplified **[std]**)

Target face `TF = 2 F` **[std]** (within observed caps: ≤ 9× base [S2], ≤ 300% of base [S3]).
Each year, OYT face `= max(TF − F − PUAF_t, 0)`; the dividend first pays the OYT cost
`q^{sc}_{x+t} · OYT_t · v_g` **[std]**, remainder buys PUAs; crossover when `PUAF_t ≥ TF − F`,
after which the rider is pure PUA [S2] [S3] [S11]. Death benefit while blended: `TF + excess
PUAs − L_t`.

### Benefit amounts

```
DB_t   = F + PUAF_{t−1} + DA_{t−1} − L_{t−1}                 (PUA/ACCUM components as elected)
CSV_t  = CV_t + PUACV_t + DA_t − L_t                          (surrender value, EOY t)
MAT    = F + PUAF_T + DA_T − L_T   at T = 100 − x             (model maturity [std])
```

`DB` per the contractual formula [S1], reduced to modeled components **[std]**. Deaths in year
t are assumed to occur at EOY before the year-t dividend is credited, so `DB_t` carries the
prior year's PUA face **[std]** (terminal-dividend and premium-refund items not modeled,
product-spec Table 3 note (m)).

### Annual processing order (policy year t, per unit in force `l_{t−1}`)

1. **BOY:** collect gross premium `G` (if `t ≤` premium period) and PUA rider premium `A_t`;
   pay premium tax and acquisition/maintenance expense `E_t`.
2. **BOY:** apply REDUCE_PREM offset from `D_{t−1}` if elected.
3. **During year:** interest accrues implicitly (CV table on `i_g` [S1]; loan at `i_L` [S1]).
4. **EOY — deaths:** probability `q^e_{x+t−1}`; outgo `q^e_{x+t−1} · l_{t−1} · DB_t`.
5. **EOY — loan interest capitalization:** `L_t = L_{t−1} · (1 + i_L)` less repayments [S1].
6. **EOY — dividend:** credit `D_t + D^PUA_t` to survivors (from t = 2 **[std]**); apply per
   dividend option; update `PUAF_t, PUACV_t, DA_t`.
7. **EOY — surrenders:** probability `w_t` applied to survivors
   `l_{t−1} · (1 − q^e_{x+t−1})`; outgo `= CSV_t` per surrendering policy.
8. **Update in force:** `l_t = l_{t−1} · (1 − q^e_{x+t−1}) · (1 − w_t)`.
9. **At T = 100 − x:** pay `MAT · l_T`; terminate **[std]**.

Ordering (deaths → dividend → surrenders at EOY) is **[std]**; it makes surrender values
include the just-credited dividend, consistent with anniversary processing.

### Net liability cash flow (per issued policy, year t)

```
NetCF_t = − G^{net}_t · l_{t−1} − A_t · l_{t−1} + E_t · l_{t−1}          (BOY items, sign: outgo +)
          + q^e · l_{t−1} · DB_t + w_t · l_{t−1}(1 − q^e) · CSV_t        (EOY benefits)
          + D^{cash}_t · l_{t−1}(1 − q^e) + MAT · l_T · 1{t=T}           (cash dividends, maturity)
```

Internal dividend applications (PUA, ACCUM, REDUCE_PREM) are not cash flows when credited;
they emerge later through `DB`, `CSV`, and `MAT` **[std]**. Loans are modeled on the offset
view: see next.

### Loans (offset treatment — brief)

Base run: `loan_utilization = 0`. Variant **[std]**: `L_t = 0.20 · CV_t` maintained by
borrowing/repaying at EOY; borrowed amounts are policyholder cash outflows from the insurer,
loan interest received is an inflow, and `DB`/`CSV`/`MAT` are net of `L_t` [S1] [S3] [S9]. Under
direct recognition the dividend adjustment above applies [S1] [S3]. Economically the loan is an
offsetting asset; the reference model reports gross liability flows plus a separate loan
account rather than netting into a "net amount at risk" presentation **[std]**.

### RefWL-FE variant deltas

- Premium: `G = (F/1000) · rate(x, sex, tobacco) + 36` [S7]; no dividends (non-par
  [unverified]; modeled non-par).
- Graded plan: for natural-cause deaths in years 1–2, `DB_t = 1.10 · (cumulative premiums
  paid)`; accidental deaths pay `F` from day 1 [S6] [S7]. Accidental split requires an
  accidental-death fraction of `q^e` **[std]** (reference value 3% of deaths **[std]**).
- Maturity at age 100 (120 in FL — not modeled **[std]**) pays `F − L_T` [S8].
- CV schedule: reuse of the par nonforfeiture machinery **[std]** (product-spec Table 5 note (r)).
- Lapse: FE simplified-issue business lapses higher than par WL; reference schedule 12% year 1,
  10% year 2, grading to 6% level by year 5 **[std]** (no FE-specific study in the research
  base; flagged as an open issue).

## Policyholder behavior modeling

Base behavior is static (schedules in class (c)). Dynamic overlays, all **[std]**:

- **Interest-sensitive lapse multiplier** (for scenario runs):
  `w_t^dyn = w_t · min(1 + 2.0 · max(0, r^{cmp}_t − i_d − 0.01), 3.0)` where `r^{cmp}_t` is
  the competitor/market rate in the scenario. Rationale: par WL cash values are liquid at book
  value, so sustained rate spreads induce excess surrender; the low base level reflects the
  strong persistency of dividend-paying WL. Calibration is judgmental **[std]** — the research
  base records no dynamic-lapse study for WL.
- **Premium offset behavior:** once `D_t ≥ G` (dividend covers the premium), a fraction
  `0.50` **[std]** of policyholders switch to REDUCE_PREM/premium-offset behavior (offset is a
  real product feature: a lettered dividend option at one carrier [S2]; a named automatic
  offset option at another [S3]). This shifts premium income to internal dividend application
  in later durations.
- **Loan utilization:** static 0%/20% variants only **[std]**; no dynamic loan take-up (the
  6%-fixed direct-recognition design largely neutralizes loan arbitrage [S1] [S3]).
- **No dynamic mortality (anti-selection) on lapse** for the base par product **[std]**;
  selective-lapse mortality loading is documented mainly for term post-level-period designs
  (see the SOA persistency/PLT study family around [REG-R20]), not level-premium par WL.

## Worked example

Single-year walk-through of the core recursion: RefWL-Par, male Standard NT, `x = 45`,
`F = 100,000` **[std]**, `G = 1,800` **[std illustrative]**, PUA dividend option, no rider, no
loan. Policy year `t = 10` (attained age 55 at EOY). All table values are illustrative
**[std]** (the shipped CV/NSP tables are generated on 2017 CSO / 4% as specified above);
`i_g = 4.00%` [S1], `i_d = 6.00%` **[std]**.

| Step | Item | Formula | Value |
|---|---|---|---|
| 1 | Guaranteed CV, BOY (EOY 9) | `CV_9` (table) | 9,500.00 **[std]** |
| 2 | Guaranteed CV, EOY | `CV_10` (table) | 11,200.00 **[std]** |
| 3 | Net level premium (NF basis) | `NP_g` | 1,300.00 **[std]** |
| 4 | Guarantee mortality, age 54 | `q^g_54` | 0.00320 **[std]** |
| 5 | Scale mortality, age 54 | `q^{sc}_54 = 0.70 · q^g_54` | 0.00224 **[std]** |
| 6 | Interest margin | `(0.06 − 0.04) · (9,500 + 1,300)` | 216.00 |
| 7 | Mortality margin | `(0.00320 − 0.00224) · (100,000 − 11,200)` | 85.25 |
| 8 | Expense margin | `e^m_10` | 25.00 **[std]** |
| 9 | Dividend | `D_10 = 216.00 + 85.25 + 25.00` | 326.25 |
| 10 | NSP at age 55 | `NSP_55` (table) | 0.42 **[std]** |
| 11 | PUA face purchased | `ΔPUAF = 326.25 / 0.42` | 776.79 |
| 12 | PUA face, EOY (prior 4,100.00 **[std]**) | `PUAF_10 = 4,100.00 + 776.79` | 4,876.79 |
| 13 | PUA cash value, EOY | `PUACV_10 = 4,876.79 × 0.42` | 2,048.25 |
| 14 | Death benefit for year 11 deaths | `F + PUAF_10` | 104,876.79 |
| 15 | Surrender value, EOY 10 | `CV_10 + PUACV_10` | 13,248.25 |

(For clarity the PUA-block dividend `D^PUA_10` is omitted from this table; in the model it
adds `(0.02 · PUACV_9) + (0.00096 · (PUAF_9 − PUACV_9))` to the amount in step 9 **[std]**.)

## Valuation and reserve pointers (brief)

This library projects **gross liability cash flows**; statutory, tax, and GAAP measurement are
separate layers, cited not reproduced:

- **Statutory:** Standard Valuation Law root [REG-R1], codified in the AP&P Manual as **Appendix
  A-820** and now read in full — ¶11 CRVM, ¶¶7–10 the valuation interest rate, ¶16 the aggregate
  nonforfeiture floor, ¶¶19–20 deficiency reserves, ¶¶24 and 27 the formulaic/PBR boundary
  [REG-R153]; **A-830** likewise [REG-R154], though ¶3.b routes no calculation paragraph to a
  level-premium level-benefit whole life. Both were "not retrieved" behind the VM-A index entry
  [REG-R110] and no longer are. For issues on/after 2020-01-01 — a date that is the PBR
  *accreditation* year, the statutory-law trigger A-820 ¶¶3–4 prints being **1 January 2017** —
  VM-20 minimum reserve = f(net premium reserve, deterministic reserve,
  stochastic reserve) with exclusion tests; seriatim NPR on 2017 CSO; traditional par WL typically
  passes the deterministic exclusion test (valuation net premiums ≤ guaranteed gross premiums) and
  many WL blocks hold NPR only [R3]. Small companies under the Life PBR Exemption (< $300M) value
  under VM-A/VM-C (pre-PBR CRVM) [R3]. ASOP 52 governs the actuary's PBR work [REG-R31].
- **Tax:** IRC §807 — greater of net surrender value and 92.81% of the CRVM/VM reserve,
  capped at statutory [REG-R16]; the statutory engine plus a haircut/cap wrapper.
- **GAAP:** LDTI (ASU 2018-12) rewrites long-duration GAAP (annually updated cash flow
  assumptions, single-A discounting through OCI) [REG-R34 — not fetched; characterization
  corroborated only by secondary summaries](#uslib-reg-r34). Same projected cash flows, different measurement
  overlay — the reason projection and measurement are separated in this library.
- **Model governance:** ASOP 56 (modeling) [REG-R32] and, for cash-flow analysis engagements,
  ASOP 7 [REG-R27 — listed in the regulatory bibliography](#uslib-reg-r27) frame validation/documentation
  expectations for the implementation itself.

## Key sensitivities and model risks

Dominant assumptions (in typical order of impact on par WL liability value):

1. **Dividend scale vs. guarantee spread** (`i_d − i_g`, mortality margin, expense margin):
   drives dividends, hence PUA growth, hence death benefit and surrender value trajectories —
   compounding because PUAs themselves earn dividends [S14]. The DIR snapshot is a declared,
   changeable rate (observed 5.75%–6.60% for 2026 alone [S4] [S14]); scale-change dynamics are
   a scenario input, not a model constant.
2. **Best-estimate mortality** (level and improvement vs. 2015 VBT [REG-R18], A/E per ILEC
   [R9]): sets both claim outgo and the mortality margin of the dividend; note the same table
   family feeds two places with opposite signs — a consistency trap.
3. **Lapse:** low and level for par WL, but long-duration liabilities are convex in lapse;
   illustration regulation exists precisely because lapse-supported scales misstate value
   [R2]. Verify the model is not inadvertently lapse-supported when testing dividend scales.
4. **Expense inflation** on per-policy maintenance for a product with 55+-year horizons.
5. **Loan utilization** under direct recognition [S1] [S3]: shifts dividend composition and
   net cash flow timing; the fixed-6%/DIR-6% snapshot coincidence (zero adjustment) will not
   survive a scale change.

Known modeling pitfalls:

- **CV-table vs. first-principles mismatch:** if the CV table input and the `NSP`/annuity
  functions come from different bases, `PUACV ≠ PUAF` at age 100 and the dividend recursion
  leaks. Regenerate all guarantee-basis quantities from one 2017 CSO / 4% source [S1] [R1] [R8].
- **Dividend floor and negative margins:** with `D_t` floored at 0 **[std]**, adverse
  experience does not claw back — asymmetry matters in stochastic runs.
- **First-dividend timing** (year 1 vs 2) shifts early-duration PUA compounding; it is a real
  cross-carrier difference [S1] [S3], keep it a parameter.
- **MEC administration on limited-pay variants:** 10-pay premiums approach 7-pay limits; face
  decreases can retroactively create MECs and PUA-rider payments consume 7-pay room
  [R5] [S3] [S1]. The reference model does not police §7702/§7702A limits [R4] [R5] — flag
  model points that would fail rather than silently projecting them **[std]**.
- **Truncation at age 100** **[std]** is exact for surrender/maturity amounts but reallocates
  age-100–121 payments from death to maturity; do not use the truncated model for
  mortality-timing-sensitive measures beyond age 100 [S1].
- **State variations** (FL maturity 120, WA face minimums, ND suicide, MT unisex)
  [S6] [S7] [S8] [S1] are not modeled; the reference is a generic-state contract **[std]**.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-whole_life-r1
[R2]: #uslib-whole_life-r2
[R3]: #uslib-whole_life-r3
[R4]: #uslib-whole_life-r4
[R5]: #uslib-whole_life-r5
[R6]: #uslib-whole_life-r6
[R8]: #uslib-whole_life-r8
[R9]: #uslib-whole_life-r9
[REG-R1]: #uslib-reg-r1
[REG-R110]: #uslib-reg-r110
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R16]: #uslib-reg-r16
[REG-R18]: #uslib-reg-r18
[REG-R19]: #uslib-reg-r19
[REG-R20]: #uslib-reg-r20
[REG-R25]: #uslib-reg-r25
[REG-R30]: #uslib-reg-r30
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
