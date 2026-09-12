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

- **Projection frequency: monthly**, on policy months **[std]**. The contract's *annual*
  drivers stay annual and are processed at the anniversary — the dividend declaration and
  the capitalization of loan interest [S1] — and the guaranteed cash value schedule is an
  anniversary table. What the monthly grid adds is everything that is not contractually
  annual: **modal premium collection**, which retires the annual-mode standardization of
  product-spec Table 2 note (f) now that the grid can express the sourced modal factors
  [S1] [S7]; death claims settled in the month of death rather than at the anniversary;
  monthly expense accrual; and a surrender value that means something between
  anniversaries. An annual step remains a special case of the recursion below and
  reproduces its in-force at every anniversary exactly — see *Annual equivalence* — but it
  is not what the reference model runs.
- **Time index: `t` is 0-based and counts policy months.** `t = 0` is the issue month,
  period `t` runs from time `t` to time `t + 1`, and the frame is `t = 0 … T − 1` with
  `T = 12(100 − x)` the number of policy months projected. Because every contractual
  schedule is annual, the policy year is **derived** and used as a lookup key:
  `dur(t) = t // 12` is the completed policy years at the start of month `t`, and the
  contractual **policy year is the 1-based label `dur(t) + 1`**, never indexed by —
  "policy year 10" below is the months `t = 108 … 119`. The **anniversary** is the end of
  the last month of a policy year, `t ≡ 11 (mod 12)`, and that is where every annual event
  lands. An in-force model point opens at `t = 12·t0`, `t0 = duration_inforce` being the
  policy **years** already elapsed, so the frame always opens on an anniversary. A state
  variable subscripted `t` is its value at the **end** of month `t`; the value entering
  month `t` is the closing value of month `t − 1`, or the model point's opening state at
  the first projected month, and an annual quantity reads the balance entering its policy
  year, twelve months back. The one exception is `l_t`, the in-force probability, which is
  read at the **start** of month `t` so that it weights that month's cash flows.
- **Timing conventions [std]:** premiums and premium-linked expenses at the beginning of the
  month (BOM), in the months the elected mode makes them due; death claims and surrenders
  at the end of the month (EOM); dividends, loan-interest capitalization and maturity at
  the anniversary, in the processing order given below. State variables are stored at EOM.
- **Decrement conversion [std]:** every rate in this product is published and tabulated
  **annually**, and the monthly rates the recursion applies are derived from them at the
  constant-force conversion, `q_m = 1 − (1 − q)^(1/12)` and `w_m = 1 − (1 − w)^(1/12)`, so
  that twelve months compound back to exactly the annual rate.
- **Age basis: age nearest birthday (ANB)** **[std]** (product-spec Table 1 note (a)); the
  2017 CSO set provides ANB tables [R8]. The attained age entering the policy year of month
  `t` is `x + dur(t)`; at the anniversary that ends it, `x + dur(t) + 1`. Age changes on
  the anniversary, not on the birthday and not monthly.
- **Projection horizon:** to the anniversary at attained age 100, where the model pays a
  maturity benefit and terminates **[std]**. The contract itself matures at 121 [S1], but the
  guaranteed CV equals face at 100 and PUA CV equals PUA face at 100 [S1] [S3], so from age 100
  the policy is economically an endowment at face; truncating at 100 changes only the timing
  of the terminal payment between ages 100–121 (mortality vs. maturity), not its amount per
  survivor. The last projected month is `t = 12(100 − x) − 1`.
- **Model points:** single-policy model points, projected seriatim; results scale linearly in
  face within a band-free specification **[std]**. Amounts are U.S. dollars per policy;
  probabilities are per policy year.
- **Decrement model:** annual rates, applied monthly at the converted rates above; deaths
  before surrenders at EOM; the dividend is credited to the policies in force at the
  anniversary, after that month's deaths and before its surrenders **[std]** (order list
  below).
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
| `premium_mode` | enum {A, SA, Q, M} | A (the anchor cell; the mode drives which months collect an instalment, at the sourced modal factors [S1] [S7]) |
| `pua_rider_premium` (A_t) | float per year | 0.00 |
| `term_blend_target` | float (0 = off) | 0.00 (variant: 2 × F **[std]**) |
| `loan_utilization` | float in [0,1] | 0.00 (variant: 0.20 **[std]**) |
| `duration_inforce` (t0) | int, policy **years** elapsed (0 for new business); the frame opens at month `12·t0` | 0 |
| `puaf_inforce` | float (PUA face entering `t = 12·t0`) | 0.00 |
| `loan_inforce` | float | 0.00 |

## State variables

| Variable | Meaning | Initialization |
|---|---|---|
| `l_t` | Probability in force at the **start** of month t (per issued policy) | `l_0 = 1` |
| `CV_t` | Guaranteed cash value per policy (base), EOM t | anniversary table input, straight-line between anniversaries **[std]**; `CV_{T−1} = F` at `T = 12(100 − x)` [S1] [S3] |
| `PUAF_t` | Paid-up additions face in force, EOM t | opening balance at `t = 12·t0` is `puaf_inforce` |
| `PUACV_t` | PUA cash value, EOM t | `PUAF_t · NSP_m(t)` **[std]**, `NSP_m` the same straight line |
| `DA_t` | Dividend accumulation balance (ACCUM option only), EOM t | opening balance 0; accrues at `(1 + i_d)^{1/12}` monthly |
| `L_t` | Loan balance incl. capitalized interest, EOM t | opening balance at `t = 12·t0` is `loan_inforce` |
| `DB_t` | Death benefit payable on death in month t | formula below |
| `D_t` | Dividend credited at the anniversary ending month t; 0 in every other month | recursion below |

## Assumption inputs

The model distinguishes three assumption classes. Keeping them in separate input structures is
deliberate: (a) is locked by contract, (b) is an insurer-declared snapshot that re-rates
annually, (c) is the modeler's experience basis.

### (a) Contractual / guaranteed elements (from the product spec)

| Input | Value | Basis |
|---|---|---|
| Guarantee interest `i_g` | 4.00% | [S1]; Model 808 floor [R1] |
| Guarantee mortality `q^g_{x+dur(t)}` | 2017 CSO composite, sex-distinct, ANB | [S1] [R3] [R8]; ANB **[std]** |
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
| Experience mortality in scale `q^{sc}_{x+dur(t)}` | `AE^{sc} · q^{2015VBT}_{x+dur(t)}` with `AE^{sc} = 0.70` of 2017 CSO in the worked example | **[std illustrative]**; structure per [S4] [R6], tables [REG-R18] |
| Expense margin in scale `e^{m}_t` | $25 per policy per year | **[std]** |
| Dividend floor | `D_t ≥ 0` | **[std]** (dividends are non-negative distributions of surplus [R6]) |
| PUA purchase basis | `NSP_{x+dur(t)}` on 2017 CSO / 4%, unloaded (dividend purchases); 10% load on rider payments | **[std]** / [S3] (product-spec Table 3 note (k), Riders) |
| Accumulation option credit rate | `i_d` | [S2] rate declared annually; reuse of DIR **[std]** |

Non-guaranteed scales are constrained in illustration use by the disciplined-current-scale and
self-support / lapse-support machinery of Model 582 [R2] and ASOP 24 [REG-R30]; the model's
"current scale" should be interpreted as a currently-payable-scale snapshot, not a projection
of future scale changes.

### (c) Behavioral / experience assumptions (modeler-set; recommended public bases)

| Input | Recommended base | Reference value |
|---|---|---|
| Best-estimate mortality `q^e_{x+dur(t)}` | 2015 VBT (sex/smoker-distinct, ANB) × company A/E; industry A/E from the ILEC 2012–2019 study | tables [REG-R18], experience [R9]/[REG-R19]; A/E factor 0.70 × 2017 CSO in the worked example **[std illustrative]** |
| Base lapse `w_t` | LIMRA/SOA U.S. Individual Life Persistency study (WL by duration/size/mode) | [REG-R20] for the study; rates below **[std]** (study figures not recorded in the research file) |
| Lapse schedule **[std]** | Annual: 5.0% in policy year 1, grading linearly to 2.0% at year 10, level 2.0% thereafter; 0 through the final policy year, so its survivors mature rather than surrender | **[std]** — "low and level" pattern consistent with mature par WL persistency; source study [REG-R20] |
| Premium persistency | 1 (premiums are fixed and guaranteed; premium cessation = lapse/RPU) | [S1] [S3]; convention **[std]** |
| Premium mode | Modal factors [S1] (par: SA 0.515 / Q 0.26265 / M 0.085833) and [S7] (FE: 0.52 / 0.275 / 0.089) | A / SA / Q / M as a model point attribute, collected on the mode's own cycle; the load is inside the factor |
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
x           issue age (ANB)                     t   month index, t = 0 … 12(100 − x) − 1
dur(t)      completed policy years, t // 12         (policy year dur(t) + 1)
F           base face amount                    G   gross annual premium
P(t)        modal instalment collected at BOM t: modal factor x G^net in a due month [S1][S7]
i_g         guaranteed interest (4.00%)         i_d dividend interest rate (6.00%)
i_L         policy loan rate (6.00%)            v_g = 1 / (1 + i_g)
q^g_{y}     2017 CSO rate at attained age y     q^e_{y}  best-estimate rate at age y
            (both annual; q_m = 1 − (1 − q)^(1/12) is what the month applies)
w_t         annual lapse rate of the policy year of month t;  w_m likewise
l_t         in-force probability, BOM of t
CV_t        guaranteed cash value (base), EOM t: the anniversary table, straight-lined
NSP_y       net single premium per 1 of paid-up (endow-at-100) WL face at age y,
            on 2017 CSO / 4%:  NSP_y = A_{y:(100−y)|}  (endowment insurance to 100)
NSP_m(t)    the same, straight-lined from NSP_{x+dur(t)} to NSP_{x+dur(t)+1}  [std]
ä_{y:n|}    annuity-due, n years, on 2017 CSO / 4%
D_t         dividend credited at the anniversary ending month t (0 otherwise)
PUAF_t, PUACV_t  PUA face / cash value          DA_t  dividend accumulation balance
L_t         loan balance at EOM t
DB_t        death benefit, deaths in month t    E_t  expense outgo in month t
            (every state subscript t is an end-of-month t value)
```

### Guaranteed cash value: conceptual formula and practical treatment

Conceptual (Standard Nonforfeiture Law minimum, adjusted-premium / nonforfeiture-net-level-
premium method) [R1]:

```
NNLP      = F · NSP_x / ä_{x:(100−x)|}                       (net level premium, NF basis)
EA        = 0.01 · F + 1.25 · min(NNLP, 0.04 · F)            (expense allowance)  [R1]
P_adj     such that  P_adj · ä_{x:m|} = F · NSP_x + EA       (m = premium period)  [R1]
CV_t^min  = F · NSP_{x+t+1} − P_adj · ä_{x+t+1:(m−t−1)|}     (second term 0 once t ≥ m − 1)
```

on 2017 CSO / 4% [S1] [R1] [R3], written at the anniversary that ends policy year `k`, the
formula's `t` being `k − 1`. Properties to verify: the schedule reaches `F` at attained age
100 (since `NSP_100 = 1`), and smooth progression by duration [R1].

Practical treatment **[std]**: the reference implementation reads the schedule (per $1,000 of
face) from a table input keyed by policy year, because contractual CV tables are policy-form
documents not publicly available for the surveyed carriers (research gap noted in
`_research/whole-life.md`). The shipped table is generated from the formula above; an
implementer replacing it with a carrier table changes no other logic. Contractual
`CV ≥ CV^min` always [R1].

**Between anniversaries [std].** The schedule is printed at anniversaries only, so on a
monthly grid `CV_t` is straight-lined:

```
CV_t = CV^anniv_{dur(t)} + (CV^anniv_{dur(t)+1} − CV^anniv_{dur(t)}) · (t mod 12 + 1)/12
```

with `CV^anniv_k` the schedule's policy-year-`k` row and `CV^anniv_0 = 0`. It is exact at the
anniversary, where `t mod 12 = 11`, so **no anniversary quantity moves against the annual
grid** — not the dividend's interest margin, not the net amount at risk, not the anniversary
surrender value. Pro-rating for elapsed time is the ordinary policy-form convention and is
what makes a mid-year surrender value mean anything; the Standard Nonforfeiture Law requires
an adjustment for lapse of time in any case [R1]. `NSP` is straight-lined the same way, as
`NSP_m(t)`, so the paid-up-additions block is valued on the same clock.

### Dividend recursion (three-factor contribution formula)

Anchor (published mechanics of one surveyed carrier) [S4]:

```
D_t = ( CV_{t−1} + G − MEC_t ) · (1 + i_d) − CV_t
```

with `CV_{t−12}` the guaranteed cash value entering the policy year (zero at issue), and where
`MEC_t` is the mortality-and-expense charge based on actual company results — i.e., the
dividend is the excess of an experience-basis accumulated value over the guaranteed value [S4].

Reference parametrization **[std]** (exact carrier factor formulas are proprietary; this is the
classic three-factor contribution decomposition consistent with [S4] and the contribution
principle [R6]):

```
D_t = D^int_t + D^mort_t + D^exp_t ,   floored at 0        (t an anniversary month)
D^int_t  = (i_d − i_g) · (CV_{t−12} + NP_g)                      (interest margin)
D^mort_t = (q^g_{x+dur(t)} − q^{sc}_{x+dur(t)}) · (F − CV_t)     (mortality margin)
D^exp_t  = e^m_t                                                  (expense margin)
```

evaluated **once a year, at the anniversary**, and zero in every other month: the declaration
is annual [S1] and the monthly grid does not make it monthly. `CV_{t−12}` is the guaranteed
cash value entering the policy year the anniversary closes (zero at issue), which is the
annual grid's `CV_{t−1}` under the month index. `NP_g = NNLP` (the nonforfeiture net level
premium, so the interest margin applies to the guaranteed fund including the year's net
premium) **[std]**, `q^{sc}` is the scale's experience mortality (class (b)) at the **annual**
rate, and `e^m_t` the per-policy expense margin (class (b)). Dimensions: every term is dollars
per policy per year. Refinements observed in practice — interest on the
mortality margin, premium-timing adjustments, banded factors [S1] [S3] — are absorbed into the
calibration of `q^{sc}` and `e^m_t` **[std]**.

Dividends on the PUA block (PUAs are dividend-eligible [S14]) **[std]**:

```
D^PUA_t = (i_d − i_g) · PUACV_{t−12} + (q^g − q^{sc}) · (PUAF_{t−12} − PUACV_{t−12})
```

on the block entering the policy year the anniversary closes, valued at `NSP_{x+dur(t)}`. No
dividend is credited for policy year 1 **[std]** (product-spec Table 3 note (j); one carrier
pays none [S1], another pays a first-year dividend [S3]).

Direct recognition (loaned values) **[std]** parametrization of [S1] [S3]: replace `i_d` with
`i_L` on the loaned portion:

```
D^int_t (adjusted) = (i_d − i_g) · (CV_{t−12} + NP_g − L_{t−12}) + (i_L − i_g) · L_{t−12}
```

With `i_L = 6.00%` [S1] and the snapshot `i_d = 6.00%` **[std]** the adjustment is zero — a
coincidence of the snapshot, not a model property.

### Dividend application (by option)

- **PUA (default [S1] [S2]):** at the anniversary, `ΔPUAF_t = (D_t + D^PUA_t) / NSP_{x+dur(t)+1}`;
  `PUAF_t = PUAF_{t−1} + ΔPUAF_t`; `PUACV_t = PUAF_t · NSP_m(t)` **[std]** (the purchase falls
  at the anniversary, so it is priced at the attained age reached there; valuing all PUA face
  at the attained-age NSP on the guarantee basis is exact at issue of each layer and at age
  100, approximate between **[std]**). At age 100, `NSP_100 = 1` so `PUACV = PUAF` [S1].
- **CASH:** dividend paid out; policyholder cash flow at the anniversary.
- **REDUCE_PREM:** offsets the **next policy year's** premium:
  `G^{net} = max(G − D_{prev anniv}, 0)`, and the modal instalments then split what is left;
  excess to PUAs **[std]** (excess-to-PUA per one carrier's reduce-premium option [S3]).
- **ACCUM:** `DA_t = DA_{t−1} · (1 + i_d)^{1/12} + D_t`; the balance accrues monthly and the
  dividend lands on it at the anniversary, so twelve months compound to exactly the annual
  credit; the balance adds to death and surrender proceeds [S1] [S2].

### PUA rider (in-scope rider)

Rider payment `A` per year (within limits set at issue [S3] [S11]), billed with the base
premium and so collected on the same modal cycle **[std]**:
`ΔPUAF^rider_t = (modal instalment of A) · (1 − 0.10) / NSP` — priced at `NSP_{x+dur(t)}` for
the instalment that opens a policy year and at `NSP_m(t−1)` for the ones inside it — with a
10% load **[std]** from the observed 7.5%–10% range [S3]. Rider PUAs merge into `PUAF_t`, so
a monthly-mode rider buys twelve small layers through the year rather than one at the
anniversary.

### Term-blend rider (in-scope rider, simplified **[std]**)

Target face `TF = 2 F` **[std]** (within observed caps: ≤ 9× base [S2], ≤ 300% of base [S3]).
It is a **one-year** term layer: it is bought at the anniversary that closes a policy year and
is level through that year, so `OYT` is constant within the policy year and the cost is
charged once, at the anniversary. OYT face `= max(TF − F − PUAF_{prev anniv}, 0)` on the block
entering the policy year (writing it on the block leaving the year is circular — see
`model.md`); the dividend first pays the OYT cost `q^{sc}_{x+dur+1} · OYT · v_g` **[std]**,
remainder buys PUAs; crossover when `PUAF ≥ TF − F`, after which the rider is pure PUA
[S2] [S3] [S11]. Death benefit while blended: `TF + excess PUAs − L`.

### Benefit amounts

```
DB_t   = F + PUAF_{t−1} + OYT_t + DA_{t−1} − L_{t−1}          (PUA/ACCUM/OYT as elected)
CSV_t  = CV_t + PUACV_t + DA_t − L_t                          (surrender value, EOM t)
MAT    = F + PUAF_{T−1} + DA_{T−1} − L_{T−1}                  (at t = T − 1,
                                                               T = 12(100 − x);
                                                               model maturity [std])
```

`DB` per the contractual formula [S1], reduced to modeled components **[std]**. Deaths in
month t are assumed to occur at EOM and, at an anniversary, before that month's dividend is
credited, so `DB_t` carries the PUA face, accumulation balance and loan **entering** the
month **[std]** (terminal-dividend and premium-refund items not modeled, product-spec Table 3
note (m)).

### Monthly processing order (month t, per unit in force `l_t`)

1. **BOM:** collect the modal instalment of the gross premium `G^net` (if `dur(t) <` premium
   period `m`) and of the PUA rider premium `A`, in the months the mode makes them due; pay
   premium tax on what was collected and the month's twelfth of the maintenance expense,
   with the acquisition expense in month 0 only.
2. **BOM:** the REDUCE_PREM offset is applied to the policy year's annual premium, from the
   dividend credited at the anniversary that opened it; the instalments split what is left.
3. **During the month:** interest accrues implicitly (CV schedule on `i_g` [S1], straight-lined
   between anniversaries; loan at `i_L` [S1], capitalized annually).
4. **EOM — deaths:** probability `q^e_m`; outgo `q^e_m · l_t · DB_t`.
5. **Anniversary only — loan interest capitalization:** `L = L_{prev anniv} · (1 + i_L)` less
   repayments [S1].
6. **Anniversary only — dividend:** credit `D_t + D^PUA_t` to survivors (from policy year 2
   **[std]**); apply per dividend option; update `PUAF_t, PUACV_t, DA_t`.
7. **EOM — surrenders:** probability `w_m` applied to survivors `l_t · (1 − q^e_m)`; outgo
   `= CSV_t` per surrendering policy.
8. **Update in force:** `l_{t+1} = l_t · (1 − q^e_m) · (1 − w_m)`.
9. **At `t = T − 1`, `T = 12(100 − x)`:** pay `MAT` to the survivors `l_{T−1} · (1 − q^e_m)` —
   `w = 0` through the final policy year, so nobody surrenders out of it — and terminate
   **[std]**.

Ordering (deaths → dividend → surrenders at EOM) is **[std]**; it makes surrender values
include the just-credited dividend, consistent with anniversary processing.

**Annual equivalence.** Because the monthly rates compound back to their annual values and
every annual event stays on the anniversary, twelve months of step 8 collapse to
`l_{t+12} = l_t · (1 − q^e) · (1 − w)` — the annual-step recursion, term for term. The
in-force **at every anniversary** is therefore identical on the two grids, to floating point,
and so is every anniversary-dated quantity: the guaranteed cash value, the dividend and all
three of its margins, the paid-up additions purchased and in force, and the anniversary
surrender and death benefit amounts. What differs is the *cash flows*, which is the point of
the finer grid.

### Net liability cash flow (per issued policy, month t)

```
NetCF_t = − P(t) · l_t − A(t) · l_t + E_t · l_t                    (BOM items, sign: outgo +)
          + q^e_m · l_t · DB_t + w_m · l_t(1 − q^e_m) · CSV_t      (EOM benefits)
          + D^{cash}_t · l_t(1 − q^e_m)                            (cash dividends)
          + MAT · l_t(1 − q^e_m) · 1{t = T−1}                      (maturity)
```

Internal dividend applications (PUA, ACCUM, REDUCE_PREM) are not cash flows when credited;
they emerge later through `DB`, `CSV`, and `MAT` **[std]**. Loans are modeled on the offset
view: see next.

### Loans (offset treatment — brief)

Base run: `loan_utilization = 0`. Variant **[std]**: `L_t = 0.20 · CV_t` maintained by
borrowing/repaying as the cash value moves, so on the monthly grid the advances spread
through the year while the interest still capitalizes once, at the anniversary. Borrowed
amounts are policyholder cash outflows from the insurer, loan interest received is an
inflow, and `DB`/`CSV`/`MAT` are net of `L_t` [S1] [S3] [S9]. Under
direct recognition the dividend adjustment above applies [S1] [S3]. Economically the loan is an
offsetting asset; the reference model reports gross liability flows plus a separate loan
account rather than netting into a "net amount at risk" presentation **[std]**.

### RefWL-FE variant deltas

- Premium: `G = (F/1000) · rate(x, sex, tobacco) + 36` [S7]; no dividends (non-par
  [unverified]; modeled non-par).
- Graded plan: for natural-cause deaths in policy years 1–2 — the months `t = 0 … 23` —
  `DB_t = 1.10 · (cumulative premiums paid to BOM t)`, which on the monthly grid now grows
  with each instalment rather than once a year; accidental deaths pay `F` from day 1 [S6] [S7].
  Accidental split requires an accidental-death fraction of `q^e` **[std]** (reference value
  3% of deaths **[std]**).
- Maturity at age 100 (120 in FL — not modeled **[std]**) pays `F − L_{T−1}` [S8].
- CV schedule: reuse of the par nonforfeiture machinery **[std]** (product-spec Table 5 note (r)).
- Lapse: FE simplified-issue business lapses higher than par WL; reference schedule 12% in
  policy year 1, 10% in year 2, grading to 6% level by year 5 **[std]**, annual rates spread
  over their months at `w_m` (no FE-specific study in the research base; flagged as an open
  issue).

## Policyholder behavior modeling

Base behavior is static (schedules in class (c)). Dynamic overlays, all **[std]**:

- **Interest-sensitive lapse multiplier** (for scenario runs):
  `w_t^dyn = w_t · min(1 + 2.0 · max(0, r^{cmp}_t − i_d − 0.01), 3.0)` where `r^{cmp}_t` is
  the competitor/market rate in the scenario. Rationale: par WL cash values are liquid at book
  value, so sustained rate spreads induce excess surrender; the low base level reflects the
  strong persistency of dividend-paying WL. Calibration is judgmental **[std]** — the research
  base records no dynamic-lapse study for WL.
- **Premium offset behavior:** once the prior anniversary's dividend covers the annual
  premium, a fraction
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
`F = 100,000` **[std]**, `G = 1,800` **[std illustrative]**, annual mode, PUA dividend option,
no rider, no loan. Policy year 10 — the months `t = 108 … 119`, with the anniversary at the
end of month 119 (attained age 55 there). All table values are illustrative **[std]** (the
shipped CV/NSP tables are generated on 2017 CSO / 4% as specified above); `i_g = 4.00%` [S1],
`i_d = 6.00%` **[std]**.

Every step below is an **anniversary** quantity, and the monthly grid leaves anniversary
quantities exactly where the annual grid put them — which is why the walk-through is
unchanged by the change of grid. What the grid changed is the *index* each one is read at:
`CV_8` is now `CV_107`, the close of the month before the policy year opens, and `CV_9` is
`CV_119`.

| Step | Item | Formula | Value |
|---|---|---|---|
| 1 | Guaranteed CV entering the policy year | `CV_107` (table, policy year 9) | 9,500.00 **[std]** |
| 2 | Guaranteed CV at the anniversary | `CV_119` (table, policy year 10) | 11,200.00 **[std]** |
| 3 | Net level premium (NF basis) | `NP_g` | 1,300.00 **[std]** |
| 4 | Guarantee mortality, age 54 | `q^g_54` (annual) | 0.00320 **[std]** |
| 5 | Scale mortality, age 54 | `q^{sc}_54 = 0.70 · q^g_54` | 0.00224 **[std]** |
| 6 | Interest margin | `(0.06 − 0.04) · (9,500 + 1,300)` | 216.00 |
| 7 | Mortality margin | `(0.00320 − 0.00224) · (100,000 − 11,200)` | 85.25 |
| 8 | Expense margin | `e^m` | 25.00 **[std]** |
| 9 | Dividend | `D_119 = 216.00 + 85.25 + 25.00` | 326.25 |
| 10 | NSP at age 55 | `NSP_55` (table) | 0.42 **[std]** |
| 11 | PUA face purchased | `ΔPUAF_119 = 326.25 / 0.42` | 776.79 |
| 12 | PUA face at the anniversary (prior 4,100.00 **[std]**) | `PUAF_119 = 4,100.00 + 776.79` | 4,876.79 |
| 13 | PUA cash value at the anniversary | `PUACV_119 = 4,876.79 × 0.42` | 2,048.25 |
| 14 | Death benefit for deaths in month `t = 120` | `F + PUAF_119` | 104,876.79 |
| 15 | Surrender value at the anniversary, EOM `t = 119` | `CV_119 + PUACV_119` | 13,248.25 |

(For clarity the PUA-block dividend `D^PUA` is omitted from this table; in the model it adds
`(0.02 · PUACV_107) + (0.00096 · (PUAF_107 − PUACV_107))` to the amount in step 9 **[std]**.)

The steps the monthly grid *adds* sit between those anniversaries. The mortality rate applied
in each of the twelve months is `q^e_m = 1 − (1 − 0.70 × 0.00320)^{1/12} = 0.00018686`, and
twelve of them compound back to `1 − (1 − 0.00018686)^{12} = 0.00224` exactly — the annual
rate of step 5's basis. The guaranteed cash value climbs from 9,500.00 to 11,200.00 in twelve
straight-line steps of 141.67, so a surrender in month `t = 113` (the sixth month of the
policy year) is valued at `CV_113 = 9,500 + 6 × 141.67 = 10,350.00` plus the paid-up
additions at `NSP_m(113)`, rather than at either anniversary's figure. And the annual premium
of 1,800.00 is still collected once, in month 108, because the anchor cell is annual mode;
model point 15 is the same policy on monthly mode, which collects `0.085833 × 1,800 = 154.50`
in each of the twelve.

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
   On the monthly grid it compounds continuously, `1.02^{t/12}`, rather than stepping at
   anniversaries.
5. **Loan utilization** under direct recognition [S1] [S3]: shifts dividend composition and
   net cash flow timing; the fixed-6%/DIR-6% snapshot coincidence (zero adjustment) will not
   survive a scale change.

Known modeling pitfalls:

- **CV-table vs. first-principles mismatch:** if the CV table input and the `NSP`/annuity
  functions come from different bases, `PUACV ≠ PUAF` at age 100 and the dividend recursion
  leaks. Regenerate all guarantee-basis quantities from one 2017 CSO / 4% source [S1] [R1] [R8].
- **Dividend floor and negative margins:** with `D_t` floored at 0 **[std]**, adverse
  experience does not claw back — asymmetry matters in stochastic runs.
- **First-dividend timing** (policy year 1 vs 2) shifts early-duration PUA compounding; it
  is a real cross-carrier difference [S1] [S3], keep it a parameter.
- **Making an annual event monthly.** The dividend declaration, the capitalization of loan
  interest and the purchase of paid-up additions are annual by contract [S1]. Crediting a
  twelfth of the dividend each month, or capitalizing loan interest monthly, changes the
  answer and is not a refinement — it is a different product. On the monthly grid these
  events belong on the anniversary month and nowhere else.
- **Converting the rate at the wrong point.** `q_m` and `w_m` are taken from the fully
  loaded **annual** rate, and the *annual* rate is what the dividend's mortality margin
  uses: `q^g − q^{sc}` in `D^mort` is an annual margin on an annual net amount at risk, and
  substituting monthly rates there understates the dividend twelvefold.
- **Interpolating the wrong quantity.** `CV` and `NSP` are straight-lined between
  anniversaries **[std]**, which is exact at the anniversary. Interpolating `PUAF` as well
  would double-count — the block is a step function that only changes when a purchase is
  made — and interpolating the dividend would make it monthly (see above).
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
