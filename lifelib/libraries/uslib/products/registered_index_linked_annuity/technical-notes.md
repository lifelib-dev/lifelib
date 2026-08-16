# Technical Notes

**Status:** Draft, 2026-08-04 (cited sources accessed 2026-08-04, except the AP&P Manual
appendix items **R151–R157**, accessed 2026-08-06 — see `sources.md`).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite product defined in `product-spec.md` (same directory). This is
not any single insurer's product. [S#]/[R#] tags refer to the source list in
`_research/registered-index-linked-annuity.md`; [REG-R#] tags refer to the **shared
cross-product numbering space, which now runs R1–R157** with most of the
**R73–R149** block unused, curated at
`references/regulatory-and-actuarial-references.md` (R1–R34 from
`_research/regulatory-actuarial.md`, R35–R72 from
`_research/regulatory-actuarial-annuities.md`). **[std]** marks standardizations
introduced for the reference implementation. Parameter values are identical to those in
`product-spec.md`; the mechanics anchor is the Brighthouse Shield Level II prospectus,
Appendix F [S2].

**Read this first.** A conforming RILA model **requires an option-pricing routine and a
market-data interface** (discount curve, implied volatility surface, dividend yield) — not
as a refinement but as a precondition. Actuarial Guideline LIV makes the Interim Value —
the value at which *every* mid-term withdrawal, surrender, death benefit, annuitization,
transfer and fee deduction settles — the market value of a hypothetical replicating
portfolio of European options plus a fixed income proxy [R2], and the source prospectuses
implement exactly that with Black-Scholes [S2] [S6] or an equivalent market-standard
European model [S4]. No other product in this library has a contractual value that cannot
be computed without a derivatives pricer. Architecturally the crediting engine, the
interim-value engine and the market-data provider are three separate components, and the
interim-value engine is called at every projection step for every open option.

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows (premium, surrender and withdrawal
  payments, death claims, annuitization outgo, expenses) for a single-contract model
  point. Reserves are not computed (see *Valuation and reserve pointers*).
- **Projection frequency.** **Monthly** **[std]**. The contractual interim value is a
  *daily* quantity [S2] [S4] [S5] [S6]; the model evaluates it at each month end. Terms are
  integer years, the withdrawal-charge schedule runs by complete contract years and
  free-withdrawal limits reset annually [S1] [S2], so a monthly grid captures every
  contractual boundary. A daily sub-grid is needed only for a path-dependent Performance
  Lock election module [S2].
- **Timing convention.** Month index `t = 0, 1, 2, …` denotes **month ends**, `t = 0` being
  the Issue Date. Within a month **[std]**: market state, then term-end crediting (if the
  month end is a Term End Date), then interim values, then contract-holder transactions,
  then decrements. Full ordering below.
- **Age basis.** **Age nearest birthday (ANB)** **[std]** — the 2012 IAM Period Table
  printed in Model #821 and VM-M is stated age nearest birthday [REG-R59], and VM-21
  prescribes percentages of the 2012 IAM Basic Table with Scale G2 for prudent-estimate
  mortality on contracts with **VAGLBs and roll-up GMDBs** [REG-R35] [REG-R59] — a class
  that does *not* include the return-of-premium GMDB modeled here, so the prudent-estimate
  basis is a scope reference, not a prescription for this design.
- **Model points.** Single-contract model points on an expected (probability-weighted)
  basis: in-force factors multiply per-contract cash flows. A model point is one contract
  holding one index-linked option; multi-option contracts are a vector of options sharing
  one contract-level decrement and one contract-level guarantee base.
- **Index basis.** All representative indices are **price return** [S1] [S2], so the dividend
  yield is a live pricing input — omitting it overprices every call in the portfolio.
- **Rounding.** Full precision internally; cash flows reported to cents **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell **[std]**) |
|---|---|---|
| `issue_age` | int (ANB) | 60 |
| `sex` | enum {M, F} | M |
| `issue_date` | date | 2026-01-01 |
| `single_premium` | currency | 100,000 |
| `option_id` | int (index-linked bucket) | 1 |
| `index_code` | enum {SPX, RTY, MXEA, NDX} — price return | SPX |
| `term_years` `T` | int {1, 3, 6} | 6 |
| `buffer` `b` | rate | 0.10 |
| `crediting_type` | enum {CAP, STEP, EDGE} (FLOOR module optional) | CAP |
| `declared_cap` `c` | rate (NGE, reset each term) | 1.00 |
| `declared_step` `s` | rate (NGE) | 0.08 |
| `declared_edge` `e` | rate (NGE) | 0.06 |
| `participation` `PR` | rate (NGE) | 1.00 |
| `guar_min_cap(T)` | rate | 0.02 / 0.06 / 0.08 for T = 1 / 3 / 6 [S2] |
| `term_start_index` `I_s` | index level | 100.00 (normalized) |
| `term_start_mvr` `r_0` | annual effective rate | 0.0400 |
| `investment_amount` `IA` | currency | 100,000 |
| `fixed_account_value` | currency | 0 |
| `holding_account_value` | currency | 0 |
| `rop_base` | currency (GMDB return-of-premium base) | 100,000 |
| `wc_schedule` | vector by complete contract year | (0.07, 0.07, 0.06, 0.05, 0.04, 0.03, 0.00) [S1] [S2] |
| `lock_flag` | bool (Performance Lock exercised this term) | false |
| `lock_value` | currency (valid when `lock_flag`) | — |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `IA_k(t)` | Investment Amount (AG 54 "Index Strategy Base") of option k | term-end crediting; proportional withdrawal reduction |
| `V_k(t)` | Interim Value of option k at month end t | every month (option repricing) |
| `beta_k` | Initial option budget per unit of notional for the current term | at each Term Start Date |
| `I(t)` | Index level | every month (scenario input) |
| `r(t)` | Market Value Rate (CMT at the term's maturity) | every month (scenario input) |
| `FA(t)`, `HA(t)` | Fixed Account / Holding Account values | monthly accrual |
| `AV(t)` | Account Value = sum of V_k(t) + FA(t) + HA(t) | monthly |
| `ROP(t)` | Return-of-premium GMDB base | proportional reduction on withdrawal |
| `FW_used(y)` | Free withdrawal amount consumed in contract year y | on withdrawal; resets annually |
| `AV_anniv(y)` | Account Value at the prior Contract Anniversary (free-withdrawal base) | annually [S1] [S2] |
| `cy(t)` | Complete contract years since issue = floor(t/12) | monthly |
| `tau_k(t)` | Years remaining in option k's term = (days remaining)/365 [S2] | monthly |
| `l(t)` | In-force probability at end of month t; `l(0) = 1` | monthly decrements |
| `lock_flag_k`, `LV_k(t)` | Performance Lock state and locked value | on election |

---

## Assumption inputs

Three assumption classes are distinguished, plus a fourth block that is peculiar to this
product: the contractual formula itself consumes market data.

### (a) Contractual / guaranteed elements

| Input | Value | Basis |
|---|---|---|
| Buffer `b` (guaranteed for the term) | 0.10 | [S1] [S2] |
| Term length `T` | 6 years (menu 1/3/6) | [S1] [S2]; menu **[std]** |
| Minimum guaranteed Cap Rate | 2% / 6% / 8% for T = 1 / 3 / 6 | [S1] [S2] |
| Minimum guaranteed Step Rate, Edge Rate | 2%, 2% | [S2] |
| Minimum guaranteed interest rate (Fixed / Holding Account) | 1% | [S1] [S2] |
| Withdrawal charge schedule `wc(cy)` | 7, 7, 6, 5, 4, 3, 0 % | [S1] [S2] |
| Free Withdrawal Amount | 0 in contract year 1; thereafter 10% of `AV_anniv`, non-cumulative | [S1] [S2] |
| Death benefit | max(Account Value, ROP base) for issue ages ≤ 80 | [S2] |
| Value used for every mid-term transaction | Interim Value | [S1] [S2] [S4] [S6] |
| Interim value formula | family (a), straight-line budget amortization, CMT discount | [S2]; selection **[std]** |
| Transfer Period | 5 calendar days after the Contract Anniversary coinciding with a Term End Date; `V = IA` during it | [S1] [S2] |
| Maturity Date | later of (anniversary after oldest owner's age 90) and 10 years | [S2] |

### (b) Insurer-declared current elements (NGEs, revisable under ASOP No. 2 [R5] [REG-R26])

| Input | Snapshot value | Basis |
|---|---|---|
| Declared Cap Rate, T = 6 / 3 / 1 | 100% / 55% / 12% | **[std]** — no current rate sheet was retrievable (both insurer rate pages returned HTTP 403 / WAF rejection; research gap 1). Observed *illustrative* prospectus values: 10% (1yr) [S1]; 75% (3yr, 10% buffer) [S3]; 12% (1yr) and 100% (6yr) [S6]; 60% with 110% participation (6yr, 20% buffer) [S4] |
| Declared Step Rate (1 yr) | 8% | **[std]**; observed illustrative 8% [S1], 5% with 90% participation [S3], 12.5% trigger [S6] |
| Declared Edge Rate (1 yr) | 6% | **[std]** — no Edge value appears in any retrieved document; set below the Step Rate because the Edge design pays down to −b |
| Participation Rate | 100% | [S4] |
| Declared Fixed / Holding Account rate | 3.00% | **[std]** — only the 1% contractual minimum is public [S1] [S2] |
| Trading cost factor `kappa` | 0.10% of the sum of absolute option market values | **[std]** — AG 54 requires a Trading Cost provision [R2] but no prospectus quantifies it (research gap 8); the Academy example implies costs of order 0.1% of option value [R6] |

**NGE redetermination rule [std].** At each Term Start Date the declared cap is the
solution `c` of

    Pi( c ; b, T, sigma, r, q )  =  beta_target(T)
    beta_target(T)               =  1 - ( 1 + y_e - spread ) ^ (-T)

floored at the contractual minimum guaranteed cap [S2], where `Pi(.)` is the per-unit
replicating-portfolio value defined below, `y_e` is the projected earned rate on
supporting assets and `spread` is the target margin (**[std]** 2.22%, the level implied
by the snapshot 6-year cap — see *Worked example*). This is the machinery ASOP No. 2
governs: a determination policy, an NGE framework, NGE scales, policy classes and
periodic review of in-force NGEs [R5]. Base projection holds the snapshot scale level.

### (c) Behavioral and experience assumptions

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Base mortality (deferral period) | **2012 IAM Basic Table** (ANB) — the *unloaded* table underlying the Period Table, VM-M §2.C — with generational Projection Scale G2, `q_x^{2012+n} = q_x^{2012,Basic} x (1 − G2_x)^n` | [REG-R59] |
| Valuation / guaranteed-purchase-rate basis | 2012 IAM **Period** Table with Scale G2 (i.e. the 2012 IAR), `q` rounded to three decimals per 1,000 **from the 2012 period rate each time — never by compounding an already-rounded prior-year rate** | [REG-R59] |
| Mortality A/E | 2020–2024 Individual Payout Annuity Mortality Experience Study (23 parent groups, >80% of sales, 3.1m contract-years, 143,190 deaths), reported against the 2012 IAM **Basic** basis | [REG-R61]; A/E factor **[std]** 100% |
| Deferred-period annuitant mortality | Materially under-evidenced publicly — only a 2011–2015 deferred annuity mortality study and a 2006 analysis are indexed, neither fetched | [REG-R65] [unverified] |
| Base surrender | VA / RILA contract-holder behavior study 2022–2024 (17 companies, ~48% of new premium **for VAs and RILAs**, 11.5m contracts, $1.5tn, >625,000 surrender events) — detailed tables are behind a paid data package | [REG-R64]; reference table **[std]** |
| Charge-expiry shock lapse | Order-of-magnitude anchors only: ~10% (with GLWB) vs ~33% (without) for FIA, ~52%/~56% for fixed-rate deferred | [REG-R62] [REG-R63] [unverified] |
| Withdrawal / partial-surrender utilization | Same VA/RILA study (4m withdrawal transactions, $56.7bn withdrawn) | [REG-R64]; reference rule **[std]** |
| Maintenance expense | $60 per contract per year, inflating 2.5% p.a. | **[std]** |
| Acquisition expense | 6% of premium plus $200 per contract | **[std]** |
| Premium tax | 0% | [S2]; value **[std]** |

**Mortality base — the trap.** Do **not** run best-estimate mortality off the 2012 IAM
*Period* Table. The Period Table (and hence the 2012 IAR) carries the valuation margin
built in at construction — 10% at all ages up to and including 100, grading down 1% per
year above it [REG-R60] — so a 100% A/E applied to the Period Table sets deferral-phase
mortality roughly 10% below the unloaded basis before any experience adjustment. The
experience study reports against the **Basic** table, which is why the base row above is
the Basic table. The payout chassis in `products/immediate_annuity/technical-notes.md`
calibrates the same study to **108.4%** of 2012 IAM Basic projected with G2; that factor is
*payout-annuitant-select* and is deliberately **not** imported here, because the RILA
deferral-phase population is not annuitant-select and public deferred-period annuitant
mortality is thin [REG-R65] [unverified]. Hence the **[std]** 100% A/E, which is a
placeholder, not a measurement.

Reference base annual surrender table **[std]** (shape only; calibration is the user's).
`w_base` is the **un-shocked** annual rate; the charge-expiry shock enters separately as
`M_sc(y)` in the *Total surrender* formula below, so the two are applied multiplicatively
and neither is baked into the other:

| Contract year | 1–6 | 7 | 8+ |
|---|---|---|---|
| `w_base(y)` | 2.0% | 2.0% | 6.0% |
| `M_sc(y)` | 1.0 | 3.0 | 1.0 |

giving a reference year-7 rate of **6.0%** before the moneyness multiplier. Note that this
[std] shape places the shock year and the ultimate at the same level, so the reference
table exhibits no post-shock reversion; it is a shape placeholder and a calibrated run
should separate the two.

Contract year 7 is the first year in which the withdrawal charge is zero [S1] [S2] **and**
the first year following a 6-year Term End Date — the two events coincide on this
chassis, which is why the shock is applied there.

### (d) Market data required by the contractual formula (a RILA-specific input class)

| Input | Snapshot value | Basis |
|---|---|---|
| Market Value Rate curve (CMT, term maturity, linearly interpolated) | 4.00% annual effective, flat | mechanic [S2]; level **[std]** |
| Risk-free rate for option pricing `r` | 4.00% annual effective (`r_cc = ln 1.04 = 3.9221%`) | **[std]** |
| Dividend yield `q` (price-return indices) | 2.00% annual effective (`q_cc = ln 1.02 = 1.9803%`) | **[std]** |
| Implied volatility `sigma` | 20.00%, flat surface | **[std]** |

AG 54 requires these to be "consistent with the observable market prices of derivative
assets over the Index Strategy Term, whenever possible" [R2]. A production implementation
must supply a **surface**, not a scalar: Equitable documents the interpolation procedure
explicitly — quotes are taken for the closest maturities above and below the remaining
time and, for each, the closest moneyness above and below the actual moneyness; then
interpolate to the target moneyness at the shorter maturity, repeat at the longer
maturity, and linearly interpolate between the two for the remaining time [S4]. The
Academy's demonstration scenario set uses volatilities of 20% and 25% and index term
performance from −30% to +30% in 5% steps [R6] — a usable regression grid.

---

## Cash flow components and recursions

### Notation (defined once)

| Symbol | Meaning |
|---|---|
| `t` | month index (month ends), `t = 0` at issue; `cy(t) = floor(t/12)` = complete contract years |
| `k` | index-linked option (bucket) index |
| `I(t)`, `I_s` | index level at t; index level at the current Term Start Date |
| `R_k(t)` | index performance to date = `I(t)/I_s − 1`; `R_k` at term end is the crediting input |
| `b`, `c`, `s`, `e`, `PR`, `f` | buffer, cap, step, edge, participation rate, floor (all positive fractions) |
| `T` | term length in years; `tau(t)` = days remaining / 365 [S2] |
| `IA_k(t)` | Investment Amount (Index Strategy Base) |
| `Pi(I, tau)` | per-unit-of-notional market value of the replicating option portfolio |
| `beta` | initial option budget = `Pi(I_s, T)` |
| `B_k(t)` | amortized initial budget in currency |
| `F_k(t)`, `D_k(t)`, `TC_k(t)` | fixed income asset proxy, derivative asset proxy, trading cost |
| `V_k(t)` | Interim Value |
| `r_0`, `r(t)` | Market Value Rate at term start / at t (annual effective) |
| `r_cc`, `q_cc`, `sigma` | continuously-compounded risk-free and dividend rates, implied volatility |
| `C(I,K,tau)`, `P(I,K,tau)`, `BC(I,K,tau)` | Black-Scholes European call, put, and cash-or-nothing binary call paying 1 |
| `AV(t)` | Account Value = `sum_k V_k(t) + FA(t) + HA(t)` |
| `G` | gross withdrawal removed from the contract; `FW` free withdrawal amount; `wc(cy)` charge rate |
| `ROP(t)` | return-of-premium GMDB base |
| `q_m(t)`, `w_m(t)` | monthly mortality and surrender rates; `l(t)` in-force probability |

Black-Scholes, continuous parameters:

    d1 = [ ln(I/K) + (r_cc − q_cc + sigma^2/2) tau ] / (sigma sqrt(tau)),   d2 = d1 − sigma sqrt(tau)
    C  = I e^(−q_cc tau) N(d1) − K e^(−r_cc tau) N(d2)
    P  = K e^(−r_cc tau) N(−d2) − I e^(−q_cc tau) N(−d1)
    BC = e^(−r_cc tau) N(d2)

Dimensional check: `Pi` is dimensionless (a fraction of notional), `beta` dimensionless,
`IA`, `B`, `F`, `D`, `TC`, `V`, `AV`, `G` are currency, `tau` and `T` are years, all rates
are per annum.

### Term-end crediting

Let `R` be the index performance over the completed term. Piecewise crediting rate `g`:

    BUFFER + CAP      g = min(R, c)                if R >= 0
                      g = min(0, R + b)            if R <  0                    [S1] [S2]

    BUFFER + CAP + PR g = min(PR * R, c)           if R >= 0
                      g = min(0, R + b)            if R <  0                    [S4]

    BUFFER + STEP     g = s                        if R >= 0
                      g = min(0, R + b)            if R <  0                    [S1] [S2]

    BUFFER + EDGE     g = e                        if R >= -b
                      g = R + b                    if R <  -b                   [S2]

    FLOOR + CAP       g = min( max(R, -f), c )                                  [S5]

The `min(0, ·)` in the buffer branch is load-bearing: "The Performance Rate can never be
greater than zero if the Index Performance is negative" [S1]. Note the deliberate
discontinuities the source documents flag — a Step design pays the full step at
`R = 0.00%` and zero at `R = −0.01%` [S4], and a dual/absolute-return design flips sign at
the buffer edge [S4]. They are contractual, not artifacts; do not smooth them.

Roll-forward [S1] [S2]:

    IA_k(term end) = IA_k(term start, adjusted for withdrawals) * (1 + g)

### Replicating portfolios (per unit of notional; each option has notional equal to `IA` [S4])

    CAP:        Pi = [ C(I, I_s, tau) − C(I, I_s(1+c), tau) − P(I, I_s(1−b), tau) ] / I_s     [S2] [S3] [S5] [S6]
    CAP + PR:   Pi = PR * [ C(I, I_s, tau) − C(I, I_s(1+c/PR), tau) ] / I_s
                     − P(I, I_s(1−b), tau) / I_s                                              [S4]
    STEP:       Pi = s * BC(I, I_s, tau) − P(I, I_s(1−b), tau) / I_s                          [S2] [S5]
    EDGE:       Pi = e * BC(I, I_s(1−b), tau) − P(I, I_s(1−b), tau) / I_s                     [S2] [S5]
    FLOOR:      Pi = [ C(I, I_s, tau) − C(I, I_s(1+c), tau)
                       − P(I, I_s, tau) + P(I, I_s(1−f), tau) ] / I_s                         [S5]
    TIERED PR:  Pi = [ C(I, I_s, tau) + (PR2 − PR1) * C(I, I_s(1+L), tau)
                       − P(I, I_s(1−b), tau) ] / I_s                                          [S3]

`L` is the tier level. The **floor design needs four options, not three** — buy the ATM
call spread, sell an ATM put, and buy back an OTM put struck at the floor so the short put
exposure stops there; Allianz states that "the out-of-the-money put will almost always
reduce, and never exceed, the negative impact of the at-the-money put for the Index Guard
Strategy" [S5]. For the Edge/dual-precision design the binary call is *in the money*
because it pays when the index ratio is at or above `1 − b` [S2] [S5]. If a Cap option is
uncapped, the out-of-the-money call is valued at zero [S2].

**Verification identity (implement as a unit test).** At `tau = 0`, every `Pi` above
collapses to the corresponding `g`. For CAP with `I/I_s = 1 + R`:
`max(R,0) − max(R − c, 0) − max(−b − R, 0) = g`. If a model's interim value at term end
does not reproduce `IA * (1 + g)` exactly, the strike set or the notional convention is
wrong.

### Interim value — the [std] baseline (family (a), the AG 54-literal form [S2] [R2])

    B_k(t)  = beta * IA_k(t) * tau(t) / T                                (straight-line amortization [S2])
    F_k(t)  = [ IA_k(t) − B_k(t) ] * [ (1 + r_0) / (1 + r(t)) ] ^ tau(t)
    D_k(t)  = IA_k(t) * Pi( I(t), tau(t) )
    TC_k(t) = kappa * IA_k(t) * sum of | per-unit option component values |   for tau(t) > 0
            = 0                                                              at tau(t) = 0
    V_k(t)  = F_k(t) + D_k(t) − TC_k(t)

`B` is the market value of the Derivative Asset Proxy **under initial market conditions**,
amortized straight-line to term end [S2]; `r_0` and `r(t)` are the Market Value Rates
(CMT at the term's maturity, linearly interpolated between adjacent CMT maturities) on the
Term Start Date and the calculation date [S2]; `tau` is days remaining / 365 [S2].
Because `B_k(t)` is defined as `beta` times the *current* `IA_k(t)`, `V_k(t)` is
**homogeneous of degree one in `IA_k(t)`** **[std]** — a convention the model must impose
so that a withdrawal reduces the interim value by exactly the cash removed (below).

Boundary conditions (both are AG 54 requirements and both are exact under this form):

- `tau = T`: `B = beta * IA`, `F = IA(1 − beta)`, `D = beta * IA`, so `F + D = IA`. AG 54
  requires the Index Strategy Base to equal the Strategy Value at term start [R2].
- `tau = 0`: `B = 0`, `F = IA`, `D = IA * g`, and `TC = 0` — there are no options left to
  exit, and the Academy example likewise shows no trading cost at term end [R6] — so
  `V = F + D = IA(1 + g)`. Implement `TC_k` as strictly interior to the term
  (`kappa_effective = kappa * 1{tau > 0}` **[std]**); leaving the trading-cost provision on
  at `tau = 0` breaks the term-end verification identity stated above by `kappa * IA * |g|`.

The Academy's worked example confirms both numerically and notes that the interim value is
**undefined at term start and term end** — those points are Strategy Values, not Interim
Values [R6].

### Interim value — the two alternative families (implement as switchable strategies)

**(b) Full notional discounted at a current rate, plus an always-positive expense
rebate** [S4] [S6]:

    V_k(t) = IA_k(t) / (1 + rate(t)) ^ tau(t)  +  D_k(t)  +  CCF_k(t)
    CCF_k(t) = E_0 * tau(t) / T          (Cap Calculation Factor; always positive, declines)

Equitable discounts the **full** Segment Investment with no subtraction of an initial option
budget and adds the Cap Calculation Factor, "a return of estimated expenses for the portion
of the Segment Duration that has not elapsed" (worked: $10 of estimated expenses on a
one-year segment gives $6 with 219 days remaining, since 10 x 219/365 = 6); the rate is an
investment-grade rate (risk-free plus a spread) that Equitable notes is above swap rates and
therefore "will result in a lower value for that component" [S4]. Lincoln's
`C x [1/(1+E)^D x (1+E)^D/(1+F)^D]` is presented as accretion-times-MVA but collapses
algebraically to `C / (1+F)^D` [S6].

**(c) A delta applied to the notional rather than a value, with no interest-rate
adjustment term** [S5]:

    DailyAdjustment(t) = [ ( Pi(I(t), tau(t)) − Pi(I_s, T) ) + Pi(I_s, T) * (1 − tau(t)/T) ] * IA_k(t)
    V_k(t)             = IA_k(t) + DailyAdjustment(t)

Allianz describes the second bracketed term ("proxy interest") as "approximated by the
value of amortizing the cost of the Proxy Investment over the Term to zero" [S5] — the
same option-budget amortization that appears as term `B` in families (a) and (b), added
rather than subtracted. **There is no interest-rate adjustment factor in this form at all**
[S5].

**Non-obvious equivalence worth knowing.** Expanding (c) and using `beta = Pi(I_s, T)`
gives `V = IA[1 + Pi(I(t), tau) − beta * tau/T]`, which is exactly family (a) with the
MVA factor set to 1. **Families (a) and (c) differ only in whether the fixed leg is
marked for interest-rate movement.** That is the direct consequence of AG 54's project
history: specific MVA requirements were deliberately removed from the guideline because
consensus was unreachable on whether MVAs should be permitted at all, leaving the "equity"
principle to state review [R2].

**Option-budget amortization switch [std].** `B_k(t)` may be computed either as
`beta * IA * tau/T` (straight-line, the [std] baseline [S2], and the mandated form in
Pennsylvania for [S3]) or as `Pi_initial-conditions(I_s, tau(t)) * IA` (initial market
conditions with **updated time to expiry**, the national form for [S3]). One insurer needs
both, so this is a configuration flag, not a modeling opinion.

**Legacy contrast module (pre-AG 54) [S1].** The older design uses no option pricing:
accrue each rate linearly and apply the term-end rules to the accrued rates —
`AccruedCapRate = c x (days elapsed)/(days in term)`, likewise for the Shield and Step
Rates, 365 days assumed per calendar year of a term [S1]. Worked: $50,000, Shield 10, 10%
Cap, 1-year term, index 500 → 600 at day 183 gives an accrued cap of 5%, a 5% Performance
Rate and an interim value of $52,500 [S1]. Useful as a tractable first implementation
target and as a regression contrast; it predates AG 54's July 1, 2024 effective date [R2]
and would not satisfy the Hypothetical Portfolio requirement without a
material-consistency demonstration.

### The universal proportional rule for withdrawals

Every insurer in the sample reduces the index-linked notional **in proportion to the
reduction in interim value**, not dollar-for-dollar [S2] [S3] [S4] [S6]. For a gross
withdrawal `G_k` taken from option k at time t:

    IA_k(t+) = IA_k(t−) * ( 1 − G_k / V_k(t−) )
    V_k(t+)  = V_k(t−) − G_k                      (follows from homogeneity of V in IA)

The reduction in notional is `Delta_IA = G_k * IA_k(t−) / V_k(t−)`, so

    Delta_IA − G_k = G_k * ( IA_k(t−) / V_k(t−) − 1 )   >  0   whenever  V_k(t−) < IA_k(t−)

i.e. **the notional lost can exceed the cash received**. Numeric illustration at the
worked-example parameters: `IA = $100,000`, `V = $84,803.11`, `G = $8,000` →
`Delta_IA = $9,433.62`, an excess of **$1,433.62** over the cash withdrawn, and the
remaining notional is $90,566.38. Brighthouse works the same rule at
`$50,000 x (1 − $20,000 / $53,514.77) = $31,313.57` [S2]; Prudential works it at a 71.429%
ratio and gives a second case in which a $14,000 withdrawal against a $14,000 interim
value zeroes a $14,285.71 base [S3]. The prospectus states the asymmetry directly: a
withdrawal when the interim value is below the investment amount "will cause a greater
percentage reduction in the Investment Amount that remains" [S2].

Exception: after a **Performance Lock**, the locked value is reduced **dollar-for-dollar**
[S2] — the option leg is gone and the bucket is a fixed accrual to term end.

### Withdrawal charge, free amount, and allocation

    FW(t)        = 0                                            if cy(t) = 0
                 = 0.10 * AV_anniv(y) − FW_used(y)              otherwise            [S1] [S2]
    chargeable   = max( 0, G_total − FW(t) )
    WC(t)        = wc( cy(t) ) * chargeable                                          [S1] [S2]
    net proceeds = G_total − WC(t)

The charge is deducted from the amount withdrawn and is **not grossed up** on this chassis
[S1] [S2] (contrast [S4], where "any amount deducted to pay withdrawal charges is also
subject to that same withdrawal charge percentage"). Verification against the prospectus
example [S2]: $100,000 payment, $80,000 Account Value at the start of contract year 6,
full withdrawal → `FW = $8,000`, chargeable `$72,000`, `wc(5) = 3%`, charge `$2,160`, cash
value `$77,840`. `G_total` is allocated across open options **pro rata to interim value**
**[std]** (the prospectuses do not prescribe an allocation for an unspecified withdrawal).

### Contract-level values and benefits

    AV(t)   = sum_k V_k(t) + FA(t) + HA(t)
    CSV(t)  = AV(t) − wc(cy(t)) * max(0, AV(t) − FW(t))                 (full surrender)  [S1] [S2]
    ROP(t+) = ROP(t−) * ( 1 − G_total / AV(t−) )                        (proportional)    [S1] [S2]
    DB(t)   = max( AV(t), ROP(t) )        for issue ages <= 80;  = AV(t) for 81+          [S2]
    Annuitization value = AV(t), with each open option contributing V_k(t)                [S1]

Note the GMDB's interaction with the interim value: `AV(t)` is depressed exactly when the
option leg is deep out of the money, so the return-of-premium guarantee bites in equity
stress [S1] [S2]. The reduction ratio applied to `ROP` uses the **gross** amount removed
from the contract, i.e. including any withdrawal charge [S1].

Fixed and Holding Accounts accrue monthly at the declared rate, floored at the 1%
guaranteed minimum [S1] [S2]:
`FA(t) = FA(t−1) * (1 + max(i_declared, 0.01))^(1/12)`.

### Monthly processing order [std]

At each month end `t`:

1. **Market state.** Refresh `I(t)`, the CMT curve, `sigma`, `q` from the scenario.
2. **Term-end crediting.** For each option whose Term End Date is `t`: compute
   `R_k = I(t)/I_s − 1`, apply `g`, set `IA_k <- IA_k (1 + g)`. Set the interim value equal
   to `IA_k` for the Transfer Period [S2].
3. **Renewal / transfer.** Apply the term-end roll rule (below): renew into the same
   option at the new declared rate (floored at the guaranteed minimum cap [S2]), transfer
   to the Fixed Account, or route to the Holding Account if the option and the Fixed
   Account are both unavailable [S2]. Reset `I_s`, `r_0`, `T`, `tau`, recompute
   `beta = Pi(I_s, T)`.
4. **Interim values.** For every open option, compute `F_k`, `D_k`, `TC_k`, `V_k`.
5. **Accounts.** Accrue `FA`, `HA`. Set `AV(t)`. On a Contract Anniversary, snapshot
   `AV_anniv` and reset `FW_used`.
6. **Contract-holder transactions.** Scheduled and dynamic partial withdrawals: allocate,
   compute the withdrawal charge, reduce `IA_k` **proportionally**, reduce `ROP`
   proportionally, recompute `V_k` and `AV(t)`.
7. **Decrements (end of month).** Death at `q_m(t)`, then surrender at `w_m(t)` on
   survivors **[std order]**; plus the discrete term-end surrender fraction if `t` is a
   Term End Date. Update `l(t) = l(t−1) (1 − q_m(t)) (1 − w_m(t))`.
8. **Maturity.** At the Maturity Date, force annuitization of `AV(t)` [S2].

### Cash flow outputs (per contract, month t, before in-force weighting)

| Cash flow | Formula | Sign |
|---|---|---|
| Single premium | `single_premium` at t = 0 | + |
| Death claims | `DB(t)` | − |
| Full surrender | `CSV(t)` | − |
| Partial withdrawal | `G_total − WC(t)` | − |
| Withdrawal charge income | `WC(t)` (retained; not a separate cash flow if `CSV`/net proceeds are used) | + |
| Annuitization outgo | `AV(t)` converted to a payout stream at the Maturity Date | − |
| Acquisition expense | `0.06 x premium + 200` at t = 0 **[std]** | − |
| Maintenance expense | `60/12 x 1.025^(y−1)` **[std]** | − |
| Option budget / hedge cost | **not a liability cash flow** — it is an asset-side flow; the liability model sees it only through the declared cap (see note) | n/a |

Note on annuitization: this file specifies the **deferral phase only**. The payout stream
bought at the Maturity Date is not re-derived here — survivorship weighting, period-certain
floors and joint-life continuance are the payout chassis in
`products/immediate_annuity/technical-notes.md`, applied to the **two** forms this
contract offers (Life with 10 Years of Annuity Payments Guaranteed; Joint and Last Survivor
with 10 Years Guaranteed) [S2]. Two deltas against that chassis: this contract offers **no
refund forms** (neither cash refund nor installment refund) [S2], so that branch is unused;
and the survivor continuance percentage on the joint form is documented **only by name** in
the retrieved prospectuses, so 100% last-survivor continuance is assumed **[std]**
[unverified] and the reduced-percentage branch is likewise unused. Purchase rates
themselves were not located in any retrieved document (research gap 2), so the reference
model computes factors on the **[std]** basis in `product-spec.md`.

Note on the option budget: on this chassis the cap *is* the fee — "While no fees or
charges are deducted from the amounts held in the Index Strategies, the available Cap
Rates, Participation Rates, Tier Levels, and Step Rates reflect the expenses related to
the Index Strategies" [S3]; Equitable and Lincoln call the cap an "implicit ongoing fee"
[S4] [S6]. A gross-liability projection must therefore **not** deduct a charge from the
index-linked value; the margin appears as the spread between the earned rate and the
option budget implied by the declared cap.

Aggregate expected cash flows weight each row: expenses by `l(t−1)`; death claims by
`l(t−1) q_m(t)`; surrenders by `l(t−1) (1 − q_m(t)) w_m(t)` **[std timing]**.

---

## Policyholder behavior modeling

All dynamic formulas below are **[std]** reference constructions; calibration sources are
cited where they exist, and the public RILA-specific data are thin ([REG-R64] reports
aggregate counts only; the detailed tables sit behind a paid data package).

- **Base surrender [std].** Annual `w_base(y)` per the table above, converted monthly:
  `w_m = 1 − (1 − w_annual)^(1/12)`.
- **Charge-expiry shock [std].** Multiplier `M_sc(7) = 3.0`, unity elsewhere (table above) —
  contract year 7 being the first year with a
  zero withdrawal charge [S1] [S2], which on the 6-year chassis coincides with the first
  Term End Date. Order-of-magnitude anchors from adjacent products: ~33% shock without a
  living-benefit rider and ~10% with one for FIA, ~52%/~56% for fixed-rate deferred
  [REG-R62] [REG-R63] [unverified]. The representative RILA carries no living-benefit rider,
  which argues for the un-suppressed end; the offsetting force is the term structure
  (below), which is why the [std] shock is set well below the FIA "without rider" anchor.
- **Interim-value moneyness suppression [std] — the RILA-specific effect.** Surrendering
  mid-term crystallizes the interim value, which is punitive when the option leg is out of
  the money. Reference form:

      M_iv(t) = min( 1.0, max( 0.25, V_k(t) / IA_k(t) ) ) ^ 2

  so a bucket at `V/IA = 0.85` carries a 0.72 multiplier and one at or above par carries
  1.0. Rationale: the prospectuses warn repeatedly that the interim value "may be less
  than" the value at term end [S1] and can be negative even with the index up [S2]; a
  rational holder defers.
- **Term-end concentration [std].** During the Transfer Period the interim value equals
  the Investment Amount — no option adjustment [S2] — so the economic penalty for exiting
  vanishes for five days each term. Model this as a **discrete** surrender fraction at
  each Term End Date: `phi = 10%` when the withdrawal charge is zero, `phi = 3%`
  otherwise **[std]**, applied in addition to the background monthly rate.
- **Total surrender.** `w_annual(y,t) = min( 0.50, w_base(y) x M_sc(y) x M_iv(t) )`
  **[std cap]**, plus the discrete `phi` at term ends.
- **Term-end roll behavior [std].** The contractual default is automatic renewal into the
  same option at the new declared rate [S1]. Reference split at each Term End Date, after
  the `phi` surrender: 80% renew into the same option, 15% transfer to the Fixed Account,
  5% transfer to a different index-linked option (modeled as renewal at the same
  parameters). Renewals are re-struck at the prevailing index level and the new declared
  cap; if the declared cap would fall below the guaranteed minimum, it is floored there
  [S2], which mechanically raises the option budget and compresses the spread — the
  reason the guaranteed-minimum table is a genuine tail exposure, not decoration.
- **Partial withdrawals [std].** Base rule: 0% in contract year 1 (the free amount is zero
  [S1] [S2]); thereafter 2% of Account Value per year, taken at contract anniversaries and
  capped at the Free Withdrawal Amount so no withdrawal charge is incurred in the base
  run. RMD-driven withdrawals for qualified cells begin at the applicable age; RMD timing
  is a *behavioral* input, not merely a tax one [REG-R58] [REG-R64].
- **Performance Lock [std, optional module].** Election rule: lock when
  `V_k(t) / IA_k(t) >= 1 + theta` with `theta = 0.15`, once per term [S2]. After a lock the
  option leg is removed, the bucket accrues to term end, and withdrawals reduce the locked
  value dollar-for-dollar [S2]. Switched off in the base run.

---

## Worked example

Anchor cell: male 60, single premium **$100,000**, 100% to one **6-year** option, S&P 500
price return, buffer **b = 10%**, Cap crediting with a declared cap **c = 100%** **[std]**.
Market inputs **[std]**: `r = 4.00%` annual effective, `q = 2.00%`, `sigma = 20.00%`, index
normalized to `I_s = 100`. Strikes: ATM call at 100, OTM call at `I_s(1+c) = 200`, OTM put
at `I_s(1−b) = 90`; each option's notional is the Investment Amount [S4]. Trading cost
`kappa = 0.10%` of the sum of absolute option values **[std]**.

Derived at term start: `Pi(100, 6) = 0.215679 − 0.033445 − 0.081602 = 0.100632`, so the
option budget is `beta = 10.0632%` = **$10,063.19** and the fixed leg opens at
`$89,936.81`. The equivalent geometric accretion yield on the fixed leg is **1.7834%**,
i.e. a **2.22%** spread against the 4.00% market rate — that spread is the [std] input to
the NGE cap-solve rule above. The Market Value Rate is 4.00% at term start and **5.00%**
at t = 3 (a 100 bp rise, to exercise the MVA factor).

| # | Point | t (yrs) | Index | R | Fixed proxy | ATM call | − OTM call | − OTM put | Deriv. proxy | Trading cost | Interim value | Investment Amount |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Term start (Strategy Value, not an IV [R6]) | 0 | 100 | 0.00% | 89,936.81 | 21,567.95 | −3,344.55 | −8,160.20 | 10,063.19 | 33.07 | — (base = 100,000.00) | 100,000.00 |
| A1 | Scenario A, mid-term | 3 | 120 | +20.00% | 92,280.78 | 29,145.94 | −2,182.94 | −2,726.33 | 24,236.66 | 34.06 | **116,483.39** | 100,000.00 |
| B1 | Scenario B, mid-term | 3 | 80 | −20.00% | 92,280.78 | 5,778.47 | −85.24 | −13,151.88 | −7,458.66 | 19.02 | **84,803.11** | 100,000.00 |
| B2 | Scenario B, immediately after an $8,000 withdrawal | 3 | 80 | −20.00% | 83,575.37 | 5,233.35 | −77.20 | −11,911.19 | −6,755.04 | 17.22 | **76,803.11** | **90,566.38** |
| A2 | Scenario A, term end — credit `min(40%, 100%) = +40%` | 6 | 140 | +40.00% | 100,000.00 | 40,000.00 | 0.00 | 0.00 | 40,000.00 | 0.00 | — (Strategy Value 140,000.00) | **140,000.00** |
| B3 | Scenario B, term end — credit `min(0, −25% + 10%) = −15%` | 6 | 75 | −25.00% | 90,566.38 | 0.00 | 0.00 | −13,584.96 | −13,584.96 | 0.00 | — (Strategy Value 76,981.42) | **76,981.42** |

Trace and checks:

- **Row 0.** `F = 100,000 (1 − 0.100632 x 6/6) x (1.04/1.04)^6 = 89,936.81`;
  `F + D = 100,000.00` exactly — AG 54's requirement that the Index Strategy Base equal the
  Strategy Value at term start [R2]. The interim value is undefined here [R6].
- **Rows A1/B1.** `tau = 3`, so `B = 0.100632 x 100,000 x 3/6 = 5,031.60` and the
  unadjusted fixed leg is `94,968.40`. The MVA factor `(1.04/1.05)^3 = 0.971690` reduces it
  to `92,280.78` — a **$2,687.62** cost of the 100 bp rate rise. Without the rate move the
  interim values would be `$119,171.01` (A) and `$87,490.73` (B).
- **Row B1 is the case the prospectuses warn about**: the index is down 20%, well beyond
  the buffer's mid-term protection, and the short out-of-the-money put alone is worth
  −$13,151.88. Even in Row A1 — index up 20% — the short put still subtracts $2,726.33
  [S2].
- **Row B2, the proportional rule.** `G = $8,000` (assumed within the Free Withdrawal
  Amount, so no withdrawal charge). Ratio `8,000 / 84,803.11 = 9.4336%`;
  `IA <- 100,000 x (1 − 0.094336) = 90,566.38`. The notional falls **$9,433.62** for
  **$8,000** of cash — an excess of **$1,433.62**, exactly `G (IA/V − 1)`. Every component
  of the interim value scales by the same 0.905664 factor, so the interim value falls by
  exactly the $8,000 withdrawn: `84,803.11 − 8,000 = 76,803.11`. The `ROP` GMDB base falls
  in the same proportion as the Account Value [S1] [S2].
- **Rows A2/B3.** At `tau = 0` the replicating portfolio reproduces the crediting formula
  exactly: `+40%` capped at 100% gives `Pi = 0.40`; `−25%` with a 10% buffer gives
  `Pi = −0.15 = min(0, R + b)`. Scenario B's term-end Investment Amount is
  `90,566.38 x 0.85 = 76,981.42` — the withdrawal's proportional bite persists to term end.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**. Reserve and capital layers consume
them and are cited, not reproduced:

- **Nonforfeiture.** AG 54 is the governing standard and is unusual in that the
  nonforfeiture value *is* the model's interim value: contracts issued on or after
  July 1, 2024 must produce Interim Values materially consistent with the Hypothetical
  Portfolio less Trading Costs, with an actuarial memorandum and certifications filed with
  each product [R2] [REG-R44]. Nonforfeiture benefits follow **Model #250 Section 7,
  excluding §7.B** [R2] [REG-R43]. **Model #805 does not apply if and only if AG 54 is
  satisfied** [REG-R42] [REG-R44]; if it did apply, note the indexed nonforfeiture rate is
  floored at **15 basis points**, not 1% [REG-R42].
- **Statutory reserve.** VM-21 constitutes CARVM for in-scope contracts; aggregate reserve
  = stochastic reserve (**CTE70**) + additional standard projection amount, with
  contract-holder behavior in §10 and prudent-estimate mortality in §11 [REG-R35]. **Scope
  test:** VM-21 §2.A.3 excludes separate-account contracts that guarantee an index and
  offer no GMDB/VAGLB, so a bare accumulation RILA is out of scope, while the
  representative return-of-premium GMDB design is in [R3] [S2]. AG 43 remains the scoping
  shell that pulls pre-2017 business onto the VM-21 calculation [REG-R35] [REG-R38];
  implementation guidance in the Academy's VM-21 practice note supplement [REG-R66]. **An
  out-of-scope contract falls back to formulaic CARVM, and that fallback is no longer
  unsourced** — AG 33 has been read and reaches any annuity contract subject to CARVM with
  elective benefits available [REG-R151], while AG 35 has been read and does not address
  this design [REG-R152].
- **Capital.** C-3 Phase II: TAR at **CTE 90**, RBC = TAR − statutory reserves, subject to
  the Standard Scenario floor [REG-R47]; VM-21 §§4.A–4.E and the RBC requirements are
  identical apart from the elective tax treatment, so one projection serves both
  [REG-R35]. Reform background in [REG-R48].
- **Tax.** IRC §807: greater of net surrender value and 92.81% of the NAIC-prescribed
  method (CARVM), capped at statutory [REG-R16]; distribution taxation under §72
  [REG-R55]; §817(h) diversification [REG-R15].
- **U.S. GAAP.** Index credits and annuity guarantees are the paradigm **market risk
  benefits** at fair value through earnings under LDTI [REG-R34], with ASOP No. 10 the
  professional-standards counterpart [REG-R71].
- **Standards for the modeling work itself.** ASOP No. 7 (life cash flow analysis)
  [REG-R27]; ASOP No. 22 (asset adequacy) [REG-R29]; ASOP No. 54 (pricing) [REG-R70];
  ASOP No. 56 (modeling, validation, model risk) [REG-R32]; ASOP No. 2 for the NGE
  determination process [R5] [REG-R26]. There is **no ASOP for principle-based reserves for
  annuities** — ASOP 52 is scoped to VM-20 life products [REG-R31], and the nearest
  guidance is the non-binding Academy practice note [REG-R66].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order:

1. **Implied volatility.** The interim value is a derivative price; `sigma` moves it
   directly, and **the sign differs by strategy**: increases in expected volatility hurt
   dual-precision, precision and 1-year performance strategies, while *decreases* hurt the
   floor (Index Guard) strategy [S5]. A flat-surface approximation is the largest single
   simplification in this model.
2. **Interest rates through the MVA factor.** At the worked-example parameters a 100 bp
   rise costs $2,687.62 of interim value at the term midpoint — larger than the entire
   trading-cost provision by two orders of magnitude. Family (c) has no such term at all
   [S5], so the choice of interim-value family is itself a rate-sensitivity assumption.
3. **The NGE renewal rule for caps.** It sets every future option budget and hence future
   interim values, surrender behavior and margin. Floored at the guaranteed minimum
   [S1] [S2], which converts a low-rate environment into a direct margin compression.
4. **Surrender timing relative to term boundaries.** Because the interim value equals the
   Investment Amount during the Transfer Period [S2], surrenders concentrate there; a
   model that spreads surrenders uniformly across the term systematically over-collects
   the negative interim value adjustment.
5. **Proportional withdrawal accounting.** Modeling withdrawals as dollar-for-dollar
   reductions of the notional overstates remaining notional in down markets by
   `G (IA/V − 1)` per withdrawal and compounds through the rest of the term.
6. **GMDB moneyness correlation.** The return-of-premium guarantee is most in the money
   exactly when interim values are depressed [S1] [S2] — the guarantee and the account are
   not independent, so a deterministic run understates its cost.

Known modeling pitfalls:

- **Price return vs total return.** All representative indices are price return [S1] [S2];
  omitting the dividend yield overprices every call and inflates interim values throughout.
- **Applying the cap annually on a multi-year term.** "We do not apply the Cap and any
  Participation Rate annually on a 3-year or 6-year Term Index Option" [S5] — the cap
  applies to the whole-term return.
- **Losing homogeneity.** If `B_k(t)` is frozen at the term-start notional rather than
  scaled with the current `IA_k(t)`, a withdrawal no longer reduces the interim value by
  exactly the cash withdrawn and the contract silently gains or loses value on every one.
- **Term-end mismatch.** If `V_k` at `tau = 0` does not equal `IA_k (1 + g)` to the cent,
  the strike set, the notional convention, the buffer sign — or a trading-cost provision
  left switched on at `tau = 0` — is wrong; unit-test it for every crediting type.
- **Discount-rate reference mismatch.** CMT [S2], CMT plus corporate spread [S6], a credit
  index at a duration that need not match the term [S3], or an investment-grade rate above
  swap rates [S4]. Reconciling to one insurer requires that insurer's reference.
- **Amortization convention.** Straight-line [S2] vs updated time to expiry [S3] — one
  insurer uses both, split by state [S3].
- **Negative interim value with the index up.** "You could have negative Interim Value,
  even if the Index Value has increased at the time of the calculation" [S2]; flooring the
  interim value at zero, or at the notional, is not implementing the contract.
- **Smoothing the crediting discontinuities.** Step and Edge designs are genuinely
  discontinuous at `R = 0` and `R = −b` [S2] [S4]; the binary options are what make the
  interim value track that, and smooth approximations break the term-end identity.
- **Era mixing.** The pre-AG 54 pro-rata design [S1] and the hypothetical-portfolio design
  [S2] are both live in in-force blocks (AG 54 applies to issues on or after July 1, 2024
  [R2]); an in-force model must carry both engines and key them off issue date.
- **Trading costs are a free parameter.** No retrieved prospectus quantifies them
  [S2] [S4] [S6]; the [std] 0.10% matches only the order of magnitude implied by [R6].
- **Regression vectors exist — use them.** Lincoln publishes interim-value grids across
  index moves of −30%/−10%/+20%/+40% for 1- and 6-year terms and for cap, trigger and
  dual-trigger accounts [S6]; Prudential a three-strategy grid at ±20% [S3]; Brighthouse a
  single fully decomposed case [S2]; and the Academy a six-year path with all
  Black-Scholes inputs disclosed plus an Excel Lambda library reproducing the calculation
  [R6]. These are the only public conformance tests available.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-registered_index_linked_annuity-r2
[R3]: #uslib-registered_index_linked_annuity-r3
[R5]: #uslib-registered_index_linked_annuity-r5
[R6]: #uslib-registered_index_linked_annuity-r6
[REG-R15]: #uslib-reg-r15
[REG-R151]: #uslib-reg-r151
[REG-R152]: #uslib-reg-r152
[REG-R16]: #uslib-reg-r16
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[REG-R34]: #uslib-reg-r34
[REG-R35]: #uslib-reg-r35
[REG-R38]: #uslib-reg-r38
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R44]: #uslib-reg-r44
[REG-R47]: #uslib-reg-r47
[REG-R48]: #uslib-reg-r48
[REG-R55]: #uslib-reg-r55
[REG-R58]: #uslib-reg-r58
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R61]: #uslib-reg-r61
[REG-R62]: #uslib-reg-r62
[REG-R63]: #uslib-reg-r63
[REG-R64]: #uslib-reg-r64
[REG-R65]: #uslib-reg-r65
[REG-R66]: #uslib-reg-r66
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[S1]: #uslib-registered_index_linked_annuity-s1
[S2]: #uslib-registered_index_linked_annuity-s2
[S3]: #uslib-registered_index_linked_annuity-s3
[S4]: #uslib-registered_index_linked_annuity-s4
[S5]: #uslib-registered_index_linked_annuity-s5
[S6]: #uslib-registered_index_linked_annuity-s6
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
