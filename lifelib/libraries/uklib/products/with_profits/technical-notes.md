# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's fund. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `_research/with-profits.md`); [REG-R#] tags
refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks
claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`. Mechanics anchors: the PPFMs of three proprietary insurers
[S1] [S4] [S5]; regulatory codification of the asset-share item list: PRA Surplus
Funds Part [R8]; canonical methodology literature: Needleman & Roff (1995) on asset
shares and Hibbert & Turnbull (2003) on guarantee costs, as listed on the IFoA SA2
resources page [R13].

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums in; death,
  maturity and surrender claims out; expenses; shareholder transfers) for
  single-policy with-profits model points on the two composite chassis (unitised bond,
  conventional endowment), with the smoothed-fund (PruFund-style) variation as an
  alternative crediting module. Reserves are not computed here (see Valuation and
  reserve pointers).
- **The asset share is a state variable, not a cash flow.** Policy cash flows are
  premiums, claims (paid at smoothed payouts), expenses and shareholder transfers;
  the asset share [S1] [R8] drives claim amounts through the bonus, smoothing and MVR
  machinery. The estate absorbs payout-vs-asset-share differences [S1] [S5].
- **Projection frequency.** Monthly **[std]**, with the **bonus declaration left on its
  annual cycle**. The declaration is the governing act of discretion, it happens once a
  policy year, and it permanently hardens the guarantee [S1] [S4] [S7] — so it fires in
  the twelfth month of each policy year and nowhere else, while everything continuous
  (fund return, charges, mortality charge, decrements, the smoothed payout, the final
  bonus and the MVR) runs monthly around it. Annual rates are converted with the
  effective forms `(1 + r)^(1/12)` and `1 − (1 − r)^(1/12)` **[std]**, so twelve months
  compound back to the annual figure exactly and the assumption basis does not move with
  the grid. The PruFund daily/quarterly smoothing [S9] [S11] remains out of scope: a
  monthly grid still cannot carry a 5% *daily* limit or a 2.5% gap trigger that fires
  and unwinds between two monthly points.
- **Time index [std].** `t` is the **0-based** policy month index: `t = 0` is the issue
  month, month `t` runs from time `t` to time `t + 1`, and the projection covers
  `t = 0, 1, …, proj_len − 1`, so `proj_len` is the number of policy months from issue.
  An in-force cell opens its frame at `t = 12 × duration_ifo`, its elapsed months, and
  carries its state in as the **opening** balances of that month. The contractual policy
  year containing month `t` is the 1-based label `t // 12 + 1`; anniversary `k` ends
  month `12k − 1`; and the attained age in month `t` is `x + t // 12`, advancing on the
  anniversary.
- **Timing conventions [std].** Premiums and partial withdrawals at the start of the
  month (BOM); fund return accrues over it; proportional charges, the shareholder
  transfer and the mortality charge at end of month (EOM), in the processing order
  below; claims and decrements at EOM. The bonus declaration falls at EOM in a
  **declaration month** only — `(t + 1) mod 12 = 0` — ahead of that month's mortality
  charge and payout calculation, so the hardened guarantee is what the month's claims
  are measured against.
- **Age basis.** Age nearest birthday **[std]** — no retrieved UK document fixes a
  model age basis; ANB is chosen for symmetry with the library's US convention (its
  traditional use in UK assured-lives tables is [unverified]; the currently marketed
  bond quotes its issue-age limit on an age-next-birthday basis [S10]).
- **Currency.** GBP. Single-policy model points, projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
- **Specimen-policy convention.** Firms compute asset shares for specimen policies or
  groups, not necessarily per policy [S1] [S4] [S5] [R1 COBS 20.2.5R(2)](#uklib-with_profits-r1); the reference
  model computes a per-model-point asset share and treats it as the specimen.
- **Rounding.** Intermediate values at full precision; cash flows reported to pence
  **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cells, product-spec) |
|---|---|---|
| `chassis` | enum {UWP_bond, CWP_endowment, SF_prufund} | UWP_bond |
| `issue_age` | int (ANB) | 55 (UWP) / 35 (CWP) |
| `sex` | enum {M, F} | M |
| `duration_ifo` | int, completed policy years at valuation | 5 |
| `premium_single` | currency (UWP bond) | 25,000 |
| `premium_regular` | currency p.a. (CWP: £60/month → 720 p.a.) | 720 |
| `sum_assured` | currency (CWP basic SA) | 20,000 |
| `term_years` | int (CWP; UWP bond whole-of-life → none) | 25 |
| `units` | float (UWP) | 25,000 |
| `unit_price` | currency (UWP `Q`; £1.0000 at seed) | 1.104081 |
| `attaching_bonus` | currency (CWP `G − SA`) | — |
| `asset_share_init` | currency (in-force cells); the `AS` the first projected month opens with | 30,000 |
| `smoothed_payout_init` | currency; the opening `S`, benchmark for the smoothing cap | 29,500 |
| `guarantee_dates` | list of anniversaries (MVR-free); anniversary `k` ends month `12k − 1` | {10} |
| `mvr_free_wd_rate` | % of original premium p.a. | 5% |
| `tax_basis` | enum {life_net, pension_gross} [S1] [REG-R17] | life_net |
| `gao_flag` / `gao_rate` | bool / annuity per £1 cash | false / — |
| `mutual_dist_flag` | bool (mutual profit distribution variation [S6]) | false |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `AS(t)` | Asset share at the end of month t [S1] [R8] | monthly recursion |
| `Q(t)` | With-profits unit price (UWP) at the end of month t; never decreases | EOM, **declaration months only** |
| `FV(t)` | Unit face value `U(t)·Q(t)` (UWP) | EOM |
| `G(t)` | Guaranteed benefit `SA` + attaching reversionary bonuses (CWP) | EOM, **declaration months only** |
| `b` | Declared annual regular bonus rate for the policy year holding t | once a policy year, setting rule |
| `S(t)` | Smoothed target payout (after the cap and the corridor) | EOM |
| `FB(t)` | Final (terminal) bonus payable on a claim in month t | EOM |
| `MVR(t)` | Market value reduction on non-guaranteed exits | EOM |
| `CB(t)` | Cost of bonus recognized in month t; nil outside a declaration month | EOM |
| `ST(t)` | Shareholder transfer = `CB(t)/9` (90:10); nil with it | EOM |
| `SM(t)` | Smoothing account balance (within estate) | on exits |
| `CumGC(t)` | Cumulative guarantee-charge deductions (for the 2% lifetime cap [S1]) | monthly |
| `l(t)` | In-force probability at the **start** of month t (at time t) | BOM, after the previous month's decrements |

`Q`, `FV` and `G` are **step functions of the policy year**: a declaration moves them in
the twelfth month and they are flat through the other eleven. That is the single most
important thing to get right when implementing this on a monthly grid — compounding the
annual rate `b` twelve times a year produces a projection that runs, whose roll-forwards
close, and whose guarantee is an order of magnitude too large a decade later.

Each state variable except `l` is a **closing** balance: `AS(t)`, `Q(t)`, `FV(t)`,
`G(t)`, `S(t)` are the values at the end of month `t`, so the value a month opens with
is the previous month's close, and for the first projected month it is the carried-in
state on the model point. `l` is the count at a time point: `l(t)` is the in force at
the start of month `t`, `l(0) = 1` at issue, and it is the weight on that month's
cash flows.

---

## Assumption inputs

Three classes are distinguished explicitly. Class (a) is contractual/guaranteed;
class (b) is the insurer's current discretionary scale (PPFM-governed discretion
[R2], advised by the With-Profits Actuary [R5]); class (c) is the modeler's view of
experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Basic sum assured / premium / term (CWP) | £20,000 / £720 p.a. / 25 years | anchor **[std]**, product-spec (15) |
| Bonus hardening | declared regular bonus increases the guaranteed benefit; contractual once added; guaranteed at death/maturity only | [S1] [S8] |
| Unit-price floor (UWP) | `Q(t) ≥ Q(t−1)`, i.e. `b(t) ≥ 0` | [S1] [S4] |
| Guarantee events (UWP) | death; contractual guarantee dates (10th anniversary); face value + FB payable without MVR | [S4] [S5]; date choice **[std]**, product-spec (12) |
| Death benefit factor (UWP) | `g_db = 101%` of (FV + FB); MVR never on death | 101% **[std]**, product-spec (11); no-MVR [S5] |
| MVR-free withdrawals | ≤ 5% p.a. of original premium | **[std]**, product-spec (13) |
| MVR contractual bound | MVR ≤ excess of unit value over underlying asset value | [R1 COBS 20.2.16R](#uklib-with_profits-r1) |
| PruFund smoothing limits (variation) | daily 5.0% / quarterly 10.0% / gap 2.5% (growth funds); contractual defined terms | [S9] [S11] |

### (b) Insurer-discretionary current elements (snapshot; revisable under PPFM discipline [R2] [R5])

| Input | Value | Basis |
|---|---|---|
| Regular bonus rate `b` — UWP | 2.00% p.a. | **[std]**, product-spec (8) — declarations not public in PPFMs |
| Reversionary bonus rate `b_rev` — CWP | 1.50% p.a. compound | **[std]**, product-spec (16) |
| Bonus change cap | ±1.00% p.a. in normal circumstances; floor 0 | [S1] [S7]; adoption **[std]**, product-spec (20) |
| Guarantee-fill target `θ` | 80% of projected maturity asset share | **[std]**, product-spec (21); philosophy [S1] |
| Smoothing y/y cap `σ` | ±10% | [S1]; adoption **[std]**, product-spec (23) |
| Target corridor | 80%–120% of asset share | [S1] [R1]; adoption **[std]**, product-spec (22) |
| AMC `c_amc` (UWP) | 1.00% p.a. | **[std]**, product-spec (9) |
| Guarantee/smoothing charge `c_g` | 0.10% p.a. of asset share; lifetime cap: deductions cease once `CumGC ≥ 2% ×` current asset share | cap [S1]; rate and cap mechanics **[std]**, product-spec (10) |
| Interim bonus rate | = last declared regular bonus rate | practice [S1] [S7]; equality **[std]**, product-spec (17) |
| MVR scale | derived each year from the formulas below (no tabulated scale) | [S5] [S6]; derivation **[std]** |
| EGR (smoothed-fund variation) | 5.0% p.a. | **[std]**, product-spec (25) |
| Mutual profit distribution (variation) | 0 in base | [S6]; base choice **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

CMI tables issued after 1 March 2013 are subscriber-restricted [R10] [REG-R22], so no
current CMI rates can be reproduced here: the reference basis is a **[std]** proxy on
the freely redistributable ONS national life tables [REG-R32] (population mortality
is heavier than insured experience [REG-R32]). AM92/AF92 (published 1999) remain the
canonical assured-lives *shape* reference [REG-R24]; their use in historical
with-profits work is [unverified] convention [R10].

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base mortality | 60% × ONS National Life Tables (UK, 2021–2023) qx, sex-distinct | proxy **[std]**; source [REG-R32]; shape cross-check AM92 [REG-R24] |
| Mortality improvement | CMI_2025 projections model, long-term rate 1.25% p.a. — *named, not reproduced* (subscriber-restricted) | model existence [REG-R30]; LTR choice **[std]** |
| Base surrender rate — UWP bond | 5% p.a. flat | **[std]** |
| Base lapse rate — CWP endowment | 5% yr 1, 4% yr 2, 3% yr 3, 2% yrs 4+ | **[std]** |
| Dynamic surrender multipliers | see Policyholder behavior modeling | **[std]** |
| Paid-up conversion (CWP) | excluded from base model; flag for extension | option exists [S4]; exclusion **[std]** |
| Maintenance expense | £30 per policy p.a., inflating 3.0% p.a. | **[std]** |
| Fund return `r(t)` | 5.0% p.a. deterministic base scenario, net of dealing costs [S5]; net of life-fund tax for `tax_basis = life_net` cells [S1] [REG-R17] | scenario level **[std]** |
| GAO take-up (legacy flag) | 90% when in-the-money by >10%, else 30% | **[std]** [unverified — no public experience retrieved] |

Deterministic single-scenario projection is the base; the cost of guarantees requires
stochastic valuation (see Cash flow components, cost-of-guarantees note).

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy **month** index, **0-based**: `t = 0, 1, …, proj_len − 1`; policy year `y(t) = t // 12 + 1`; `x` = age at entry (ANB), attained age `x + t // 12` |
| `P(t)` | premium received at BOM t (a twelfth of the annual regular premium) |
| `W(t)` | partial withdrawals paid at BOM t (a twelfth of the annual election) |
| `E(t)` | insurer maintenance expense in month t ((£30/12) × 1.03^(y(t)−1) **[std]**) |
| `r`, `r_m` | earned fund return, annual (net basis per `tax_basis`) and monthly |
| `c_amc`, `c_g` | AMC 1.00% p.a.; guarantee/smoothing charge 0.10% p.a. **[std]**; `c_amc,m`, `c_g,m` their monthly equivalents |
| `q(x+t)`, `q_m` | annual mortality rate (class (c) basis) and its monthly equivalent |
| `w(t)`, `w_m` | annual surrender/lapse rate (incl. dynamic multipliers) and its monthly equivalent, the guarantee-date encashment included |
| `ε` | guarantee-date encashment rate, 7.5% of the survivors of that month **[std]** |
| `MC(t)` | mortality charge to the asset share in month t [S1] |
| `b`, `b_rev` | declared annual regular / reversionary bonus rate for the policy year |
| `Q(t)`, `U(t)`, `FV(t)` | unit price, units, face value (UWP); `FV = U·Q` |
| `G(t)` | guaranteed benefit (CWP): SA + attaching bonuses |
| `S(t)` | smoothed target payout after cap and corridor |
| `FB(t)`, `MVR(t)`, `TB(t)` | final bonus, market value reduction, terminal bonus |
| `CB(t)`, `ST(t)` | cost of bonus; shareholder transfer = CB/9; both nil outside a declaration month |
| `θ, κ, σ` | guarantee-fill target 0.80; bonus-smoothing speed 0.5; **year-on-year** cap 10% **[std]**, applied monthly as `(1∓σ)^(1/12)` |
| `g_db` | UWP death benefit factor 1.01 **[std]** |
| `i_sv` | CWP surrender-basis discount rate 4.0% **[std]**; `v_sv = 1/(1+i_sv)` |
| `n` | CWP term in years (25), so maturity falls at the end of month `12n − 1`; `h` = UWP bonus-setting horizon (10 years **[std]**) |
| `l(t)` | in-force probability at the start of month t (at time t); `l(0) = 1` |

### Monthly processing order [std]

Monthly rates, all **[std]** effective conversions of the annual assumptions:
`r_m = (1+r)^(1/12) − 1`, `c_amc,m = 1 − (1−c_amc)^(1/12)`,
`c_g,m = 1 − (1−c_g)^(1/12)`, `q_m = 1 − (1−q)^(1/12)`, `w_m = 1 − (1−w)^(1/12)`.

For month t = 0..proj_len−1:

1. **BOM**: premium `P(t)` received — a twelfth of the annual regular premium **[std]**,
   plus the single premium at `t = 0`; UWP units purchased:
   `U(t) = U(t−1) + α·P(t)/Q(t−1)` with allocation `α = 100%` (product-spec (7)).
2. **BOM**: partial withdrawals `W(t)` paid — a twelfth of the annual election **[std]**
   (MVR applies if outside the MVR-free allowance); asset share reduced pro rata to the
   pre-MVR policy value [S1].
3. Fund return `r_m` accrues on the asset share balance.
4. **EOM**: proportional charges: multiply by `(1 − c_amc,m − c_g,m)`; accumulate
   `CumGC`; set `c_g = 0` for the month once `CumGC(t−1) ≥ 2% × AS(t−1)` — the
   cumulative and the asset share the month **opens** with, so that the charge does not
   depend on the balance it is deducted from [S1 cap; mechanics **[std]**]. The cap is
   tested every month rather than once a year, so the charge stops the month the
   cumulative overtakes the threshold.
5. **EOM, declaration months only** (`(t+1) mod 12 = 0`): the annual regular bonus `b`
   declared for the policy year per the setting rule below;
   `Q(t) = Q(t−1)(1+b)` (UWP) or `G(t) = G(t−1)(1+b_rev)` (CWP);
   cost of bonus `CB(t)` computed on pre-declaration values; shareholder transfer
   `ST(t) = CB(t)/9` deducted from the asset share [S5] [R8]; product-spec (2). In the
   other eleven months `Q(t) = Q(t−1)`, `G(t) = G(t−1)` and `CB = ST = 0`.
6. **EOM**: mortality charge `MC(t) = q_m · max(0, DB_g(t) − AS_pre(t))`
   deducted, where `DB_g` is the guaranteed death benefit (`g_db·FV(t)` UWP; `G(t)`
   CWP) and `AS_pre` the balance after step 5 [S1 formula: mortality rate × (death
   benefit − policy value); guaranteed-only DB in the sum at risk **[std]**]. In the
   eleven months before a declaration the sum at risk is measured against the guarantee
   as it then stands; the declaration month's charge is the first to carry the hardened
   one.
7. **EOM**: smoothed payout `S(t)` computed (cap, then corridor); `FB`/`TB`/`MVR`
   derived. All three are monthly quantities: a claim in any month is paid on the
   payout of that month.
8. **EOM**: claims paid — deaths at `q_m`, surrenders at `w_m`, maturity at the last
   projected month `t = 12n − 1`; smoothing account posts `(payout − AS(t))` per exiting
   unit of probability.
9. Survivorship: `l(t+1) = l(t) · (1 − q_m) · (1 − w_m)` (maturity month:
   survivors mature).

Because `q_m` and `w_m` compound back to `q` and `w` exactly over twelve months, and
both are constant within a policy year, `l(12y)` is the in-force an annual-step
projection of the same tables would report at the `y`-th anniversary. That identity is
the cheapest check on a monthly implementation of the decrements.

### Asset share recursion (core)

```
AS(t) = [ AS(t−1) + P(t) − W_AS(t) ] · (1 + r_m) · (1 − c_amc,m − c_g,m)
        − ST(t) − MC(t) + M(t)
```

`AS(t−1)` is the balance month `t` **opens** with: the previous month's closing asset
share, or, in the first projected month of an in-force cell, the `asset_share_init` the
model point carries. The same reading applies to `Q(t−1)`, `G(t−1)`, `FV(t−1)` and
`S(t−1)` below — there is no row below the frame.

Component bases (each item as recorded for the retrospective accumulation
[S1] [S2] [S4] [S5] [S6] [S7] and codified in PRA Surplus Funds 3.3 [R8]):

- **Premiums `P(t)`** — accumulated in full; explicit charges are taken via `c_amc`
  rather than allocation deductions **[std]** (product-spec (7)).
- **`W_AS(t)`** — asset-share reduction for BOM withdrawals, pro rata to the pre-MVR
  policy value [S1].
- **Investment return `r(t)`** — actual return on the backing asset pool including
  unrealised gains [S1] [S5] [R8]; net of dealing costs [S5]; net of life-fund tax for
  BLAGAB cells, gross for pensions [S1] [S2] [REG-R17]; asset shares are not credited
  with return earned on the estate [S1] [S2].
- **Expenses/charges `c_amc`** — percentage-of-asset-share expense charge; observed
  1% caps [S1] [S5]; excess actual expenses over charges fall to the estate [S1].
- **Cost of guarantees and smoothing `c_g`** — deduction from credited return
  [S1] [S4] [S6]; lifetime cap 2% of asset shares [S1].
- **Shareholder transfer `ST(t)`** — charged to asset shares [S5] [R8]; one-ninth
  formulation **[std]** (product-spec (2)).
- **Mortality charge `MC(t)`** — rate × sum at risk; actual-vs-charged differences
  accrue to the estate [S1].
- **Miscellaneous surplus / estate distributions `M(t)`** — allocated annually where
  applicable [S1] [S5] [R8]; `M(t) = 0` in the base model **[std]** (product-spec (3)),
  so the monthly grid has nothing to allocate.

### Regular bonus setting rule [std]

The PPFM principles are: rates set from projections; gradual changes (±1% p.a.
normal); keep a substantial proportion of the payout in final-bonus form; full
discretion to declare zero [S1] [S7]. The reference parametrization:

1. Project the asset share to the horizon at the expected net return
   `r_e = r_base − c_amc − c_g` **[std]** — annual rates throughout, because the rate
   being set is annual — from the balance the declaration month opens with:
   `AS_proj = AS(t−1) · (1+r_e)^(m) + future premiums accumulated to the horizon at
   r_e`, with `m = n − y(t)` in **years**, the term less the policy year the declaration
   closes (CWP), or `m = h = 10` (UWP whole-of-life bond).
2. Supportable rate: the level bonus rate that grows the guarantee to the
   guarantee-fill target θ = 80% of the projected asset share, measured on the
   guarantee the declaration month opens with:
   - UWP: `b_supp = [ θ·AS_proj / FV(t−1) ]^(1/m) − 1`
   - CWP: `b_supp = [ θ·AS_proj / G(t−1) ]^(1/m) − 1`
3. Smoothed declaration with the ±1% discipline [S1] [S7]:
   `b(y) = max( 0, b(y−1) + clamp( κ·(b_supp − b(y−1)), −0.01, +0.01 ) )`, κ = 0.5
   **[std]**. The discipline is **per declaration**, so the rule is applied once a
   policy year, at that year's declaration month, against the rate declared a year
   earlier — not once a month, which would be a different and far looser rule.

The base projection holds the snapshot rates (2.00% UWP / 1.50% CWP) level; the rule
above is the revision module for scenario work.

### Smoothed payout, final bonus, terminal bonus

Raw target = the unsmoothed asset share (payout target 100% of asset share
[S5] [S7] [S8] [R1]). Apply the smoothing cap, then the corridor, every month:

```
S_raw(t)  = AS(t)
S_cap(t)  = clamp( S_raw(t), (1−σ)^(1/12)·S(t−1), (1+σ)^(1/12)·S(t−1) )   σ = 10%  [S1]
S(t)      = clamp( S_cap(t), 0.80·AS(t), 1.20·AS(t) )                     [S1][R1]
```

The cap is the **year-on-year** ±σ discipline [S1] taken to its twelfth root **[std]**,
so that twelve capped months move the payout by exactly ±σ over the policy year. That
conversion is what preserves the rule's meaning on a monthly grid: a flat ±σ per month
would be twelve times as loose, and applying ±σ only at anniversaries would leave the
eleven intervening payouts — on which real claims are paid — unsmoothed.

The corridor implements the 80–120% target range deterministically at model-point
level; the ≥90%-of-policies test [S1] [R1] is a portfolio property, out of scope for a
single-policy model **[std]**.

- UWP final bonus: `FB(t) = max(0, S(t) − FV(t))`; guarantee-event payout
  `FV(t) + FB(t)`; death payout `g_db · (FV(t) + FB(t))` [S5: no MVR on death].
- CWP terminal bonus: `TB(t) = max(0, S(t) − G(t))`; maturity payout
  `G + TB` at the end of the last projected month, `t = 12n − 1`;
  death payout `G(t) + interim accrual + FB per the same scale` [S1] [S4] [S8].
- When the guarantee bites (`S(t) < FV(t)` or `S(t) < G(t)`), the excess of the
  guaranteed payout over the asset share is charged to the smoothing/guarantee
  account within the estate [S1] [S4].

### MVR (unitised, non-guaranteed exits)

```
MVR(t) = min( max(0, FV(t) − S(t)),  max(0, FV(t) − AS(t)) )
Surrender payout = FV(t) + FB(t) − MVR(t)
```

The first argument recovers the smoothed-payout shortfall below face value (post-MVR
payouts target 100% of asset share, here its smoothed image [S5]); the second is the
COBS 20.2.16R bound — the MVR may not exceed the excess of unit value over the
underlying asset value [R1]. Because `FB > 0` requires `S > FV` and `MVR > 0`
requires `S < FV`, final bonus and MVR are never simultaneous (the rule observed in one
consolidated with-profits fund [S4]; adoption product-spec (24)). MVR-free events:
death [S5], guarantee dates [S4] [S5], withdrawals within the 5% allowance **[std]**
(product-spec (13)).

A guarantee date is a **date**, and the monthly grid says so: an exit in month `12k − 1`
for a guarantee anniversary `k` is MVR-free, and an exit in any of the other eleven
months of that policy year bears the reduction like any other. An annual grid has to
treat the whole year as the date.

### Cost of bonus and shareholder transfer (90:10 mechanics)

`ST(t) = CB(t) / 9` — one-ninth of the cost of bonus, so that shareholders receive
10% of each 90:10 distribution (product-spec (2); components [S1] [S5] [S8] [R1]).
Measurement of `CB` **[std]**:

Both arise in the declaration month and are nil in the other eleven.

- UWP regular bonus: `CB_reg(t) = b · FV(t−1)` — the face-value uplift delivered
  by the declaration, on the face value that month opens with.
- CWP reversionary bonus: `CB_reg(t) = ΔG(t) · v_sv^(n−y(t))` with
  `ΔG(t) = G(t) − G(t−1)` — the declared addition discounted to the declaration date
  over the `n − y(t)` **years** still to run (survivorship discount omitted **[std]**
  simplification).
- Final/terminal bonus: `CB_fb(t) = (FB or TB paid on claims in month t)`, recognized
  at payment, so unlike the regular-bonus cost it arises in any month a claim does.

`ST` is a cash outflow from the fund (distribution to shareholders), reported
separately in the model output; per COBS 20.2.17AR, adjustments reducing policyholder
distributions below the required percentage require proportionate
shareholder-transfer reductions [R1] — modeled implicitly by tying `ST` to
actually-declared/paid bonus.

### Smoothing account

On each exit, post the smoothing cost `(payout − AS(t))` weighted by the exiting
probability to `SM(t)` (within the estate). Intended broadly neutral over time
[S1] [S2] [S5] [S6]; the base model tracks the balance without recycling. Optional
module: year-end recycling into credited returns as one insurer operates it (maximum
deduction currently 2.5% of asset shares p.a.) [S5].

### Cost of guarantees — cited, not specified

The deterministic charge `c_g` is a *charging* proxy, not a valuation. The economic
cost of the guarantees (unit-price floor, guarantee-date face value, CWP sum assured
plus hardened bonuses, GAO) requires stochastic market-consistent valuation: PRA
Technical Provisions 9.2 requires guarantees and options to be valued with realistic
dynamic assumptions [R7], and the canonical methodology is market-consistent
stochastic simulation of the bonus/smoothing/MVR rules (Hibbert & Turnbull 2003; Hare
et al. 2000 [R13]). This model produces the per-scenario cash flows such a valuation
consumes; the stochastic layer itself is out of scope.

### GAO module (legacy flag)

Where `gao_flag` is set (CWP pension cells), the retirement benefit is
`max( CashFund(T) · OMR(T), CashFund(T) · gao_rate )` — the guaranteed annuity rate
floors the open-market conversion. GAOs are present in several closed funds, backed
by fixed-interest assets, with interest-rate risk identified as a fund business risk
[S4]; the 2000 GAO litigation history is [unverified] context. `gao_rate` = £0.09 p.a. per
£1 of cash fund **[std]** [unverified as typical]; take-up per class (c). The GAO is
a valuation-critical option (stochastic interest-rate exposure) — cited, not
fully specified.

### Cash flow outputs (per month t, probability-weighted by `l`)

`l(t)` is the in force at the start of month `t`, so it is the weight on every flow of
that month — the same row of the result table.

| Output | Formula |
|---|---|
| Premium income | `P(t) · l(t)` |
| Death claims | `q_m · l(t) · DeathPayout(t)` |
| Surrender claims | `w_m · l(t) · (1 − q_m) · SurrenderPayout(t)` |
| Maturity claims | `l · (1 − q_m)(1 − w_m) · (G + TB)` — the survivors of the last projected month `12n − 1` (CWP) |
| Partial withdrawals | `W(t) · l(t)` |
| Maintenance expenses | `E(t) · l(t)`, a twelfth of the annual expense |
| Shareholder transfers | `ST(t) · l(t)` — nil outside a declaration month — plus `CB_fb/9` on claims, which arises whenever a claim does |

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** — no public UK with-profits lapse experience was
retrieved; the shapes are rationalized from the product's incentive structure, and
dynamic option-exercise modeling is a regulatory expectation for the BEL [R7].

- **Base surrender**: UWP bond 5% p.a. flat; CWP 5%/4%/3%/2%+ (class (c) table). The
  table is keyed by the contractual **policy year**, the 1-based label, so month `t`
  reads row `t // 12 + 1` and policy years past the table take its last row. The rate is
  annual and the projection decrements by `w_m = 1 − (1 − w)^(1/12)` **[std]**.
- **MVR deterrent**: `w(t) = w_base(t) · 0.6` while `MVR(t) > 0` **[std]** — an
  active MVR penalizes exit, and firms may consider exit volumes in setting MVRs
  within the COBS bound [R1 COBS 20.2.16AR](#uklib-with_profits-r1). A diffuse tilt, so
  it multiplies the annual rate.
- **Guarantee-imminent suppression**: `w(t) = w_base(t) · 0.8` in the twelve months
  before a guarantee date **[std]** (waiting for the MVR-free window). Also a tilt on
  the annual rate.
- **Guarantee-date encashment**: an additional `ε = 7.5%` **[std]** of the survivors of
  the guarantee-date **month** `12k − 1`, and only when `FV(t) > AS(t)` (the guarantee
  is in the money), so that
  `w_m(t) = 1 − (1 − w_m,ordinary(t))(1 − ε)`. MVR-free encashment is rationally
  exercised precisely in that state and worth nothing otherwise, so the gate is not
  optional: applying it unconditionally invents anti-selection where there is none.

  This is the one place where the monthly grid changes an assumption's **shape** rather
  than its frequency, and deliberately. On an annual grid the exercise could only be a
  `× 2.5` multiplier on the whole guarantee-date year's surrender rate **[std]**, which
  spreads MVR-free exits across eleven months in which the window is shut. Here it falls
  in the month the option is actually open, at a rate set so that a guarantee-date year
  still sheds about the proportion the annual multiplier shed. Neither figure is
  measured — no public UK with-profits experience was retrieved — and both are
  rationalized from the incentive structure alone.
- **Withdrawal utilisation**: withdrawing bond cells take the full 5%
  MVR-free/tax-deferred allowance, a twelfth of it each month **[std]**; utilisation 30%
  of policies **[std]** (allowance context [S10] [REG-R15]).
- **GAO take-up**: 90% when in-the-money by >10%, else 30% **[std]** [unverified].
- **Paid-up conversion (CWP)**: excluded from base **[std]**; where modeled, benefits
  reduce per policy terms and future bonuses may or may not accrue [S4], and asset
  shares may need separate treatment for altered policies [S6].

---

## Worked example

Anchor UWP bond cell (product-spec (14)): £25,000 single premium; `U = 25,000`
units at a seed price of `£1.0000`; five declarations, one at the end of each of the
first five policy years, give an opening price of `1.02^5 = 1.104081` and an opening
face value of `£27,602.02`. The cell is in force at duration 5, so it is projected from
`t = 60` — the first month of its sixth policy year — and the asset share, the smoothed
payout and the unit price are the balances that month **opens** with.
Worked-example state **[std]**: `AS = £30,000.00`, `S = £29,500.00`.
Parameters: `c_amc = 1.00%` p.a., `c_g = 0.10%` p.a., `q(60) = 0.005` p.a.
(illustrative of the class (c) proxy **[std]**), `g_db = 1.01`, `σ = 10%` year on year.
No premium and no withdrawals in the year. Two return scenarios **[std]**:
A: `r = +7.0%` p.a.; B: `r = −15.0%` p.a. (declared bonus cut to 1.00%, the maximum
normal reduction [S1] [S7]).

The example projects **the sixth policy year, months `t = 60 … 71`**, and the
declaration falls at the end of `t = 71`. Monthly rates:

| Rate | Scenario A | Scenario B |
|---|---|---|
| `r_m = (1+r)^(1/12) − 1` | +0.565415% | −1.345195% |
| `c_amc,m = 1 − (1−c_amc)^(1/12)` | 0.083718% | 0.083718% |
| `c_g,m = 1 − (1−c_g)^(1/12)` | 0.008337% | 0.008337% |
| `q_m = 1 − (1−q)^(1/12)` | 0.041762% | 0.041762% |
| cap bounds `(1∓σ)^(1/12)` | 0.9912584 / 1.0079741 | 0.9912584 / 1.0079741 |

Over the twelve months, and then the closing month `t = 71`:

| Step | Quantity | Scenario A (r = +7.0%) | Scenario B (r = −15.0%) |
|---|---|---|---|
| 0 | Opening `AS` / `FV` at `t = 60` | 30,000.00 / 27,602.02 | 30,000.00 / 27,602.02 |
| 3–4 | AMC taken over the twelve months | 311.10 | 274.93 |
| 4 | Guarantee charge taken over the twelve months | 30.98 | 27.38 |
| 6 | Mortality charge taken over the twelve months | 0.00 | 4.60 |
| 3–4 | `AS` after return and charges in month 71 | 31,747.19 | 25,216.50 |
| 5 | Declared bonus `b` for the policy year | 2.00% | 1.00% |
| 5 | `Q(71)`; `FV(71) = 25,000 · Q(71)` | 1.126163; 28,154.07 | 1.115122; 27,878.05 |
| 5 | Cost of bonus `CB = b · FV(70)` | 552.04 | 276.02 |
| 5 | Shareholder transfer `ST = CB/9` | 61.34 | 30.67 |
| 5 | Asset share after `ST` | 31,685.86 | 25,185.83 |
| 6 | `MC = q_m · max(0, 1.01·FV(71) − AS)` in month 71 | 0.00 | 1.24 |
| 6 | **`AS(71)`** | **31,685.86** | **25,184.59** |
| 7 | `S_cap`: clamp against `S(70)` at the monthly bounds | 31,685.86 (within) | 26,846.96 (floor binds) |
| 7 | `S(71)`: corridor clamp to [0.8, 1.2]·AS | 31,685.86 | 26,846.96 (within corridor) |
| 7 | Final bonus `FB = max(0, S − FV)` | 3,531.79 | 0.00 |
| 7 | `MVR = min(max(0, FV−S), max(0, FV−AS))` | 0.00 | min(1,031.08, 2,693.46) = 1,031.08 |
| 8 | Guarantee-date payout `FV + FB` (no MVR) | 31,685.86 | 27,878.05 (guarantee bites) |
| 8 | Surrender payout `FV + FB − MVR` | 31,685.86 | 26,846.96 |
| 8 | Death payout `1.01 · (FV + FB)` | 32,002.72 | 28,156.83 |
| 8 | Smoothing/guarantee cost on exit (payout − AS): guarantee-date / surrender | 0.00 / 0.00 | 2,693.46 / 1,662.37 |

The Step column is the processing-order step, not the time index: the closing rows are
month `t = 71` and the three aggregate rows are sums over `t = 60 … 71`. The closing
quantities are the row `result_payout()` publishes at `t = 71`; the intermediate steps
are `asset_share_at(71, …)` and the per-claim exit costs are
`smoothing_cost_pp(71, kind)`. Note that the payout, the final bonus and the MVR exist
in **every** month of the year, not only its last: a claim in month 65 is paid on
month 65's smoothed payout, which is what a monthly grid is for.

Checks: the asset share ends the year at 105.6% of its opening value in A and 83.9% in
B; the smoothed payout ends at 107.4% and 91.0%, both inside the ±10% year-on-year band
the monthly cap compounds to. Scenario B's cap binds in eleven of the twelve months —
not the twelfth, because the first month's asset share was still above the floor — which
is why the payout lands a little above the 90.0% an annual step would produce. The MVR
(1,031.08) is below the COBS bound `FV − AS = 2,693.46` [R1]; the guarantee-date exit
pays full face value with the 2,693.46 excess over asset share borne by the estate's
guarantee/smoothing account [S1] [S4]. On the scenario A guarantee-date claim an
additional shareholder transfer of `FB/9 = 392.42` accrues at payment (90:10 on the
final bonus, ST section). Scenario A pays 100.0% of `AS(71)`; scenario B's surrender
pays 106.6% — both within the 80–120% corridor [S1] [R1].

CWP maturity illustration (one line): the twenty-five declarations of a 25-year
endowment close at the end of month `12n − 1 = 299`, where
`G(299) = 20,000 · 1.015^25 = £29,018.91` — one declaration per policy year and
twenty-five of them, which is the arithmetic a monthly implementation gets wrong if it
compounds `b` monthly. With smoothed maturity target `S = £34,000.00` **[std]**,
`TB = 34,000.00 − 29,018.91 = £4,981.09` — 14.7% of the payout in non-guaranteed
form, consistent with the substantial-final-bonus philosophy [S1]; the associated
shareholder transfer at payment is `TB/9 = £553.45` **[std]** measurement. (The shipped
endowment cell's own projection reaches a smoothed payout below the guarantee, so the
guarantee bites and the terminal bonus is nil; the £34,000 above is the notes'
illustration of the mechanic, not that cell's output.)

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers are
cited, not reproduced.

- **Solvency UK BEL.** Technical provisions = best estimate + risk margin; the best
  estimate is the probability-weighted, discounted value of all cash flows [R7]
  [REG-R1]. For with-profits, the BEL includes **future discretionary benefits** —
  future regular and final bonuses expected under PPFM-consistent discretion —
  because expected payments count "whether or not ... contractually guaranteed",
  with the surplus-funds carve-out for the unallocated estate [R7] [R8]. The
  With-Profits Actuary must advise whether the FDB assumptions are consistent with
  the PPFM [R5]. Guarantees and options (unit-price floors, guarantee dates, GAOs)
  must be valued market-consistently with dynamic policyholder behavior [R7] —
  stochastic-on-deterministic use of this model.
- **Risk margin.** Post-reform cost-of-capital method: CoC 4%, risk taper λ = 0.9
  (floor 0.25) for long-term business [R7] [REG-R4]. Cited-not-specified.
- **Ring-fencing and estate.** With-profits fund assets must cover the fund's
  liabilities [R6]; surplus funds (the estate) are own funds, excluded from
  technical provisions [R8]. TMTP may apply to pre-2016 back-books [R7] [REG-R3].
- **Matching adjustment.** The guaranteed element of a with-profits immediate or
  deferred annuity can qualify as an MA "eligible element" [REG-R2] — relevant only
  to the annuity variations, not the composite cells.
- **IFRS 17.** UK-adopted IFRS 17 (effective 1 January 2023) applies to
  IFRS-reporting insurers [REG-R38]; with-profits contracts are direct-participation
  business measured under the variable fee approach [unverified — standard text not
  fetched]. The fulfilment-cash-flow engine is this same projection.
- **Conduct overlay.** Payout machinery in any valuation must respect the COBS
  target-range, MVR-bound and required-percentage rules [R1] — they are constraints
  on the FDB discretion, not just conduct background.

---

## Key sensitivities and model risks

1. **Fund return / equity backing.** Asset shares, final bonuses and MVR incidence
   all key off `r(t)`; the observed strategy ceiling is a benchmark equity backing
   ratio of 75% (one insurer's EBR upper limit [S5]). Deterministic base runs
   materially understate guarantee costs (convexity) — the central model risk here
   [R7] [R13].
2. **Bonus discretion path.** The split of payout between hardened regular bonus and
   final bonus changes guarantee costs without changing the target payout: a higher
   `θ` or faster `κ` hardens guarantees. The [std] parametrization is a genuine
   modeling choice with no public calibration.
3. **Smoothing parameters.** The ±10% cap and 80–120% corridor determine how much of
   a market shock passes to payouts immediately; firms' actual limits vary (5%–15%
   observed [S1] [S5] [S7]) and can be suspended under solvency stress [S5].
4. **MVR application.** Whether the discretion is exercised promptly (and the review
   buffer — one consolidator tolerates up to 10% return variation before an extra MVR
   review [S4]) drives surrender strain in down markets.
5. **Surrender behavior at guarantee dates.** The guarantee-date spike multiplier and
   MVR deterrent are unverified [std] shapes; anti-selective exit when guarantees are
   in the money is the dominant behavioral risk (dynamic assumptions required [R7]).
6. **Mortality proxy.** The 60%-of-ONS basis is a placeholder; insured with-profits
   experience differs by class and era, and current CMI tables are
   subscriber-restricted [R10] [REG-R22] [REG-R32].
7. **Expense and charge caps.** Where actual expenses exceed capped charges (1% caps
   [S1] [S5]) the excess falls to the estate — a fund-level, not policy-level, cash
   flow this single-policy model does not capture.
8. **GAO interest-rate exposure.** Legacy GAO cells are long interest-rate optionality
   [S4]; omitting the stochastic layer understates their cost materially.
9. **Estate interactions.** Reattributions, special bonuses and mutual profit
   distributions [S5] [S6] are fund-level discretions outside the base model; scenario
   overlays should treat them as management actions.
10. **Data-provenance limits.** Snapshot bonus rates, EGRs and MVR scales are [std]
    placeholders by design (declarations are not in PPFMs — research gap); a
    calibration pass against current bonus declarations is required before any
    quantitative use.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-with_profits-r1
[R10]: #uklib-with_profits-r10
[R13]: #uklib-with_profits-r13
[R2]: #uklib-with_profits-r2
[R5]: #uklib-with_profits-r5
[R6]: #uklib-with_profits-r6
[R7]: #uklib-with_profits-r7
[R8]: #uklib-with_profits-r8
[REG-R1]: #uklib-reg-r1
[REG-R15]: #uklib-reg-r15
[REG-R17]: #uklib-reg-r17
[REG-R2]: #uklib-reg-r2
[REG-R22]: #uklib-reg-r22
[REG-R24]: #uklib-reg-r24
[REG-R3]: #uklib-reg-r3
[REG-R30]: #uklib-reg-r30
[REG-R32]: #uklib-reg-r32
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
