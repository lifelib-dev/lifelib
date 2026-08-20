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
- **Projection frequency.** Annual **[std]**. Rationale: bonus declarations, the
  governing discretion cycle, are annual [S1] [S4] [S7]; sub-annual mechanics (daily
  unit pricing [S4], PruFund daily/quarterly smoothing [S9] [S11]) are compressed to
  annual equivalents in the base model, with the PruFund module noting its native
  daily/quarterly grid.
- **Timing conventions [std].** Premiums and partial withdrawals at the start of the
  policy year (BOY); fund return accrues over the year; proportional charges, bonus
  declaration, shareholder transfer and mortality charge at end of year (EOY), in the
  processing order below; claims and decrements at EOY after declaration.
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
| `asset_share_0` | currency (in-force cells) | 30,000 |
| `smoothed_payout_0` | currency (`S(0)` benchmark for the y/y cap) | 29,500 |
| `guarantee_dates` | list of anniversaries (MVR-free) | {10} |
| `mvr_free_wd_rate` | % of original premium p.a. | 5% |
| `tax_basis` | enum {life_net, pension_gross} [S1] [REG-R17] | life_net |
| `gao_flag` / `gao_rate` | bool / annuity per £1 cash | false / — |
| `mutual_dist_flag` | bool (mutual profit distribution variation [S6]) | false |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `AS(t)` | Asset share at end of year t [S1] [R8] | annual recursion |
| `Q(t)` | With-profits unit price (UWP); never decreases | EOY declaration |
| `FV(t)` | Unit face value `U(t)·Q(t)` (UWP) | EOY |
| `G(t)` | Guaranteed benefit `SA` + attaching reversionary bonuses (CWP) | EOY declaration |
| `b(t)` | Declared regular bonus rate for year t | EOY, setting rule |
| `S(t)` | Smoothed target payout (after y/y cap and corridor) | EOY |
| `FB(t)` | Final (terminal) bonus payable on claim in year t | EOY |
| `MVR(t)` | Market value reduction on non-guaranteed exits | EOY |
| `CB(t)` | Cost of bonus recognized in year t | EOY |
| `ST(t)` | Shareholder transfer = `CB(t)/9` (90:10) | EOY |
| `SM(t)` | Smoothing account balance (within estate) | on exits |
| `CumGC(t)` | Cumulative guarantee-charge deductions (for the 2% lifetime cap [S1]) | annual |
| `l(t)` | In-force probability at end of year t | EOY decrements |

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
| `t` | policy year index (1, 2, …); `x` = age at entry (ANB) |
| `P(t)` | premium received at BOY t |
| `W(t)` | partial withdrawals paid at BOY t |
| `E(t)` | insurer maintenance expense in year t (£30 × 1.03^(t−1) **[std]**) |
| `r(t)` | earned fund return in year t (net basis per `tax_basis`) |
| `c_amc`, `c_g` | AMC 1.00% p.a.; guarantee/smoothing charge 0.10% p.a. **[std]** |
| `q(x+t−1)` | mortality rate for year t (class (c) basis) |
| `w(t)` | surrender/lapse rate for year t (incl. dynamic multipliers) |
| `MC(t)` | mortality charge to the asset share in year t [S1] |
| `b(t)`, `b_rev(t)` | declared regular / reversionary bonus rate for year t |
| `Q(t)`, `U(t)`, `FV(t)` | unit price, units, face value (UWP); `FV = U·Q` |
| `G(t)` | guaranteed benefit (CWP): SA + attaching bonuses |
| `S(t)` | smoothed target payout after cap and corridor |
| `FB(t)`, `MVR(t)`, `TB(t)` | final bonus, market value reduction, terminal bonus |
| `CB(t)`, `ST(t)` | cost of bonus; shareholder transfer = CB/9 |
| `θ, κ, σ` | guarantee-fill target 0.80; bonus-smoothing speed 0.5; y/y cap 10% **[std]** |
| `g_db` | UWP death benefit factor 1.01 **[std]** |
| `i_sv` | CWP surrender-basis discount rate 4.0% **[std]**; `v_sv = 1/(1+i_sv)` |
| `n` | CWP term (25); `h` = UWP bonus-setting horizon (10 years **[std]**) |
| `l(t)` | in-force probability at end of year t; `l(0) = 1` |

### Annual processing order [std]

1. **BOY**: premium `P(t)` received; UWP units purchased: `U(t) = U(t−1) + α·P(t)/Q(t−1)`
   with allocation `α = 100%` (product-spec (7)).
2. **BOY**: partial withdrawals `W(t)` paid (MVR applies if outside the MVR-free
   allowance); asset share reduced pro rata to the pre-MVR policy value [S1].
3. Fund return `r(t)` accrues on the asset share balance.
4. **EOY**: proportional charges: multiply by `(1 − c_amc − c_g)`; accumulate
   `CumGC`; set `c_g = 0` once `CumGC ≥ 2% × AS(t)` [S1 cap; mechanics **[std]**].
5. **EOY**: regular bonus `b(t)` declared per the setting rule below;
   `Q(t) = Q(t−1)(1+b(t))` (UWP) or `G(t) = G(t−1)(1+b_rev(t))` (CWP);
   cost of bonus `CB(t)` computed on pre-declaration values; shareholder transfer
   `ST(t) = CB(t)/9` deducted from the asset share [S5] [R8]; product-spec (2).
6. **EOY**: mortality charge `MC(t) = q(x+t−1) · max(0, DB_g(t) − AS_pre(t))`
   deducted, where `DB_g` is the guaranteed death benefit (`g_db·FV(t)` UWP; `G(t)`
   CWP) and `AS_pre` the balance after step 5 [S1 formula: mortality rate × (death
   benefit − policy value); guaranteed-only DB in the sum at risk **[std]**].
7. **EOY**: smoothed payout `S(t)` computed (cap, then corridor); `FB`/`TB`/`MVR`
   derived.
8. **EOY**: claims paid — deaths at `q`, surrenders at `w`, maturity at `t = n`;
   smoothing account posts `(payout − AS(t))` per exiting unit of probability.
9. Survivorship: `l(t) = l(t−1) · (1 − q(x+t−1)) · (1 − w(t))` (maturity year:
   survivors mature).

### Asset share recursion (core)

```
AS(t) = [ AS(t−1) + P(t) − W_AS(t) ] · (1 + r(t)) · (1 − c_amc − c_g)
        − ST(t) − MC(t) + M(t)
```

Component bases (each item as recorded for the retrospective accumulation
[S1] [S2] [S4] [S5] [S6] [S7] and codified in PRA Surplus Funds 3.3 [R8]):

- **Premiums `P(t)`** — accumulated in full; explicit charges are taken via `c_amc`
  rather than allocation deductions **[std]** (product-spec (7)).
- **`W_AS(t)`** — asset-share reduction for BOY withdrawals, pro rata to the pre-MVR
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
  applicable [S1] [S5] [R8]; `M(t) = 0` in the base model **[std]** (product-spec (3)).

### Regular bonus setting rule [std]

The PPFM principles are: rates set from projections; gradual changes (±1% p.a.
normal); keep a substantial proportion of the payout in final-bonus form; full
discretion to declare zero [S1] [S7]. The reference parametrization:

1. Project the asset share to the horizon at the expected net return
   `r_e = r_base − c_amc − c_g` **[std]**:
   `AS_proj = AS(t) · (1+r_e)^(m) + future premiums accumulated to the horizon at r_e`,
   with `m = n − t` (CWP) or `m = h = 10` (UWP whole-of-life bond).
2. Supportable rate: the level bonus rate that grows the guarantee to the
   guarantee-fill target θ = 80% of the projected asset share:
   - UWP: `b_supp = [ θ·AS_proj / FV(t) ]^(1/m) − 1`
   - CWP: `b_supp = [ θ·AS_proj / G(t) ]^(1/m) − 1`
3. Smoothed declaration with the ±1% discipline [S1] [S7]:
   `b(t) = max( 0, b(t−1) + clamp( κ·(b_supp − b(t−1)), −0.01, +0.01 ) )`, κ = 0.5
   **[std]**.

The base projection holds the snapshot rates (2.00% UWP / 1.50% CWP) level; the rule
above is the revision module for scenario work.

### Smoothed payout, final bonus, terminal bonus

Raw target = the unsmoothed asset share (payout target 100% of asset share
[S5] [S7] [S8] [R1]). Apply the year-on-year cap, then the corridor:

```
S_raw(t)  = AS(t)
S_cap(t)  = clamp( S_raw(t), (1−σ)·S(t−1), (1+σ)·S(t−1) )      σ = 10%  [S1]
S(t)      = clamp( S_cap(t), 0.80·AS(t), 1.20·AS(t) )                    [S1][R1]
```

The corridor implements the 80–120% target range deterministically at model-point
level; the ≥90%-of-policies test [S1] [R1] is a portfolio property, out of scope for a
single-policy model **[std]**.

- UWP final bonus: `FB(t) = max(0, S(t) − FV(t))`; guarantee-event payout
  `FV(t) + FB(t)`; death payout `g_db · (FV(t) + FB(t))` [S5: no MVR on death].
- CWP terminal bonus: `TB(t) = max(0, S(t) − G(t))`; maturity payout `G(n) + TB(n)`;
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

### Cost of bonus and shareholder transfer (90:10 mechanics)

`ST(t) = CB(t) / 9` — one-ninth of the cost of bonus, so that shareholders receive
10% of each 90:10 distribution (product-spec (2); components [S1] [S5] [S8] [R1]).
Measurement of `CB` **[std]**:

- UWP regular bonus: `CB_reg(t) = b(t) · FV(t−1)` — the face-value uplift delivered
  by the declaration.
- CWP reversionary bonus: `CB_reg(t) = ΔG(t) · v_sv^(n−t)` with
  `ΔG(t) = G(t) − G(t−1)` — the declared addition discounted to the declaration date
  (survivorship discount omitted **[std]** simplification).
- Final/terminal bonus: `CB_fb(t) = (FB or TB paid on claims in year t)`, recognized
  at payment.

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

### Cash flow outputs (per policy year t, probability-weighted by `l`)

| Output | Formula |
|---|---|
| Premium income | `P(t) · l(t−1)` |
| Death claims | `q(x+t−1) · l(t−1) · DeathPayout(t)` |
| Surrender claims | `w(t) · l(t−1) · (1 − q) · SurrenderPayout(t)` |
| Maturity claims | `l(n) · (G(n) + TB(n))` (CWP, year n) |
| Partial withdrawals | `W(t) · l(t−1)` |
| Maintenance expenses | `E(t) · l(t−1)` |
| Shareholder transfers | `ST(t) · l(t−1)` plus `CB_fb/9` on claims |

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** — no public UK with-profits lapse experience was
retrieved; the shapes are rationalized from the product's incentive structure, and
dynamic option-exercise modeling is a regulatory expectation for the BEL [R7].

- **Base surrender**: UWP bond 5% p.a. flat; CWP 5%/4%/3%/2%+ (class (c) table).
- **MVR deterrent**: `w(t) = w_base(t) · 0.6` while `MVR(t) > 0` **[std]** — an
  active MVR penalizes exit, and firms may consider exit volumes in setting MVRs
  within the COBS bound [R1 COBS 20.2.16AR](#uklib-with_profits-r1).
- **Guarantee-date spike**: `w(t) = w_base(t) · 2.5` in a guarantee-date year
  **[std]** — MVR-free encashment is rationally exercised when `FV(t) > AS(t)`
  (guarantee in the money); apply the multiplier only in that state.
- **Guarantee-imminent suppression**: `w(t) = w_base(t) · 0.8` in the year before a
  guarantee date **[std]** (waiting for the MVR-free window).
- **Withdrawal utilisation**: withdrawing bond cells take the full 5%
  MVR-free/tax-deferred allowance; utilisation 30% of policies **[std]**
  (allowance context [S10] [REG-R15]).
- **GAO take-up**: 90% when in-the-money by >10%, else 30% **[std]** [unverified].
- **Paid-up conversion (CWP)**: excluded from base **[std]**; where modeled, benefits
  reduce per policy terms and future bonuses may or may not accrue [S4], and asset
  shares may need separate treatment for altered policies [S6].

---

## Worked example

Anchor UWP bond cell (product-spec (14)): £25,000 single premium; `U = 25,000`
units at `Q(0) = £1.0000`; five declarations at 2.00% give
`Q(5) = 1.02^5 = 1.104081`, `FV(5) = £27,602.02`. Worked-example state **[std]**:
`AS(5) = £30,000.00`, `S(5) = £29,500.00`. Year-6 parameters: `c_amc = 1.00%`,
`c_g = 0.10%`, `q(60) = 0.005` (illustrative of the class (c) proxy **[std]**),
`g_db = 1.01`, `σ = 10%`. No premium, no withdrawals in year 6. Two return
scenarios **[std]**: A: `r = +7.0%`; B: `r = −15.0%` (declared bonus cut to 1.00%,
the maximum normal reduction [S1] [S7]).

| Step | Quantity | Scenario A (r = +7.0%) | Scenario B (r = −15.0%) |
|---|---|---|---|
| 0 | `AS(5)` / `FV(5)` | 30,000.00 / 27,602.02 | 30,000.00 / 27,602.02 |
| 3 | After fund return: `30,000 · (1+r)` | 32,100.00 | 25,500.00 |
| 4 | After charges `× (1 − 0.011)` | 31,746.90 | 25,219.50 |
| 5 | Declared bonus `b(6)` | 2.00% | 1.00% |
| 5 | `Q(6)`; `FV(6) = 25,000 · Q(6)` | 1.126162; 28,154.06 | 1.115122; 27,878.04 |
| 5 | Cost of bonus `CB = b(6) · FV(5)` | 552.04 | 276.02 |
| 5 | Shareholder transfer `ST = CB/9` | 61.34 | 30.67 |
| 5 | Asset share after `ST` | 31,685.56 | 25,188.83 |
| 6 | `MC = q · max(0, 1.01·FV(6) − AS)` | 0.00 | 0.005 × 2,967.99 = 14.84 |
| 6 | **`AS(6)`** | **31,685.56** | **25,173.99** |
| 7 | `S_cap`: clamp(AS, 0.9·29,500, 1.1·29,500) | 31,685.56 (within) | 26,550.00 (floor binds) |
| 7 | `S(6)`: corridor clamp to [0.8, 1.2]·AS | 31,685.56 | 26,550.00 (within corridor) |
| 7 | Final bonus `FB = max(0, S − FV)` | 3,531.50 | 0.00 |
| 7 | `MVR = min(max(0, FV−S), max(0, FV−AS))` | 0.00 | min(1,328.04, 2,704.05) = 1,328.04 |
| 8 | Guarantee-date payout `FV + FB` (no MVR) | 31,685.56 | 27,878.04 (guarantee bites) |
| 8 | Surrender payout `FV + FB − MVR` | 31,685.56 | 26,550.00 |
| 8 | Death payout `1.01 · (FV + FB)` | 32,002.42 | 28,156.82 |
| 8 | Smoothing/guarantee cost on exit (payout − AS): guarantee-date / surrender | 0.00 / 0.00 | 2,704.05 / 1,376.01 |

Checks: scenario B surrender pays exactly the smoothed target (−10.0% y/y, the [S1]
cap); the MVR (1,328.04) is below the COBS bound `FV − AS = 2,704.05` [R1]; the
guarantee-date exit pays full face value with the 2,704.05 excess over asset share
borne by the estate's guarantee/smoothing account [S1] [S4]. On the scenario A
guarantee-date claim an additional shareholder transfer of `FB/9 = 392.39` accrues at
payment (90:10 on the final bonus, ST section). Scenario A pays 100.0% of `AS(6)`;
scenario B's surrender pays 105.5% of `AS(6)` — both within the 80–120% corridor
[S1] [R1].

CWP maturity illustration (one line): at `n = 25`, `G(25) = 20,000 · 1.015^25 =
£29,018.91`; with smoothed maturity target `S(25) = £34,000.00` **[std]**,
`TB = 34,000.00 − 29,018.91 = £4,981.09` — 14.7% of the payout in non-guaranteed
form, consistent with the substantial-final-bonus philosophy [S1]; the associated
shareholder transfer at payment is `TB/9 = £553.45` **[std]** measurement.

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
