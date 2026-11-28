# BasicLMM and CashValue_ME_LMM: design note

*This note records the design of `BasicLMM`, an economic scenario generator from the LIBOR
market model, and of `CashValue_ME_LMM`, the TVOG example that uses it: the mathematics,
the Excel input, the structure of the models, the interface to liability models, the tests
and the decisions behind them. It was made from the plan written while the models were
drafted, in November 2026, in the lifelib-dev/lifelib-economic repository, and leaves out
what concerned only the drafting. It follows the design note of the G2++ models,
[`g2pp_design.md`](g2pp_design.md), section by section. The model folders are the source of
truth: where they and this note differ, the models are right. Paths are relative to the
library folder, `lifelib/libraries/economic/`.*

## 1. Goal and scope

`BasicLMM` is a modelx model that generates **risk-neutral, monthly, stochastic
interest-rate scenarios** from the **LIBOR market model**: the lognormal forward-LIBOR model
of Brigo & Mercurio (2nd ed. 2006, chapter 6), with the shift of their §10.1. The model is
fitted exactly to an initial yield curve, and **all inputs are read from an Excel file**.
Its outputs drive lifelib liability models through the interface `BasicG2PP` already has,
so that

```
TVOG = mean over stochastic scenarios of PV(liability cash flows)
       - PV(liability cash flows) in the certainty-equivalent (CE) scenario
```

**In scope**

- Shifted-lognormal forward rates under the spot-LIBOR measure, with any number of factors,
  started from the forward rates of the initial curve
- Monthly grid t_i = i/12, i = 0..n (i is the same index as `t` in lifelib liability
  models). The tenor of the forward rates is 1, 2, 3, 4, 6 or 12 months, set in Excel
- Excel input: the shift, the tenor, run settings, initial curve(s) with maturities up to
  150 years, the volatility of the forward rates as a table of factor loadings by time to
  expiry, and bond-fund shares by years to maturity
- Outputs per scenario and month, under the names `BasicG2PP` uses: deflator, bank-account
  return, zero-coupon bond prices and yields at any whole-month tenor, the market-value
  return of the bond fund, plus the CE scenario. The LIBOR rate takes the short rate's place
- Validation: martingale tests, and Monte Carlo against Black's formula for caplets
- Worked TVOG example: the liability model of `CashValue_ME_G2PP` driven by this generator

**Out of scope**: calibration. The volatility table and the shift are calibrated elsewhere
and entered in Excel, like G2++'s parameters. Neither the initial curve nor the volatility
table is extrapolated.

**Out of scope for v1**: a volatility smile beyond the shift (stochastic volatility, SABR);
separate curves for discounting and for forward rates (the forward rates are those of the
one input curve, and "LIBOR" names the model, not a benchmark); real-world (P-measure)
scenarios; equity, credit and inflation models; multi-currency runs.

## 2. What lifelib already has, and how the design uses it

| Existing piece | What it gives | Use in this design |
|---|---|---|
| `economic/BasicG2PP` | The precedent: Excel read at run time, parameters as cells, the CE scenario as row 0, the bond fund, `*_paths()` outputs, a `Validation` space with `mcstats.py`, a numpy reference implementation and tests against it | Template for everything that does not depend on the rate model. The cells that read the curve and the fund, the CE cells and the output cells are copied as they are, and a test keeps the copies equal (§8) |
| `economic/g2pp_input.xlsx` | 12 example curves to 150 years and 3 example funds | Source of the `Curve` and `Fund` sheets of `lmm_input.xlsx` |
| `economic/CashValue_ME_G2PP` | lifelib's `savings/CashValue_ME_EX4`, reading its scenarios from a space `ESG` | Base of `CashValue_ME_LMM`: the same `Projection` space, with a copy of `LMM` as `ESG` |
| `economic/BasicHullWhite` | B&M notation and docstring style | As for `BasicG2PP` |

What changes with the model, and shapes the design:

| | `BasicG2PP` | `BasicLMM` |
|---|---|---|
| Rates | Gaussian short rate, two factors | shifted-lognormal forward rates, any number of factors |
| State per scenario and month | 3 numbers | every forward rate not yet set: up to 60 with the example input |
| Monthly step | exact | log-Euler; no bias to measure with the example input (§3) |
| Bond prices | closed form, any maturity | products of forward rates at tenor dates; interpolated in between |
| Lower bound of rates | none | minus the shift |
| Rates over long horizons | mean-reverting | can explode, unless volatility decays with time to expiry (§3, §10) |
| Closed forms for tests | bond options, a call on the deflator, the GMAB for a cash or single-maturity fund | caplets; the GMAB only for a policy maturing at the second tenor date |
| 1,000 scenarios × 600 months | 0.5 s, 60 MB | 1 s, 320 MB with annual forward rates; 10 s, 2.3 GB with monthly ones |

## 3. Key design decisions

1. **Forward rates of one tenor, moved every month.** The model's variables are the forward
   rates F_k for the periods between the tenor dates T_k = k × `tenor_mth` months.
   `tenor_mth` is 1, 2, 3, 4, 6 or 12, so every tenor date is a month of the grid and every
   anniversary is a tenor date. All rates not yet set move in every monthly step. The
   example uses 12: annual forward rates match the annual swaptions that such generators
   are usually calibrated to, and they keep a 50-year run near `BasicG2PP`'s cost (§6).
   With 1, the model is a monthly LMM with nothing to interpolate, at about 7 times the
   memory and 10 times the run time.
2. **Shifted-lognormal rates.** F_k + α is lognormal under its forward measure (B&M §10.1),
   with α = `shift` ≥ 0. Rates stay above −α, caplets keep Black's formula with the rate and
   the strike shifted, and α = 0 is the lognormal LMM. Without a shift the model cannot
   start from a curve with a negative forward rate, and a rate near zero hardly moves: on
   `JPY_DOWN`, whose first forward rate is 0.02%, the 1-year rate at 10 years has a standard
   deviation of 0.5% with α = 0 and 1.5% with α = 2% (Appendix A).
3. **Spot-LIBOR measure.** Scenarios are simulated under the measure whose numeraire is the
   bank account rolled over from tenor date to tenor date (B&M §6.3.2). Its reciprocal is
   the deflator, so `disc_factor_paths()` means what it means in `BasicG2PP`, and every
   asset earns the bank-account return in expectation. Under the terminal measure the
   deflator would be P(0,T_K)/P(t,T_K): noisier, and not what liability models expect.
4. **Log-Euler monthly step.** ln(F_k + α) takes an Euler step with the drift of the start
   of the month. Unlike G2++'s step it is not exact, but the prototype finds no bias to
   measure with the example volatilities. Against a scheme that makes deflated bond prices
   exact martingales, on the same random numbers, mean deflators differ by 0.8e-5 ± 1.5e-5
   at 10 years and by 1.9e-5 ± 7.3e-5 at 50, where 1,000 scenarios have a standard error of
   0.05% and 0.7%. Caplet prices are within 0.02% of a predictor-corrector scheme's at the
   money, and those agree with Black's formula. Appendix A also explains what was rejected:
   the predictor-corrector scheme (1.7 times the run time for no measurable gain), and the
   two martingale discretisations of Glasserman & Zhao (2000), of which one distorts
   short-dated caplets and the other gives negative bond prices in extreme paths.
5. **Volatility as factor loadings by time to expiry.** The `Vol` sheet gives the volatility
   vector of a forward rate as a function of its time to expiry, one column per factor, so
   the number of factors is the number of columns. The length of a row is the rate's
   volatility, and the angle between two rows gives the correlation of two rates. Each
   rate's vector is constant within a month, read at the middle of the month, so the
   model's caplet volatilities are exact sums (§4). Parametric forms (B&M §6.3.1) and rank
   reduction (B&M §6.9.2) are ways to produce the table outside the model, like calibration.
   The factors therefore do not depend on the horizon: extending `step_size` leaves earlier
   months unchanged, up to rounding. The table must reach the longest time to expiry of a
   run, with no extrapolation, as for the curve.
6. **Example volatilities decay with time to expiry.** A volatility that stays at 10% for
   long expiries, as textbook examples have it, sends the 99th percentile of the 1-year
   rate at 50 years to 350% (Appendix A): high rates raise their own drift. The example
   table falls from 21% at expiry to 9% at 10 years and 2% at 30 years, which is the shape
   of the G2++ example's volatilities, and gives a 99th percentile of 16%.
7. **Bonds of every monthly maturity, by an interpolation that keeps the model
   arbitrage-free.** The LMM itself prices only bonds that mature on tenor dates. In
   between, the deflated price of a bond is linear in maturity between its two neighbouring
   tenor bonds, which follows from giving no volatility to bonds that mature within the
   current tenor period (Schlögl 2002). A linear combination of martingales is a
   martingale, so every bond, the bank account and the bond fund are priced consistently.
   One deterministic factor per maturity, within 1.5e-4 of 1, makes the model reproduce the
   input curve at every month and not only at tenor dates, so the CE scenario equals
   `BasicG2PP`'s on the same curve. With `tenor_mth` = 1 nothing is interpolated.
8. **One array per month: the forward rates not yet set.** `fwd_rates(i)` has a row per
   scenario and a column per rate, and every other quantity is a product or an
   interpolation of its columns. modelx caches the array of every month, so memory and run
   time grow with scenarios × months × rates (§6).
9. **`maturity_size`: the bond maturities carried at every month.** The rates to simulate
   must be fixed before the run, so they cover `step_size` + `maturity_size` months. Bond
   prices, yields and fund bonds are available for maturities up to `maturity_size` months
   at every projection month, and a longer one raises an error that names the parameter. A
   rate does not depend on rates that expire later, so raising `maturity_size` leaves the
   results unchanged, up to rounding.
10. **Everything that does not depend on the rate model is as in `BasicG2PP`**: Excel read
    at run time through `input_file`; parameters as zero-argument Cells; scenario 0 as the
    CE scenario; antithetic variates; random numbers laid out `(step_size, scen_size, d)`;
    one main space plus a `Validation` space; no curve extrapolation; the bond fund and its
    `Fund` sheet; the names and shapes of the outputs.
11. **Its own workbook.** `lmm_input.xlsx` has `Curve` and `Fund` sheets identical to those
    of `g2pp_input.xlsx`, so the two generators can be compared on the same curve and fund,
    and neither file holds the other model's parameters.
12. **No closed form for the GMAB, and a floorlet identity in its place.**
    `formula_gmab_g2pp` has no LMM counterpart, because deflators and bond prices are not
    lognormal: a lognormal approximation is within 5% at the money, but off by up to 22%
    in the money and by multiples out of the money (Appendix A). A single-premium policy
    that matures at the second tenor date with an all-cash fund is exactly a floorlet (§4).
    That gives the TVOG example its closed-form check, and caplets against Black's formula
    give the generator its own.

## 4. Mathematical specification (B&M 2006, chapter 6 notation)

**Grids**, with p = `tenor_mth`, n = `step_size` and m̄ = `maturity_size`:

```
t_i  = iΔ,  Δ = 1/12,  i = 0..n                 months
T_k  = kτ = t_{kp},  τ = p/12,  k = 0..K        tenor dates
K    = ⌈(n + m̄)/p⌉                              number of forward rates
c(i) = ⌊i/p⌋                                    T_{c(i)} ≤ t_i < T_{c(i)+1}
```

**Forward rates.** F_k(t), k = 1..K, is the simply compounded forward rate for the period
(T_{k-1}, T_k]:

```
1 + τ F_k(t) = P(t, T_{k-1}) / P(t, T_k),        F_k(0) from the initial curve P^M(0, ·)
```

F_k is set at T_{k-1} and keeps the value F_k(T_{k-1}) afterwards. At t_i the rates
k ≤ c(i)+1 are set, and the rates k ≥ c(i)+2 are alive in the step to t_{i+1}.

**Dynamics under the spot-LIBOR measure Q^d** (B&M §6.3.2, with the shift α of §10.1):

```
d(F_k + α) = (F_k + α) [ λ_k(t) · Σ_{j=β(t)}^{k} g_j(t) λ_j(t) dt + λ_k(t) · dW(t) ]
g_j(t)     = τ (F_j(t) + α) / (1 + τ F_j(t))
```

W is a d-dimensional Brownian motion, λ_k(t) the volatility vector of F_k, and β(t) the
index of the first rate not yet set. The numeraire is B_d(t), the bank account that
reinvests at each tenor date T_{k-1} at the rate F_k(T_{k-1}). With α = 0 and
λ_j · λ_k = ρ_{jk} σ_j σ_k this is B&M's formula.

**Volatility.** During the month [t_i, t_{i+1}) the rate F_k has m = (k-1)p - i months to
expiry at the start of the month, and its volatility vector is

```
λ_k = λ(m) = (f_1(u), ..., f_d(u))   at  u = (m - ½)Δ years
```

where f_1, ..., f_d are the columns of the `Vol` sheet, linear in u between its rows and
flat before the first row.

**Monthly step** (log-Euler), for the rates k ≥ c(i)+2, with Z_i ~ N(0, I_d):

```
μ_k = λ_k · Σ_{j=c(i)+2}^{k} g_j(t_i) λ_j
ln(F_k(t_{i+1}) + α) = ln(F_k(t_i) + α) + (μ_k - ½|λ_k|²)Δ + √Δ λ_k · Z_i
```

The sum is a cumulative sum over k, so a step costs N × K × d operations. Rates stay above
−α by construction.

**Deflated prices of the tenor bonds.** A price divided by the bank account is its deflated
price. For the bond maturing at T_k:

```
D(t_i; T_k) = P(t_i, T_k) / B_d(t_i) = Π_{j=1}^{k} 1 / (1 + τ F_j(t_i)),     k = 0..K
```

Once T_k has passed, this is the deflator at T_k, 1/B_d(T_k), and no longer changes. In
continuous time each D(·; T_k) is a martingale under Q^d.

**Bonds of every monthly maturity.** For the bond maturing at month j = lp + r, with
0 ≤ r < p and w = r/p, the deflated price at t_i ≤ t_j is

```
D(t_i; t_j) = κ_j [ (1-w) D(t_i; T_l) + w D(t_i; T_{l+1}) ]
κ_j         = P^M(0, t_j) / [ (1-w) P^M(0, T_l) + w P^M(0, T_{l+1}) ]
```

This is Schlögl's (2002) interpolation by day-count fractions, in which a bond that matures
within the current tenor period has no volatility, times the factor κ_j that fits the
initial curve at t_j. κ_j is 1 on tenor dates. Being a fixed combination of martingales,
D(·; t_j) is a martingale.

**Scenario quantities**

```
D(t_i)      = D(t_i; t_i)                                      deflator = 1 / bank account
P(t_i, t_j) = D(t_i; t_j) / D(t_i)                             zero-coupon bond price
R_i         = D(t_i)/D(t_{i+1}) - 1 = 1/P(t_i, t_{i+1}) - 1    bank-account return over [t_i, t_{i+1})
L(t_i)      = (1/P(t_i, t_{i+p}) - 1) / τ                      LIBOR rate, F_{c(i)+1}(t_i) on a tenor date
```

The second form of R_i holds because the deflated price of a bond does not change in its
last month. So the bank account rolls over one-month bonds, and its return over a month is
known at the start of the month. With p > 1 it is known from the start of the tenor period.

**CE scenario**: every forward rate keeps its initial value, so D_CE(t_i; t_j) = P^M(0,t_j),
D_CE(t_i) = P^M(0,t_i), R_CE,i = P^M(0,t_i)/P^M(0,t_{i+1}) - 1 and
P_CE(t_i,t_j) = P^M(0,t_j)/P^M(0,t_i), as in `BasicG2PP`.

**Bond fund**: shares w_c in the bank account and w_m in zero-coupon bonds with m months to
maturity, rebalanced monthly, as in `BasicG2PP`:

```
R^F_i = w_c R_i + Σ_m w_m [ P(t_{i+1}, t_{i+m}) / P(t_i, t_{i+m}) - 1 ]

P(t_{i+1}, t_j) / P(t_i, t_j) = (1 + R_i) D(t_{i+1}; t_j) / D(t_i; t_j)
```

The deflated account value D(t_i) AV(t_i) is a martingale for any shares, and constant for
an all-cash fund. In the CE scenario the fund earns R_CE,i whatever the shares. The fund
needs bonds up to t_{n-1+m}, so its longest maturity must not exceed `maturity_size`.

**Closed forms used by the tests**

- Black's formula with total volatility v:
  ```
  Bl(F, X, v) = F Φ(d1) - X Φ(d1 - v),     d1 = [ln(F/X) + v²/2] / v
  ```
- Caplet on F_k (k ≥ 2) with strike X, paying τ(F_k(T_{k-1}) - X)⁺ at T_k:
  ```
  E[ D(T_k) τ (F_k(T_{k-1}) - X)⁺ ] = τ P^M(0,T_k) Bl(F_k(0) + α, X + α, v_k)
  v_k² = Δ Σ_{m=1}^{(k-1)p} |λ(m)|²
  ```
  The deflated payoff is (D(t; T_{k-1}) - (1 + τX) D(t; T_k))⁺ at t = T_{k-1}. The formula
  is exact for the model in continuous time, whose volatilities are constant within each
  month. The floorlet follows by put-call parity.
- GMAB of a single-premium policy with no fees or decrements, an all-cash fund and maturity
  at the second tenor date T_2 = t_{2p}. The account value is
  AV(T_2) = AV0 (1 + τF_1(0)) (1 + τF_2(T_1)), so the guarantee is a floorlet on F_2:
  ```
  PV = E[ D(T_2) (SA - AV(T_2))⁺ ]
     = (AV0 / P^M(0,T_1)) τ P^M(0,T_2) [ (X + α) Φ(v_2 - d1) - (F_2(0) + α) Φ(-d1) ]
  X  = (SA P^M(0,T_1)/AV0 - 1) / τ,     d1 = [ln((F_2(0) + α)/(X + α)) + v_2²/2] / v_2
  ```
  and PV = 0 when X + α ≤ 0. For any fund, the CE value of a GMAB maturing at T is
  (SA P^M(0,T) - AV0)⁺, and TVOG = PV - CE.
- Swaption, as a diagnostic and not as a test. For the payer swaption that expires at T_a
  on the swap to T_b, with a fixed leg that pays yearly, at the anniversaries T_l, l ∈ 𝒯,
  the swap rate is S = (P(T_a) - P(T_b))/A with A = Σ_{l∈𝒯} P(T_l). Rebonato's formula
  (B&M §6.15), with the shift and with a fixed leg that pays less often than the tenor, is
  ```
  v_S² ≈ Σ_{i < ap} Δ | Σ_{j=a+1}^{b} z_j λ((j-1)p - i) |²,     z_j = (∂S/∂F_j)(F_j(0) + α)/(S(0) + α)
  ∂S/∂F_j = τ/(1 + τF_j(0)) · [ P^M(0,T_b) + S(0) Σ_{l∈𝒯, l≥j} P^M(0,T_l) ] / A(0)
  price ≈ A(0) Bl(S(0) + α, X + α, v_S)
  ```
  In the prototype it is within 0.5% of the Monte Carlo volatility at the money, and up to
  3.5% off at 1.25 times the forward swap rate.

A GMAB with a longer term has no closed form (decision 12).

## 5. Excel input: `lmm_input.xlsx`, next to the model folder

**Sheet `Params`** (columns `parameter`, `value`, `description`)

| parameter | example | notes |
|---|---|---|
| `shift` | 0.02 | α, as a rate: forward rates stay above −`shift`. 0 gives the lognormal LMM. At least 0, and below 12/`tenor_mth` |
| `tenor_mth` | 12 | tenor of the forward rates in months: 1, 2, 3, 4, 6 or 12 |
| `maturity_size` | 120 | number of monthly bond maturities carried at every month: at least `tenor_mth`, and at least the longest maturity of the fund and of any yield used |
| `scen_size` | 1000 | number of stochastic scenarios N, even when antithetic |
| `step_size` | 600 | number of monthly steps n: at least the liability `max_proj_len()` |
| `seed` | 1234 | random seed |
| `antithetic` | TRUE | antithetic variates |
| `curve_id` | EUR_BASE | column of the `Curve` sheet to use |
| `compounding` | annual | compounding of the input spot rates: `annual` or `continuous` |
| `fund_id` | BOND_MIX | column of the `Fund` sheet to use |

**Sheet `Curve`**: as in `g2pp_input.xlsx`, with the same 12 curves to 150 years, and
interpolated the same way (ln P^M linear between knots, no extrapolation). The curve must
reach T_K, the first tenor date at or after `step_size` + `maturity_size` months: 60 years
for the example, and at most 140 years of projection with 10 years of maturities.

**Sheet `Vol`**: column `maturity` (time to expiry in years, at least 0 and increasing, any
grid) plus one column per factor (`f1`, `f2`, ...). A row holds the volatility vector of a
forward rate with that time to expiry. Values are linear between rows and flat before the
first row, and the last row must reach the longest time to expiry of the run,
((K-1)p - ½)/12 years: 59 years for the example. The example table has two factors on 25
maturities from 0 to 150 years, rounded to six decimals:

```
f1(u) = 0.30 e^{-0.8u} - 0.7 × 0.20 e^{-0.08u},     f2(u) = √(1 - 0.7²) × 0.20 e^{-0.08u}
```

| time to expiry (years) | 0 | 1 | 5 | 10 | 20 | 30 | 50 |
|---|---|---|---|---|---|---|---|
| `f1` | 0.160 | 0.006 | -0.088 | -0.063 | -0.028 | -0.013 | -0.003 |
| `f2` | 0.143 | 0.132 | 0.096 | 0.064 | 0.029 | 0.013 | 0.003 |
| volatility | 21% | 13% | 13% | 9% | 4% | 2% | 0.4% |

These are two exponential factors with correlation −0.7, written as two independent ones:
the shape of the G2++ example (a = 0.773, b = 0.082, ρ = −0.7). With the 2% shift and
EUR_BASE, the caplet volatilities are 16% at 1 year, 13% at 10 and 8% at 30, about 65, 60
and 43 basis points in absolute terms. Like the G2++ parameters they are illustrative only.
A table is calibrated for one tenor: with the same table, a shorter tenor gives a more
volatile bank account (§10).

**Sheet `Fund`**: as in `g2pp_input.xlsx`, with the same three funds (`CASH`, `BOND_MIX`,
`BOND_10Y`). `cash` is the bank account of §4.

**Sheet `Notes`**: what each sheet holds, the source of the curves, and the two warnings of
§10 on the volatility table.

**Validation on read**: `param_table()` raises `ValueError` listing every problem: a
missing value or one of the wrong type, `shift` negative or not below 12/`tenor_mth`,
`tenor_mth` not one of the six values, `maturity_size` below `tenor_mth`, and the checks of
`BasicG2PP` on the other settings. `curve_table()` and `fund_table()` check as in
`BasicG2PP`. `vol_table()` raises it for a missing `maturity` column, maturities that are
negative or not increasing, no factor column, or a value that is blank or not a number.
`curve_knots()` raises it for a curve that ends before T_K, `vol_loadings()` for a table
that ends before the longest time to expiry, and `mkt_fwd_rates()` for an initial forward
rate that is not above −`shift`, naming the rate and the shift it needs. Asking for a bond
that matures after T_K raises it too, naming `maturity_size`.

## 6. modelx model design

**Files** in the library folder:

```
lmm_input.xlsx                      Excel input, read at run time
BasicLMM/                           modelx model: spaces LMM and Validation, and mcstats.py
CashValue_ME_LMM/                   TVOG example: CashValue_ME_G2PP's Projection plus a copy of LMM
lmm-simulation.ipynb, lmm-tvog.ipynb
plot_ex6_lmm_rate_fan.py, plot_ex7_lmm_caplet_vols.py     gallery scripts
tests/lmm_registry.py, reference_lmm.py, test_*_lmm.py    pytest: reference implementation and tests
_research/lmm_design.md             this note
```

The docs page is `BasicLMM.md` in `doc/source/libraries/economic/`. Edit the model folders
and the workbook directly, the models also in Spyder-modelx. Scripts in the drafting
repository first created them, the models through the modelx API, and are not kept in
sync.

**Space `LMM`** (i and j are month indexes, k and l tenor indexes, `t_(i) = i/12` in years,
N = `scen_size()`, n = `step_size()`, p = `tenor_mth()`, K = `tenor_size()`,
d = `factor_size()`, c = c(i))

| Group | Cells | Returns | Return type |
|---|---|---|---|
| Input | `input_path()`, `param_table()`, `curve_table()`, `fund_table()` | as in `BasicG2PP`, with the `Params` of §5 | `pathlib.Path`, `pandas.Series`, two `pandas.DataFrame`s |
| | `vol_table()` | loadings from the `Vol` sheet | `pandas.DataFrame` indexed by `maturity` (years), one float column per factor |
| | `shift()` | α | `float` |
| | `tenor_mth()`, `maturity_size()`, `scen_size()`, `step_size()`, `seed()` | p, m̄, N, n and the random seed | `int` |
| | `antithetic()` | whether antithetic variates are used | `bool` |
| | `curve_id()`, `compounding()`, `fund_id()` | as in `BasicG2PP` | `str` |
| Curve | `curve_knots()` | as in `BasicG2PP`, but checks that the curve reaches T_K | `tuple` of two 1-D `numpy.ndarray`s |
| | `mkt_zcb(i)` | P^M(0, t_i) | `float` |
| | `tenor_size()` | K | `int` |
| | `mkt_fwd_rates()` | F_k(0) for k = 1..K; checks that each is above −α | `numpy.ndarray`, shape (K,) |
| | `curve_adj(j)` | κ_j | `float` |
| Volatility | `factor_size()` | d, the number of factor columns | `int` |
| | `vol_loadings()` | λ(m) in row m, for m = 0..(K-1)p (row 0, a rate at its expiry, is 0); checks that the table reaches | `numpy.ndarray`, shape ((K-1)p+1, d) |
| | `caplet_vol(k)` | Black volatility of F_k + α, √(v_k²/T_{k-1}) | `float` |
| Simulation | `std_norm_rand()` | standard normal draws, antithetic if set | `numpy.ndarray`, shape (n, N, d) |
| | `fwd_rates(i)` | F_k(t_i) for k = c+1..K. Column 0 is the rate of the current tenor period, already set | `numpy.ndarray`, shape (N, K-c) |
| | `tenor_disc_factor(l)` | D(T_l), the deflator at the tenor date T_l | `numpy.ndarray`, shape (N,) |
| | `defl_tenor_zcb(i, k)` | D(t_i; T_k) for k ≥ c | `numpy.ndarray`, shape (N,) |
| | `defl_zcb(i, j)` | D(t_i; t_j) for j ≥ i | `numpy.ndarray`, shape (N,) |
| | `disc_factor(i)`, `bank_return_mth(i)` | D(t_i) and R_i | `numpy.ndarray`, shape (N,) |
| | `P_t_T(i, j)` | P(t_i, t_j) by scenario | `numpy.ndarray`, shape (N,) |
| | `libor_rate(i)` | L(t_i) | `numpy.ndarray`, shape (N,) |
| | `spot_rate(i, m)`, `swap_rate(i, k)` | as in `BasicG2PP`: the m-month yield, and the k-year par rate with an annual fixed leg | `numpy.ndarray`, shape (N,) |
| Fund | `fund_cash_share()`, `fund_bond_shares()`, `zcb_return_mth(i, m)`, `fund_return_mth(i)` | as in `BasicG2PP`; the bond return uses the deflated prices of §4 | as in `BasicG2PP` |
| CE | `ce_disc_factor(i)`, `ce_bank_return_mth(i)`, `ce_libor_rate(i)`, `ce_spot_rate(i, m)` | CE counterparts, one deterministic value each | `float` |
| Outputs (row 0 = CE) | `scen_index()` | scenario IDs 0..N | `pandas.RangeIndex` |
| | `disc_factor_paths()` | D(t_i) for every scenario and month | `numpy.ndarray`, shape (N+1, n+1) |
| | `bank_return_paths()`, `fund_return_paths()` | R_i and R^F_i for every scenario and month | `numpy.ndarray`, shape (N+1, n) |
| | `libor_rate_paths()`, `spot_rate_paths(m)` | L(t_i) and m-month yields for every scenario and month | `numpy.ndarray`, shape (N+1, n+1) |
| | `scenario_table()` | `disc_factor`, `bank_return_mth`, `fund_return_mth` and `libor_rate` for every scenario and month | `pandas.DataFrame` with a (`scen_id`, `t`) MultiIndex |

`fwd_rates(i)` is the only wide array. The deflated bond prices are products over its
first columns, each cached as an array of length N:

```
tenor_disc_factor(l)  = tenor_disc_factor(l-1) / (1 + τ fwd_rates((l-1)p)[:, 0]),    tenor_disc_factor(0) = 1
defl_tenor_zcb(i, k)  = tenor_disc_factor(c) Π_{j=c+1}^{k} 1 / (1 + τ F_j(t_i))
```

References: `input_file = "lmm_input.xlsx"`, `dt = 1/12`, `np`, `pd`, and
`t_ = lambda i: i * dt`, as in `BasicG2PP`.

**Space `Validation`**, with the DataFrame columns `mc`, `theory`, `se` and `z` and the
pass rule of `BasicG2PP` (§8). References: `lmm` (an Interface to `LMM`), `np`, `pd`,
`stats` and `mcstats`.

- `martingale_test()`, `fund_martingale_test()`, `curve_fit_test()` and
  `zcb_martingale_test(i, j)`: as in `BasicG2PP`. In the first tenor period the deflators
  are known at time 0, so their z-scores are 0, in `curve_fit_test()` too
- `caplet_cf(k, x)` and `caplet_mc(k, x)`: the closed form of §4, and its Monte Carlo
  estimate against it, for the caplet on F_k with strike x
- `caplet_test()`: at-the-money caplets on the rates that expire at every whole year up to
  t_n. This takes the place of `moments_test()`, since rates have no closed-form moments
  under the spot-LIBOR measure
- `fwd_swap(a, b)`, `swaption_vol(a, b)` and `swaption_test(a, b)`: the forward swap rate
  and annuity, the approximation of §4, and the Monte Carlo price against it. A
  diagnostic, left out of `summary()`, because the formula is an approximation
- `summary()`: the largest |z| of each test against its limit

**Conventions**: as in `BasicG2PP` (docstrings with LaTeX math in B&M notation; path cells
assemble steps in increasing i).

**Memory and run time.** The cached `fwd_rates` arrays hold 8 N Σ_i (K - c(i)) bytes, and
the cached deflated bonds of every month add to them. Measured on `BasicLMM`'s main
outputs, for 1,000 scenarios with `maturity_size` 120 and two factors (the runs with more
forward rates were made with fewer scenarios and scaled):

| `step_size` | `tenor_mth` | K | run time | peak memory |
|---|---|---|---|---|
| 600 | 12 | 60 | 1.0 s | 320 MB |
| 600 | 6 | 120 | 2.1 s | 500 MB |
| 600 | 3 | 240 | 4.1 s | 880 MB |
| 600 | 1 | 720 | 10 s | 2.3 GB |
| 120 | 12 | 20 | 0.2 s | 45 MB |
| 120 | 1 | 240 | 1.1 s | 200 MB |
| 1,680 | 12 | 150 | 9 s | 1.7 GB |

Memory grows with the square of the horizon, where `BasicG2PP`'s grows in proportion to
it. So a monthly tenor suits horizons up to about 20 years, and a 140-year run needs fewer
scenarios or more memory.

## 7. Interface to liability models and the TVOG example

**Contract**: the same cells as `BasicG2PP`, so a liability model written against its
outputs runs on `BasicLMM`'s unchanged.

| Output | Shape | Meaning | Use in a liability model |
|---|---|---|---|
| `disc_factor_paths()` | (N+1, n+1) | deflator D(t) by scenario | replaces `disc_factors(t)` |
| `fund_return_paths()` | (N+1, n) | market-value return of the bond fund over [t, t+1) | becomes `inv_return_mth(t)` |
| `bank_return_paths()` | (N+1, n) | risk-free return over [t, t+1), known at t | diagnostics; equals `fund_return_paths()` for an all-cash fund |
| `spot_rate_paths(m)`, `libor_rate_paths()` | (N+1, n+1) | market yields and the LIBOR rate | dynamic lapse or crediting rates (optional) |

Row 0 is the CE scenario, the timing is `CashValue_ME`'s, and the time origin is the
valuation date of the input curve.

**`CashValue_ME_LMM`**

1. Read `CashValue_ME_G2PP` from the library folder, rename it, and delete its space `ESG`.
2. Copy the space `LMM` of `BasicLMM` into it as `ESG` with `UserSpace.copy`, restore the
   docstring of `t_`, and point `Projection.esg` at it. `ESG` reads `lmm_input.xlsx` next
   to the model folder.
3. In `Projection`, the cells `scen_index()`, `inv_return_table()`, `disc_factors(t)`,
   `check_pv_net_cf()` and `result_tvog()` stay as they are, because they use only the
   contract. `formula_gmab_g2pp` goes. The new `formula_gmab_floorlet(t)` gives the closed
   form of §4 for the single-premium points maturing at t, and raises `ValueError` unless
   t is the second tenor date and the fund is all cash. The docstrings name the LMM.
4. The model point tables stay. Their policies run for 10 years, so the tests and the
   notebook set `policy_term` to 2 on a copy of the table for the floorlet check, which
   with the example tenor of 12 months makes the second tenor date the maturity.

A script in the drafting repository did steps 1 to 3. As a lifelib example model,
`CashValue_ME_LMM` is described in its notebook, `lmm-tvog.ipynb`, as `CashValue_ME_G2PP`
is in `g2pp-tvog.ipynb`. The notebook shows the TVOG by fund and by tenor, the floorlet
check, and the same policies under `CashValue_ME_G2PP`. The two differ by more than the
level of volatility: with rates bounded below, a cash fund's guarantee is worth less out of
the money than under G2++, and a 10-year bond fund's more (Appendix A).

## 8. Validation and tests

**Unit (pytest, fast)**

- the workbook: its `Curve` and `Fund` sheets equal those of `g2pp_input.xlsx`; the
  example table equals its formula, rounded to six decimals; and the example run needs no
  extrapolation, and can start from any of the 12 curves
- interpolation: D(0; t_j) = P^M(0, t_j) at every month and κ_j = 1 on tenor dates (1e-15);
  `bank_return_mth(i)` equals 1/P(t_i, t_{i+1}) - 1, and bond returns equal the ratio of
  `P_t_T` prices (1e-13); an all-cash fund's returns equal `bank_return_mth` exactly
- a volatility table of zeros makes every stochastic scenario equal the CE row (1e-12)
- `caplet_vol` equals the sum of §4; `caplet_cf` satisfies put-call parity against the
  floorlet; the floorlet form of the GMAB equals the caplet formula by parity (1e-12)
- modelx outputs equal an independent numpy reference implementation with the same seed,
  to 1e-10, for the delivered workbook and for a second input set (tenor 3, another curve,
  continuous compounding, `BOND_10Y`, no antithetic variates, odd N, three factors, another
  shift). The tolerance is looser than G2++'s 1e-12, because the paths are not linear in
  the random numbers: in the prototype, runs that differ only in array shapes agree to
  1e-14 after 600 months
- reproducibility; extending `step_size` or `maturity_size` leaves earlier months unchanged
  (1e-12); the second half of the scenarios uses the negated random numbers of the first
- input errors: every rule of §5, including a curve or a volatility table that ends too
  early, an initial forward rate not above −`shift`, and a fund maturity beyond
  `maturity_size`
- the cells copied from `BasicG2PP` have the same formulas there and here, and
  `CashValue_ME_LMM`'s `ESG` equals `LMM` (`test_structure`)
- read → write → read round trip of `BasicLMM` and of `CashValue_ME_LMM`

**Statistical (marked slow; they run by default, and `-m "not slow"` leaves them out)**,
with standard errors from antithetic pair means and the pass rule of `BasicG2PP`: a check
with m z-scores passes if its largest |z| is below Φ⁻¹(1 - 0.00135/m). The runs peak at
385 to 850 MB.

- 10,000 scenarios over 20 years, tenor 12: the martingale, fund martingale (`BOND_MIX`
  and `BOND_10Y`) and curve-fit tests at every month; E[D(t_i) P(t_i,t_j)] = P^M(0,t_j)
  for four (i, j); `caplet_test()`; caplets at 0.75, 1 and 1.5 times the forward rate at 1,
  5 and 10 years; `summary()` passes
- 2,000 scenarios over 50 years, and 500 over 140 years (n = 1,680): the martingale, fund
  martingale and curve-fit tests
- 2,000 scenarios over 10 years with tenor 1: the same tests and `caplet_test()`, on a
  model with no interpolation

**Integration**, on `CashValue_ME_LMM`

- pathwise and exact, for every example fund and as for G2++: in every scenario s, CE
  included, the GMAB cost `pv_claims_over_av("MATURITY")` of the single-premium points
  equals D_s(T)(SA - AV0 Π_{t<T}(1 + R^F_{s,t}))⁺ recomputed from `fund_return_paths()`, to
  1e-10 × SA; the CE value equals (SA P^M(0,T) - AV0)⁺
- closed form: with `policy_term` 2 and the `CASH` fund, the mean GMAB cost over the
  stochastic scenarios is within the limit of `formula_gmab_floorlet(24)`;
  `formula_gmab_floorlet` raises `ValueError` for another maturity or another fund
- `result_tvog()`'s table, the projection longer than the scenarios, and the checks of the
  projection, as for `CashValue_ME_G2PP`

## 9. Possible extensions

None of these is needed by the current models:

- a helper that makes a `Vol` table from parametric volatilities and correlations, with
  tables of the caplet and swaption volatilities it implies
- a predictor-corrector step or a martingale discretisation as a setting
- a martingale (moment-matching) adjustment of the deflators
- a cap on rates
- volatilities that also depend on calendar time
- a smile beyond the shift (CEV, stochastic volatility)
- separate curves for discounting and for forward rates
- the possible extensions of [`g2pp_design.md`](g2pp_design.md) §9, which apply here too

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Rates explode over long horizons when volatility does not decay with time to expiry. With 10% for long expiries and a 2% shift, the 1-year rate at 50 years has a median of 8%, a 99th percentile of 350% and a mean of 29%, against a forward rate of 3.5% (Appendix A) | the example table decays, and gives a 99th percentile of 16% (decision 6); the notebook shows percentiles of rates next to the martingale tests, which pass even when rates explode; the docs page and the Notes sheet say what to look for; a cap on rates is a possible extension |
| Monte Carlo noise grows with the horizon. With the example input and 1,000 antithetic scenarios, the 95% half-width of mean D/P^M is ±0.10% at 10 years, ±0.30% at 30, ±1.3% at 50, ±5% at 100 and ±9% at 140 | as for G2++: antithetic on; TVOG standard errors from pair means; scenario counts per horizon in the docs |
| The monthly step is not exact, unlike G2++'s. With volatilities that explode, the bias of mean deflators reaches 2e-4 at 30 years | no bias is measurable with the example input (decision 4); the statistical tests would show one; a martingale discretisation and a predictor-corrector step are possible extensions |
| Memory and run time grow with scenarios × months × rates: 2.3 GB and 10 s for 1,000 scenarios × 600 months with a monthly tenor | the example tenor is 12 months; §6's table goes to the docs page; the statistical tests peak below 850 MB |
| A volatility table fits one tenor. With the example table, the TVOG of a 10-year guarantee on a cash fund is 10% higher with tenor 1 than with tenor 12, because the bank account then follows the 1-month rate instead of the 1-year rate | the Notes sheet and the docs page say so; the notebook shows the TVOG by tenor |
| With a tenor above one month, the bank-account return is fixed from the start of each tenor period, and bonds that mature within the period do not move | inherent to the interpolation; a shorter tenor where short maturities matter |
| Rates cannot fall below −`shift`, so guarantees that pay when rates are low are worth less than under a Gaussian model with the same volatility at the money | choose the shift with the calibration; the notebook compares the two example models |
| The GMAB has no closed form, so the TVOG example is checked less directly than G2++'s | the pathwise identity pins down timing and discounting for every fund; the floorlet identity checks a guarantee against a closed form; caplets check the distribution of the rates |
| The swaption formula is an approximation, up to 3.5% off away from the money | a diagnostic only, outside the pass rule of `summary()` |
| The cells copied from `BasicG2PP`, and the `ESG` copy of `LMM`, drift apart | tests compare the formulas (§8) |
| An initial curve with a forward rate at or below −`shift` | `mkt_fwd_rates()` raises `ValueError` before any simulation, naming the shift needed |
| A workbook edited in place is not reread; `_model.path` is None until the model has been written or read | as for `BasicG2PP`: document `model.clear_all()`; `input_path()` says to write the model and read it back |

## 11. Decisions

**Decided on 2026-11-23**, as the draft proposed them:

1. **Tenor**: `tenor_mth` is a setting (1, 2, 3, 4, 6 or 12 months), with 12 in the
   example. Fixing it at 12 would leave no way to make the bank account follow a short
   rate. Fixing it at 1 would remove the interpolation, but make a 50-year run cost 2.3 GB
   and 10 s per 1,000 scenarios.
2. **Volatility input**: a table of factor loadings by time to expiry, the `Vol` sheet. A
   few parameters in `Params` (a parametric volatility and correlation), with the rank
   reduction inside the model, would be shorter to enter. But the reduced factors would
   depend on the horizon, so extending `step_size` would change earlier months, and a
   parametric volatility with a floor invites exploding rates.
3. **Example values**: a 2% shift and the two-factor table of §5, chosen to resemble the
   G2++ example and to keep rates in a plausible range over 140 years. Like the G2++
   parameters, they are illustrative, not a calibration.
4. **Monthly step**: log-Euler (decision 4 of §3). Glasserman and Zhao's discretisation of
   deflated bond prices would follow G2++'s "exact by construction" most closely, at the
   same cost, but it makes caplets with a 1-year expiry 12% too cheap at 1.5 times the
   forward rate.
5. **TVOG example**: a second example model, `CashValue_ME_LMM`, self-contained like
   `CashValue_ME_G2PP`. A second ESG space in `CashValue_ME_G2PP`, switched by
   `lmm-tvog.ipynb`, would show that the liability model does not depend on the generator,
   but leave no model folder to open, and no place for `formula_gmab_floorlet`.
6. **Names, home and release**: `BasicLMM` with the space `LMM`, `lmm_input.xlsx` and
   `CashValue_ME_LMM`, in lifelib's `economic` library next to the G2++ models. Like them,
   they are drafted in the lifelib-dev/lifelib-economic repository and merged into lifelib
   from there, in a patch release as v0.17.4 was.

## Appendix A. Prototype check

A throwaway numpy script was run before the models were written, on the EUR_BASE curve of
`g2pp_input.xlsx` with a 2% shift, antithetic scenarios and, unless stated, annual forward
rates (tenor 12) and the example table of §5.

**Choice of the monthly step.** Four schemes ran on the same random numbers: log-Euler and
predictor-corrector (Hunter, Jäckel & Joshi 2001) on ln(F + α), and the two martingale
discretisations of Glasserman & Zhao (2000) under the spot measure, of deflated bond prices
and of their differences. The first row measures bias against the deflated-bond scheme,
whose mean deflators are exact; the caplet rows measure it against the predictor-corrector
scheme, whose caplets agree with Black's formula (|z| ≤ 2.0 over 15 expiries and strikes
with 400,000 scenarios).

| 40,000 scenarios × 600 months | log-Euler | predictor-corrector | deflated bonds | differences |
|---|---|---|---|---|
| mean deflator at 10, 30 and 50 years, difference ± SE | +0.8e-5 ± 1.5e-5, −0.2e-5 ± 4.8e-5, +1.9e-5 ± 7.3e-5 | +0.6e-5, −1.3e-5, +1.4e-5, same SE | exact | exact |
| at-the-money caplet at 1, 10 and 30 years | −0.005%, −0.017%, −0.016% | reference | +0.16%, +0.06%, +0.08% | within 0.005%, not significant (1 and 10 years) |
| caplet at 1.5 times the forward rate, at 1 and 10 years | −0.05%, −0.05% | reference | −12%, −0.3% | +0.5%, +0.2% |
| run time, relative | 1 | 1.7 | 0.8 | 1 |
| over 50 years with volatilities that explode | mean deflator +2e-4 at 30 years | the same | no failure | 0.8% of bond prices not positive |

The differences scheme recovers each bond as the numeraire bond minus a sum, which fails
once bond prices span many orders of magnitude. Its caplet figures come from 10-year runs
with 400,000 scenarios and the flat volatilities below. So log-Euler is the scheme that is
accurate for both bonds and caplets and does not fail.

**Exploding rates.** 10,000 scenarios × 600 months. "Flat" is Rebonato's form
(a + bu)e^{-cu} + d with a = 0.10, b = 0.10, c = 0.60 and d = 0.10 (20% at expiry, 10% for
long expiries), on three factors.

| 1-year rate | median | 99th percentile | 99.9th | maximum | share below 0 |
|---|---|---|---|---|---|
| flat volatility, at 10 years | 2.4% | 12% | 20% | 28% | 5% |
| flat volatility, at 30 years | 3.6% | 31% | 57% | 79% | 7% |
| flat volatility, at 50 years | 8.2% | 350% | 1,900% | 4,100% | 6% |
| example table, at 10 years | 2.5% | 9.4% | 13% | 20% | 2% |
| example table, at 30 years | 3.1% | 13% | 20% | 30% | 2% |
| example table, at 50 years | 3.7% | 16% | 24% | 36% | 1.5% |

With flat volatility the mean 1-year rate at 50 years is 29%, against a forward rate of
3.5%, and the standard deviation of ln D(T) is 3.0. With the example table the lowest
1-year rate was −1.3%, above the bound of −2%, and the standard deviation of ln D(T) is 0.09
at 10 years, 0.39 at 30 and 0.71 at 50, where the G2++ example has 0.11 at 10 and 0.60 at
50. A run of 2,000 scenarios over 140 years keeps the example's 99th percentile at 16% at
100 years and at 140, with maxima of 29% and 37%.

**Other checks**

| Check | Result |
|---|---|
| mean D(t)/P^M(0,t) at every month, largest \|z\| against its limit: 10,000 scenarios × 600 months, and 2,000 × 1,680 | 1.20 / 4.59, and 2.21 / 4.80 |
| deflated fund value at every month, `BOND_MIX` and `BOND_10Y`, same runs | 1.36 and 1.16, then 2.95 and 2.92; `CASH` is constant in every scenario |
| 95% half-width of mean D/P^M with 1,000 scenarios | 0.10% at 10 years, 0.30% at 30, 1.3% at 50, 5% at 100, 9% at 140 |
| GMAB at the second tenor date, all-cash fund, five account values, against the floorlet formula: tenor 12 (24 months) and tenor 6 with 200,000 scenarios, tenor 1 with 400,000 | \|z\| ≤ 0.8, 1.1 and 1.2 |
| swaptions at the money, Monte Carlo volatility against the approximation, 100,000 scenarios | +0.4% (5 years into 5), 0.0% (10 into 10), −0.4% (10 into 20), −0.5% (20 into 10); +3.5% at 1.25 times the swap rate (10 into 20) |
| κ_j over 110 years | within 1.5e-4 of 1 for tenor 12, 0.4e-4 for tenor 6, 0.1e-4 for tenor 3 |
| a longer `step_size` or `maturity_size`, earlier months | equal to 1e-14; not bit for bit |
| `JPY_DOWN` (first forward rate 0.02%), standard deviation of the 1-year rate at 10 years | 0.5% with no shift, 1.5% with 2% |

§6 gives the run times and memory of `BasicLMM` itself.

**GMAB of the TVOG example**: T = 10 years, SA = 50M, 10,000 scenarios, standard errors from
antithetic pair means. The columns are `CashValue_ME_G2PP`'s single-premium points, by
account value. The G2++ rows are that model's closed forms on the same curve.

| TVOG | AV0 = 50M | 47.5M | 40M | 37.5M | 30M |
|---|---|---|---|---|---|
| `CASH` | 0 (0) | 860 (302) | 1,124,894 (12,108) | 679,915 (8,846) | 13,569 (5,713) |
| `CASH`, G2++ | 22,775 | 79,078 | 1,445,854 | 843,310 | 6,112 |
| `BOND_10Y` | 72,782 (5,513) | 147,859 (7,775) | 1,286,277 (18,042) | 563,419 (14,970) | 579 (4,636) |
| `BOND_10Y`, G2++ | 19,166 | 69,855 | 1,407,136 | 809,690 | 4,931 |
| `BOND_MIX` | 3,053 (994) | 9,536 (1,684) | 676,601 (10,658) | 192,816 (7,689) | 169 (4,324) |

At AV0 = 40M, where the guarantee is near the money, the LMM example's values are 22%
(cash) and 9% (10-year bonds) below the G2++ example's, in line with its lower volatility
of ln D at 10 years. Away from the money the two part, because G2++'s rates are symmetric
and the LMM's are bounded below. The tenor matters for the cash fund: its TVOG at 40M is
1,124,894 with tenor 12, 1,182,920 with 6, 1,212,466 with 3 and 1,241,959 ± 20,460 with 1,
where `BOND_10Y`'s stays between 1,286,000 and 1,309,000.

A lognormal approximation of the GMAB, which freezes the coefficients g_j at their initial
values and applies the exchange-option formula of `formula_gmab_g2pp`, was tried for five
funds. At 40M it is within 5% of the Monte Carlo value (between −1.4% and +4.8%). At 37.5M
it is between −15% and +22% off, and at 47.5M and 50M it is wrong by multiples. It is not
used.

## References

- Brigo, D. and Mercurio, F. (2006). *Interest Rate Models - Theory and Practice with
  Smile, Inflation and Credit*, 2nd ed. Springer. Chapter 6, in particular §6.3 (the
  lognormal forward-LIBOR model), §6.3.1 (volatility structures), §6.3.2 (dynamics under
  the spot-LIBOR measure), §6.9.2 (rank reduction), §6.15 (Rebonato's formula) and §6.21
  (rates over non-standard periods); §10.1 (the shifted-lognormal model)
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer. §3.7
- Glasserman, P. and Zhao, X. (2000). Arbitrage-free discretization of lognormal forward
  Libor and swap rate models. *Finance and Stochastics* 4, 35-68
- Hunter, C., Jäckel, P. and Joshi, M. (2001). Getting the drift. *Risk*, July
- Schlögl, E. (2002). Arbitrage-free interpolation in models of market observable interest
  rates. In Sandmann, K. and Schönbucher, P. (eds), *Advances in Finance and Stochastics*.
  Springer. arXiv:1806.08107
