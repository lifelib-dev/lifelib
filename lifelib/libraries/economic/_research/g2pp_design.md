# BasicG2PP and CashValue_ME_G2PP: design note

*This note records the design of `BasicG2PP`, a G2++ economic scenario generator, and of
`CashValue_ME_G2PP`, the TVOG example that uses it: the mathematics, the Excel input, the
structure of the models, the interface to liability models, the tests and the decisions
behind them. It was made from the plan written while the models were drafted, in November
2026, in the lifelib-dev/lifelib-economic repository, and leaves out what concerned only the
drafting. The model folders are the source of truth: where they and this note differ, the
models are right. Paths are relative to the library folder, `lifelib/libraries/economic/`.*

## 1. Goal and scope

`BasicG2PP` is a modelx model that generates **risk-neutral, monthly, stochastic
interest-rate scenarios** from the two-additive-factor Gaussian model **G2++** (Brigo &
Mercurio, 2nd ed. 2006, §4.2), fitted exactly to an initial yield curve, with **all inputs
read from an Excel file**. Its outputs drive lifelib liability models so that

```
TVOG = mean over stochastic scenarios of PV(liability cash flows)
       - PV(liability cash flows) in the certainty-equivalent (CE) scenario
```

**In scope**

- G2++ under Q with exact fit to the initial curve (φ(t) derived from the curve)
- Monthly grid t_i = i/12, i = 0..n (i is the same index as `t` in lifelib liability models)
- Excel input: G2++ parameters, run settings, initial curve(s) with maturities up to 150
  years, and bond-fund shares by years to maturity
- Outputs per scenario and month: deflator (stochastic discount factor), bank-account
  return, short rate, zero-coupon bond prices and yields at any tenor, the market-value
  return of the bond fund, plus the CE scenario
- Validation: martingale tests, moment tests, closed-form option-price tests
- Worked TVOG example: lifelib `savings/CashValue_ME_EX4` driven by the generator, with the
  fund earning the bond fund's return

**Out of scope** (decided, §11): calibration of a, b, σ, η, ρ, which are calibrated
elsewhere and entered in Excel; extrapolation of the initial curve, which must itself reach
the projection horizon.

**Out of scope for v1**: real-world (P-measure) scenarios; equity, credit and inflation
models; multi-currency runs.

## 2. What lifelib already has, and how the design uses it

| Existing piece | What it does | Use in this design |
|---|---|---|
| `economic/BasicHullWhite` | Hull-White 1F. Per-step cells `short_rate(i)`, `disc_factor(i)`, `*_paths()` aggregations, B&M notation, flat 5% curve, parameters as References | Template for naming (`mkt_zcb`, `V_t_T`, `*_paths`), docstring style, and an η → 0 cross-check |
| `savings/CashValue_ME_EX1`, `EX4` | GMAB TVOG by Monte Carlo with GBM fund returns at a constant 2% rate, checked against a BSM put (`formula_option_put`). EX4 is the numpy-optimised version | Base of the TVOG example. The fund earns the return of a G2++ bond fund instead of a GBM return, and the BSM check becomes its G2++ counterpart (§4) |
| `appliedlife/IntegratedLife` | Reads Excel at run time via `pd.read_excel(_model.path.parent / file)`. Risk-free curves by currency with BASE/UP/DOWN sheets | Pattern for the Excel input. Source of the example curves |

BasicHullWhite discounts with a left-Riemann sum of short rates (`accum_short_rate`) and
also has an exact joint simulation (`accum_short_rate2`, after Glasserman 2003). BasicG2PP
uses the exact approach, extended to two factors.

## 3. Key design decisions

1. **Exact monthly discretisation.** Each step draws (x(t_{i+1}), y(t_{i+1}),
   ∫_{t_i}^{t_{i+1}}(x+y)du) jointly from their exact Gaussian transition (3 correlated
   normals per step). Then E[D(t_i)] = P^M(0,t_i) holds by construction, up to Monte
   Carlo noise, and deflators need only P^M(0,t), not the instantaneous forward curve.
   The prototype (Appendix A) shows the naive exp(-Σ r_i Δt) bias is small at monthly
   steps (about 2e-5 relative at 30 years), but the exact scheme costs no more and makes
   deflators independent of how forwards are interpolated.
2. **Bond prices in closed form.** P(t_i, T) for any T follows from x(t_i), y(t_i) (B&M
   §4.2, with the market fit), so yields at any tenor are available without nesting.
3. **Scenario 0 is the CE scenario.** Output arrays have rows scen_id = 0..N. Row 0 is the
   deterministic forward-curve scenario and rows 1..N are stochastic (lifelib already
   numbers stochastic scenarios from 1). One liability run yields both terms of TVOG.
   Confirmed in §11.
4. **Excel read at run time** (the appliedlife pattern). A Reference `input_file` names the
   workbook. Cells read it with `pd.read_excel(_model.path.parent / input_file, ...)`.
   Assigning a new `input_file` clears dependent cells automatically. After editing the
   workbook in place, call `model.clear_all()`.
5. **Parameters as zero-argument Cells** (`a()`, `sigma()`, ...), so the workbook is the
   single source of inputs. This differs from BasicHullWhite, which uses References.
6. **Variance reduction.** Antithetic variates on by default. A martingale (moment-matching)
   adjustment is a possible extension (§9).
7. **Random-number layout `(step_size, scen_size, 3)`**, step-major, so extending the
   horizon leaves earlier months unchanged.
8. **One main space** (like BasicHullWhite and CashValue_ME), so it can be copied whole
   into a liability model. Diagnostics live in a separate `Validation` space.
9. **No curve extrapolation.** The input curve must reach every maturity a run needs: the
   horizon t_n for deflators and bond-fund returns, and t_n plus the tenor for yields. The
   example curves run to 150 years. A maturity past the last knot raises an error instead
   of being extrapolated.
10. **Bond fund.** The liability model's fund holds zero-coupon bonds in fixed shares by
    years to maturity, set in Excel, plus an optional cash share in the bank account. Each
    month it sells the bonds and buys new ones at the same maturities (monthly
    rebalancing). Its returns are market-value returns from the closed-form bond prices, so
    they depend on interest rates only. An all-cash fund earns the bank-account return.

## 4. Mathematical specification (B&M 2006, §4.2 notation)

**Dynamics under Q**

```
r(t) = x(t) + y(t) + φ(t)
dx(t) = -a x(t) dt + σ dW1(t),   x(0) = 0
dy(t) = -b y(t) dt + η dW2(t),   y(0) = 0,    dW1 dW2 = ρ dt
```

**Fit to the initial curve**

```
φ(t) = f^M(0,t) + σ²/(2a²)(1-e^{-at})² + η²/(2b²)(1-e^{-bt})²
       + ρση/(ab)(1-e^{-at})(1-e^{-bt})

exp(-∫_0^t φ(u)du) = P^M(0,t) · exp(-V(0,t)/2)
```

**V(t,T)**, the variance of ∫_t^T (x+y)du given F_t, with τ = T - t:

```
V = σ²/a² [τ + (2/a)e^{-aτ} - (1/(2a))e^{-2aτ} - 3/(2a)]
  + η²/b² [τ + (2/b)e^{-bτ} - (1/(2b))e^{-2bτ} - 3/(2b)]
  + 2ρση/(ab) [τ + (e^{-aτ}-1)/a + (e^{-bτ}-1)/b - (e^{-(a+b)τ}-1)/(a+b)]
```

**Exact one-month step** (Δ = 1/12, Ba = (1-e^{-aΔ})/a, Bb = (1-e^{-bΔ})/b,
(ε1, ε2, ε3)ᵀ = L Z with Z ~ N(0, I₃) and L = chol(C)):

```
x(t_{i+1}) = x(t_i) e^{-aΔ} + ε1
y(t_{i+1}) = y(t_i) e^{-bΔ} + ε2
I_i := ∫_{t_i}^{t_{i+1}} (x+y) du = Ba x(t_i) + Bb y(t_i) + ε3
```

Conditional covariance C, which is constant because Δ is constant:

```
C11 = σ²(1-e^{-2aΔ})/(2a)
C22 = η²(1-e^{-2bΔ})/(2b)
C12 = ρση(1-e^{-(a+b)Δ})/(a+b)
C33 = V(t, t+Δ)
C13 = σ²(1-e^{-aΔ})²/(2a²) + (ρση/b)[(1-e^{-aΔ})/a - (1-e^{-(a+b)Δ})/(a+b)]
C23 = η²(1-e^{-bΔ})²/(2b²) + (ρση/a)[(1-e^{-bΔ})/b - (1-e^{-(a+b)Δ})/(a+b)]
```

If C is singular or nearly so (for example η = 0), fall back from `np.linalg.cholesky` to
a symmetric square root from `np.linalg.eigh`.

**Scenario quantities**

```
A(t_i)   = Σ_{k<i} I_k                                   (= ∫_0^{t_i}(x+y)du)
D(t_i)   = P^M(0,t_i) · exp(-V(0,t_i)/2 - A(t_i))        deflator = 1 / bank account
R_i      = D(t_i)/D(t_{i+1}) - 1                         bank-account return over [t_i, t_{i+1})
r(t_i)   = x(t_i) + y(t_i) + φ(t_i)                      short rate (diagnostic)
P(t_i,T) = P^M(0,T)/P^M(0,t_i)
           · exp(½[V(t_i,T) - V(0,T) + V(0,t_i)] - Ba(t_i,T) x(t_i) - Bb(t_i,T) y(t_i))
```

**CE scenario**: D_CE(t_i) = P^M(0,t_i), R_CE,i = P^M(0,t_i)/P^M(0,t_{i+1}) - 1,
P_CE(t_i,T) = P^M(0,T)/P^M(0,t_i). It is *not* the x = y = 0 path, which would include the
convexity terms in φ.

**Bond fund**: shares w_c in the bank account and w_m in zero-coupon bonds with τ_m years
to maturity, w_c + Σ w_m = 1. Bonds bought at t_i are sold at t_{i+1}, when τ_m - Δ is
left, and the fund rebalances to the same shares. Its market-value return over
[t_i, t_{i+1}) is

```
R^F_i = w_c R_i + Σ_m w_m [P(t_{i+1}, t_i+τ_m) / P(t_i, t_i+τ_m) - 1]

ln[P(t_{i+1}, T) / P(t_i, T)]                                   with T = t_i + τ
    = ln P^M(0,t_i) - ln P^M(0,t_{i+1}) + ½[V(τ-Δ) - V(τ) + V(0,t_{i+1}) - V(0,t_i)]
      - Ba(τ-Δ) x(t_{i+1}) - Bb(τ-Δ) y(t_{i+1}) + Ba(τ) x(t_i) + Bb(τ) y(t_i)
```

Here V(s) = V(t, t+s), Ba(s) = (1-e^{-as})/a and Bb(s) = (1-e^{-bs})/b. P^M(0,T) cancels,
so the returns need the curve only up to t_{i+1}. The account value
AV(t_i) = AV0 Π_{k<i}(1 + R^F_k) deflates to a martingale, E[D(t_i) AV(t_i)] = AV0, for any
shares, because the fund trades only bonds and the bank account. In the CE scenario every
bond earns the one-month forward, so the CE fund return is R_CE,i whatever the shares.

**Closed forms used by the tests**

- r(t) ~ N(φ(t), σ²(1-e^{-2at})/(2a) + η²(1-e^{-2bt})/(2b) + 2ρση(1-e^{-(a+b)t})/(a+b))
- Zero-coupon bond put (B&M §4.2):
  ```
  ZBP(0,T,S,K) = K P^M(0,T) N(-h + Σ) - P^M(0,S) N(-h)
  h  = ln(P^M(0,S) / (K P^M(0,T))) / Σ + Σ/2
  Σ² = σ²/(2a³)(1-e^{-a(S-T)})²(1-e^{-2aT}) + η²/(2b³)(1-e^{-b(S-T)})²(1-e^{-2bT})
     + 2ρση/(ab(a+b))(1-e^{-a(S-T)})(1-e^{-b(S-T)})(1-e^{-(a+b)T})
  ```
- Call on the deflator, since ln D(T) ~ N(ln P^M(0,T) - V/2, V) with V = V(0,T):
  E[(D(T) - K)⁺] = P^M(0,T) N(d1) - K N(d1 - √V), d1 = [ln(P^M(0,T)/K) + V/2]/√V
- GMAB on a single-premium policy with no fees or decrements. In every scenario the
  deflated payoff is D(T)(SA - AV(T))⁺ = (SA D(T) - AV0 G(T))⁺, where G(T) = D(T) AV(T)/AV0
  has mean 1. When the fund is all cash or a single bond maturity, ln D(T) and ln G(T) are
  jointly Gaussian, and the exchange-option (Margrabe) formula gives
  ```
  PV = SA P^M(0,T) N(d1) - AV0 N(d1 - s),   s² = Var[ln(AV(T)/AV0)]
  d1 = [ln(SA P^M(0,T) / AV0) + s²/2] / s
  ```
  For an all-cash fund G(T) = 1 and s² = V(0,T): PV is SA times a call on the deflator with
  K = AV0/SA, and the formula is EX1's BSM put (`formula_option_put`) with e^{-rT} replaced
  by P^M(0,T) and EX1's fund variance σ_S²T (σ_S = 3%) replaced by V(0,T). For a single
  maturity τ, ln AV is linear in x and y (formula above), so s² follows from a 3×3
  covariance recursion for (x, y, ln AV) over the months. A fund with several maturities
  has no exact closed form. The CE value is (SA P^M(0,T) - AV0)⁺ for any fund, and
  TVOG = PV - (SA P^M(0,T) - AV0)⁺.

## 5. Excel input: `g2pp_input.xlsx`, next to the model folder

**Sheet `Params`** (columns `parameter`, `value`, `description`)

| parameter | example | notes |
|---|---|---|
| `a` | 0.773 | mean reversion of x, > 0 |
| `b` | 0.082 | mean reversion of y, > 0 |
| `sigma` | 0.022 | volatility of x, > 0 |
| `eta` | 0.0104 | volatility of y, ≥ 0 |
| `rho` | -0.7 | correlation of W1 and W2, in [-1, 1] |
| `scen_size` | 1000 | number of stochastic scenarios N, even when antithetic |
| `step_size` | 600 | number of monthly steps n: at least the liability `max_proj_len()`, with n/12 no later than the curve's last maturity (n ≤ 1,800 for 150 years) |
| `seed` | 1234 | random seed |
| `antithetic` | TRUE | antithetic variates |
| `curve_id` | EUR_BASE | column of the `Curve` sheet to use |
| `compounding` | annual | compounding of the input spot rates: `annual` or `continuous` |
| `fund_id` | BOND_MIX | column of the `Fund` sheet to use |

The example parameters are illustrative only: strong mean reversion on x, slow on y and
negative ρ, the usual G2++ shape. Replace them with calibrated values.

**Sheet `Curve`**: column `maturity` (years, increasing, > 0, any grid, up to 150) plus one
column per curve ID holding spot rates. A curve ends at its last non-blank row. The
example sheet holds the curves of appliedlife's `economic_data/risk_free_202312.xlsx` (EUR,
GBP, JPY, USD × BASE, UP, DOWN, as columns such as `EUR_BASE`). All 12 of those curves run
from 1 to 150 years without gaps. In that file row k is maturity k+1.

**Curve construction**: ln P^M at the knots, with P^M(0,0) = 1, interpolated linearly in t
(flat instantaneous forwards between knots). There is **no extrapolation**: `mkt_zcb(i)`
raises `ValueError` for t_i past the last maturity. The instantaneous forward f^M(0,t) is
the flat forward of the knot interval containing t, using the last interval at the final
knot, so φ(t_n) needs nothing beyond t_n. Curves extrapolated elsewhere, such as EIOPA's
risk-free curves to 150 years, are entered as they are.

**Sheet `Fund`**: column `maturity` (years to maturity of each zero-coupon share, a whole
number of months, or `cash` for the bank account) plus one column per fund ID holding the
shares. A blank share is 0. The example workbook has three funds:

| maturity | CASH | BOND_MIX | BOND_10Y |
|---|---|---|---|
| cash | 1.0 | 0.2 | |
| 5 | | 0.3 | |
| 10 | | 0.5 | 1.0 |

`fund_id` selects the column, and the example uses `BOND_MIX`. `CASH` gives the
bank-account return. `CASH` and `BOND_10Y` have an exact GMAB closed form (§4), which the
tests use.

**Validation on read**: `param_table()` raises `ValueError` for a, b ≤ 0, σ ≤ 0, η < 0,
|ρ| > 1 or odd `scen_size` with antithetic on. `curve_table()` raises it for maturities
that are non-positive or not increasing, or a blank inside a curve. `curve_knots()` raises
it for a missing `curve_id`, or a curve that ends before t_n = `step_size()`/12.
`fund_table()` raises it for a maturity that is neither `cash` nor a positive whole number
of months, a repeated maturity, a negative share, or a fund whose shares do not sum to 1
(within 1e-9). Selecting a missing `fund_id` raises it too. Yields need
the curve out to t_i plus the tenor: with a 150-year curve, 10-year yields
(`spot_rate_paths(120)`) are available for projections up to 140 years. Past that,
`mkt_zcb` raises `ValueError` naming the maturity needed.

## 6. modelx model design

Edit the model folders directly or in Spyder-modelx. Scripts in the drafting repository
first created them through the modelx API, and are not kept in sync.

**Space `G2PP`** (i is the month index, `t_(i) = i/12` in years, N = `scen_size()`,
n = `step_size()`)

| Group | Cells | Returns | Return type |
|---|---|---|---|
| Input | `input_path()` | `input_file` resolved against the model's parent folder | `pathlib.Path` |
| | `param_table()` | validated values from the `Params` sheet | `pandas.Series` indexed by parameter name, object dtype (values mix numbers, booleans and strings) |
| | `curve_table()` | spot rates from the `Curve` sheet | `pandas.DataFrame` indexed by `maturity` (years), one float column per curve ID |
| | `fund_table()` | shares from the `Fund` sheet | `pandas.DataFrame` indexed by `maturity` (`"cash"` or years), one float column per fund ID |
| | `a()`, `b()`, `sigma()`, `eta()`, `rho()` | G2++ parameters | `float` |
| | `scen_size()`, `step_size()`, `seed()` | number of stochastic scenarios N, number of monthly steps n, random seed | `int` |
| | `antithetic()` | whether antithetic variates are used | `bool` |
| | `curve_id()`, `compounding()`, `fund_id()` | column of `Curve` to use; compounding of its rates (`"annual"` or `"continuous"`); column of `Fund` to use | `str` |
| Curve | `curve_knots()` | knot times t_k in years and ln P^M(0, t_k) of the selected curve, including t = 0; checks that the curve reaches t_n | `tuple` of two 1-D `numpy.ndarray`s of equal length |
| | `mkt_zcb(i)` | P^M(0, t_i) for t_i up to the last maturity; `ValueError` past it | `float` |
| | `mkt_fwd(i)` | f^M(0, t_i), the flat forward of the knot interval containing t_i (the last interval at the final knot) | `float` |
| Closed forms | `Ba_t_T(i, j)`, `Bb_t_T(i, j)` | (1-e^{-a(t_j-t_i)})/a and the b analogue | `float` |
| | `V_t_T(i, j)` | V(t_i, t_j) | `float` |
| | `phi(i)` | φ(t_i) | `float` |
| | `E_rt()`, `Var_rt()` | theoretical mean and variance of r(t_i) for all i | `numpy.ndarray`, shape (n+1,) |
| | `fund_logvar(j)` | s² = Var[ln(AV(t_j)/AV0)] for an all-cash or single-maturity fund (§4); `ValueError` for other funds | `float` |
| Simulation | `std_norm_rand()` | standard normal draws, antithetic if set | `numpy.ndarray`, shape (n, N, 3) |
| | `cov_step()`, `chol_step()` | C and its square root L | `numpy.ndarray`, shape (3, 3) |
| | `shocks(i)` | correlated shocks (ε1, ε2, ε3) for step i → i+1 | `numpy.ndarray`, shape (N, 3) |
| | `x(i)`, `y(i)` | factor values, x(0) = y(0) = 0 | `numpy.ndarray`, shape (N,) |
| | `accum_xy(i)` | A(t_i) | `numpy.ndarray`, shape (N,) |
| | `short_rate(i)` | r(t_i) | `numpy.ndarray`, shape (N,) |
| | `disc_factor(i)` | D(t_i) | `numpy.ndarray`, shape (N,) |
| | `bank_return_mth(i)` | R_i | `numpy.ndarray`, shape (N,) |
| | `P_t_T(i, j)` | P(t_i, t_j) by scenario | `numpy.ndarray`, shape (N,) |
| | `spot_rate(i, m)` | annually compounded m-month yield at t_i | `numpy.ndarray`, shape (N,) |
| | `swap_rate(i, k)` | k-year par rate with an annual fixed leg (optional) | `numpy.ndarray`, shape (N,) |
| Fund | `fund_cash_share()` | share of the selected fund in the bank account | `float` |
| | `fund_bond_shares()` | shares in zero-coupon bonds by maturity, zero shares dropped | `pandas.Series` of floats indexed by maturity in months (`int`) |
| | `zcb_return_mth(i, m)` | return over [t_i, t_{i+1}) of a zero-coupon bond with m months to maturity at t_i (§4) | `numpy.ndarray`, shape (N,) |
| | `fund_return_mth(i)` | R^F_i, the fund's market-value return over [t_i, t_{i+1}) | `numpy.ndarray`, shape (N,) |
| CE | `ce_disc_factor(i)`, `ce_bank_return_mth(i)`, `ce_short_rate(i)`, `ce_spot_rate(i, m)` | CE counterparts, one deterministic value each | `float` |
| Outputs (row 0 = CE) | `scen_index()` | scenario IDs 0..N, built as `pd.Index(range(N+1), name="scen_id")` | `pandas.RangeIndex` |
| | `disc_factor_paths()` | D(t_i) for every scenario and month | `numpy.ndarray`, shape (N+1, n+1) |
| | `bank_return_paths()` | R_i for every scenario and month | `numpy.ndarray`, shape (N+1, n) |
| | `fund_return_paths()` | R^F_i for every scenario and month; row 0 is the CE bank return | `numpy.ndarray`, shape (N+1, n) |
| | `short_rate_paths()` | r(t_i) for every scenario and month | `numpy.ndarray`, shape (N+1, n+1) |
| | `spot_rate_paths(m)` | m-month yields for every scenario and month | `numpy.ndarray`, shape (N+1, n+1) |
| | `scenario_table()` | `disc_factor`, `bank_return_mth`, `fund_return_mth` and `short_rate` for every scenario and month, for inspection and CSV/npz export (the returns are NaN at t = n) | `pandas.DataFrame` with a (`scen_id`, `t`) MultiIndex and one float column per quantity |

Arrays hold `float64` values, and a `float` may be a NumPy `float64`, which subclasses
`float`. A per-step array of shape (N,) holds stochastic scenarios 1..N in order. The
`*_paths()` arrays add the CE scenario as row 0, so row k is scen_id k.

References: `input_file = "g2pp_input.xlsx"`, `dt = 1/12`, `np`, `pd`.
`t_ = lambda i: i * dt`, as in BasicHullWhite.

**Space `Validation`**: `martingale_test()`, `fund_martingale_test()`, `curve_fit_test()`,
`zcb_martingale_test(i, j)`, `moments_test()`, `zbp_mc(i, j, K)` / `zbp_cf(i, j, K)`,
`deflator_call_test(i, k)` and `summary()`. Each test returns a DataFrame with columns
`mc` (Monte Carlo estimate), `theory`, `se` (from antithetic pair means) and `z`. Where an
estimate is exact by construction, such as the mean of x with antithetic variates or the
deflated value of an all-cash fund, z is 0. `summary()` lists the largest |z| of each test
against its limit (§8). References: `g2pp` (an Interface to `G2PP`), `np`, `pd`, `stats`
(scipy.stats) and `mcstats`, a small user module that computes the columns, saved in the
model folder as `mcstats.py` through `new_module`.

**Conventions**

- Docstrings with LaTeX math in B&M notation, ready for Sphinx like BasicHullWhite.
- Path cells assemble steps in increasing i, so recursion stays shallow. modelx's default
  recursion limit (100000) is not a constraint either way.
- Terms such as 1 - e^{-x} are computed with `numpy.expm1`, which keeps the digits the
  textbook form loses for small x (for example in C33 = V(Δ)). The reference
  implementation does the same, so the two agree to 1e-12.

**Memory**: roughly a dozen float arrays of length N per step (cached cells, shocks and
normals), plus one per bond maturity in the fund. That is about 60 MB for 1,000 × 600,
170 MB for the full 150 years with 1,000 scenarios (1,000 × 1,800) and 1.7 GB for
10,000 × 1,800, so document the limit and keep path cells optional. Measured peaks with
the Validation tests included are about 940 MB for 10,000 × 600 and 630 MB for
2,000 × 1,800.

## 7. Interface to liability models and the TVOG example

**Contract**

| Output | Shape | Meaning | Use in a liability model |
|---|---|---|---|
| `disc_factor_paths()` | (N+1, n+1) | D_k(t) | replaces `disc_factors(t)` |
| `fund_return_paths()` | (N+1, n) | market-value return of the bond fund over [t, t+1) | becomes `inv_return_mth(t)` |
| `bank_return_paths()` | (N+1, n) | risk-free return over [t, t+1) | diagnostics; equals `fund_return_paths()` for an all-cash fund |
| `spot_rate_paths(m)` | (N+1, n+1) | market yields | dynamic lapse or crediting rates (optional) |

The timing matches CashValue_ME: cash flows at t are discounted with D(t), and returns
apply over [t, t+1). The time origin is the valuation date of the input curve.

**`CashValue_ME_G2PP`**, derived from `savings/CashValue_ME_EX4`

1. Read `savings/CashValue_ME_EX4` and rename it.
2. Copy space `G2PP` from `BasicG2PP` into it as `ESG` with `UserSpace.copy(model, "ESG")`.
   Cross-model copying works: the copy has the same formulas, References and outputs. Only
   the docstring of the `t_` lambda is lost, and has to be set again. Add an
   Interface Reference `esg` in `Projection`. `ESG` reads `g2pp_input.xlsx` next to the
   model folder, like BasicG2PP.
3. Change `Projection`:
   - `scen_index()` → `esg.scen_index()` (0 = CE), so `model_point()` repeats each point
     N+1 times
   - `inv_return_table()` → `np.tile(esg.fund_return_paths(), (point_size(), 1))`. The fund
     earns the market-value return of the bond fund chosen by `fund_id`, and the CE row
     earns the one-month forwards whatever the shares. EX1/EX4's 3% fund volatility is not
     kept.
   - `disc_factors(t)` → `np.tile(esg.disc_factor_paths()[:, t], point_size())`
   - new `result_tvog()` by `point_id`: CE PV, mean stochastic PV, TVOG and its standard
     error for the GMAB cost (`pv_claims_over_av("MATURITY")`), GMDB cost and net cash flow.
     With antithetic pairs, compute the standard error from pair means.
   - new `formula_gmab_g2pp(t)`: the closed form from §4 for the single-premium points
     maturing at t, using `esg.fund_logvar(t)`, so it needs an all-cash or single-maturity
     fund. It replaces `formula_option_put`, which assumes a constant rate. In lifelib
     v0.17.3, EX4's version also failed as written, indexing 1-D arrays as 2-D
     (lifelib-dev/lifelib#182, since fixed).
   - drop `scen_size`, `std_norm_rand`, `disc_rate_ann` (with its data file),
     `disc_rate_mth` and `formula_option_put`, and also `scen_id = 1`, an unused leftover
     that would be misleading now that scen_id 0 is the CE scenario. `inv_return_table()`
     checks `max_proj_len() <= esg.step_size()`.
   - `check_pv_net_cf()` discounts each month with `disc_factors(t)`, which differ by
     scenario. EX4's version in lifelib v0.17.3 called `disc_factors()` without `t` and
     failed (lifelib-dev/lifelib#183, since fixed).
     `check_margin()` is left as it is; it returns False here as it does in EX4, because
     the margins leave out the GMAB claims.
4. Lighter alternative: keep the models separate and assign arrays as References, e.g.
   `liab.Projection.esg_disc_factors = esg.G2PP.disc_factor_paths()`.

To compare funds without editing the workbook, override the ESG's fund with
`esg.fund_id[()] = "CASH"`, which recalculates everything that depends on it;
`esg.fund_id.clear_all()` restores the workbook's value. `g2pp-tvog.ipynb` does this for the
three example funds.

## 8. Validation and tests

**Unit (pytest, fast)**

- C13, C23 and C33 against `scipy.integrate.quad` (relative 1e-9)
- the curve reproduces the input spot rates at the knots (1e-12)
- parameter and fund validation errors; a curve that ends before t_n, or any maturity past
  the last knot, raises `ValueError`
- bond returns from the §4 formula equal the ratio of full B&M bond prices (1e-12); an
  all-cash fund's returns equal `bank_return_mth` exactly
- `fund_logvar` from the recursion equals the direct quadratic form in x(t_k), y(t_k)
  (1e-12), and equals V(0,T) for an all-cash fund
- modelx outputs equal an independent pure-numpy reference implementation with the same
  seed (1e-12)
- reproducibility; extending `step_size` leaves earlier months unchanged; antithetic
  symmetry (mean of x is exactly 0)
- η = 0, ρ = 0 reproduces BasicHullWhite's `E_rt()` and `Var_rt()` on its default flat 5%
  continuously compounded curve, entered out to its 30 years (this exercises the singular-C
  fallback)
- read → write → read round trip of `BasicG2PP`

**Statistical** (marked slow; they run by default, and `-m "not slow"` leaves them out):
10,000 antithetic scenarios over 50 years, and 2,000 over 150 years. Standard errors come
from antithetic pair means;
treating the paths as independent overstates them. A check with m z-scores passes if its
largest |z| is below Φ⁻¹(1 - 0.00135/m). That gives the same 0.27% chance of a false
alarm as a single 3-sigma check: the limit is 3 for one z-score and about 4.6 for 600
months. A flat |z| < 3 rule would fail by chance on tests with hundreds of z-scores; the
1,000-scenario default run already reaches 2.9 in `moments_test`.

- martingale: mean D(t_i) against P^M(0,t_i) for every month, including the 150-year run
  (n = 1,800, N = 2,000); E[D(t_i) P(t_i,t_j)] = P^M(0,t_j) for four (i, j)
- fund martingale: mean D(t_i) AV(t_i)/AV0 against 1 for every month, for `BOND_MIX` and
  `BOND_10Y` (for `CASH` it holds in every scenario, a fast test)
- curve fit: spot rates implied by the mean deflators against the input curve
- moments of x, y and r against theory, every year
- ZBP Monte Carlo against the closed form: T = 10, S = 15, strikes at 98%, 100% and 102% of
  the forward bond price
- call on the deflator: at 10 years with k = 0.8, 0.9 and 1, and at 50 years with k = 0.9

**Integration**, on EX4's single-premium points (1, 2, 5, 6 and 9). The level-premium
points build up account values far above the sum assured, so their GMAB cost is zero.

- pathwise and exact, for every example fund: in every scenario, CE included, the GMAB
  cost `pv_claims_over_av("MATURITY")` equals D_k(T)(SA - AV0 Π_{t<T}(1 + R^F_{k,t}))⁺,
  recomputed from `fund_return_paths()`, with SA the total sum assured maturing and
  AV0 = `av_at(0, "BEF_FEE")`, to 1e-10 × SA. This pins down the timing of returns and
  discounting.
- for `CASH` and `BOND_10Y`, the mean over stochastic scenarios is within the limit for
  five z-scores (3.4, the rule above) of `formula_gmab_g2pp`; for every fund, the CE value
  equals (SA P^M(0,T) - AV0)⁺
- with P^M(0,T) = e^{-rT} and V(0,T) = σ²T, the all-cash closed form equals EX1's
  Black-Scholes put to 1e-12

## 9. Possible extensions

None of these is needed by the current models:

- a space parameterised by `curve_id` (`G2PP["EUR_UP"]`), for sensitivities
- a martingale (moment-matching) adjustment of the deflators, most useful at long horizons
- integration with the GMXB products of `appliedlife/IntegratedLife`
- export of the scenarios to files
- coupon-bond shares in the fund, which need the curve to reach the horizon plus the bond
  maturity
- buy-and-hold bond portfolios
- an approximate closed form for funds with several maturities

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Monte Carlo noise grows with the horizon. With the example parameters and 1,000 antithetic scenarios, the 95% half-width of mean D/P^M is about ±0.07% at 10 years, ±0.9% at 30, ±2.2% at 50, ±6% at 100 and ±10% at 150 (Appendix A; about 4.5 times smaller with 20,000) | antithetic on; report TVOG standard errors from pair means; a martingale adjustment is a possible extension (§9); suggest scenario counts per horizon |
| Gaussian model gives negative rates. With the example parameters P(r(t) < 0) is about 5% to 10% at every horizon, with a 1st percentile near -2% | inherent to G2++; report short-rate percentiles in the notebook |
| TVOG depends strongly on the fund's maturities, and not in one direction. For a 10-year GMAB, 5-year bonds give less than half the TVOG of cash, and 20-year bonds about double (Appendix A) | compare funds in the notebook; keep `CASH` in the workbook as a reference |
| Statistical tests with many z-scores raise false alarms under a flat 3-sigma rule | a limit per test that allows for its number of z-scores (§8); fixed seeds make the test suite repeatable |
| A curve too short for the horizon or for a yield tenor | `curve_knots()` checks the horizon before any simulation; `mkt_zcb` raises `ValueError` naming the maturity needed; the example curves run to 150 years |
| A workbook edited in place is not reread because cells are cached | document `model.clear_all()`; switching files through `input_file` recalculates automatically |
| `_model.path` is None until the model has been written or read | `input_path()` raises an error that says to write the model and read it back |
| `UserSpace.copy` across models may not work | verified: it works; only the `t_` lambda's docstring is lost, and has to be set again |
| Memory for large N × n | document the limits; keep path cells optional |

## 11. Decisions

**Decided on 2026-11-20** (item 4 extended on 2026-11-21)

1. **Curve input**: spot rates with log-linear discount-factor interpolation and **no
   extrapolation**. The input curve must cover the projection term, plus the tenor of any
   yield used; the workbook holds maturities up to 150 years.
2. **Parameters**: calibration is out of scope; a, b, σ, η, ρ are supplied in Excel.
3. **Integration target**: `CashValue_ME_EX4` → `CashValue_ME_G2PP`.
4. **Fund return in the TVOG example**: from interest rates only, without EX1/EX4's 3% fund
   volatility. The fund is a portfolio of zero-coupon bonds, rebalanced monthly to shares by
   years to maturity set in the `Fund` sheet, with an optional cash share. An all-cash fund
   earns the bank-account return.

**Decided on 2026-11-21**

5. **Scenario 0 = CE**: kept. Row 0 of every `*_paths()` array and `scen_id` 0 are the
   CE scenario, so one liability run gives both terms of TVOG. Means over the stochastic
   scenarios use rows 1 to N.
6. **Name and home**: `BasicG2PP` and `CashValue_ME_G2PP` go to lifelib's `economic`
   library, next to `BasicHullWhite`. The library is drafted in the
   lifelib-dev/lifelib-economic repository, at its path in lifelib and starting from a copy
   of lifelib's library, and merged into lifelib from there.

## Appendix A. Prototype check

A throwaway numpy script was run before the models were written, with the EUR BASE curve of
2023-12 from appliedlife, a = 0.773, b = 0.082, σ = 0.022, η = 0.0104, ρ = -0.7, and
20,000 antithetic scenarios × 600 months. It took 0.43 s. A second run, after the curve
decision, simulated 1,800 months (150 years) with no extrapolation in 0.85 s. A third run
added bond funds over 360 months (0.40 s for five funds); its results follow the table.

| Check | Result |
|---|---|
| mean D(t)/P^M(0,t) over all 1,800 months: largest absolute error divided by SE, with SE from antithetic pair means | 1.42; no month outside the 95% band |
| 95% half-width of mean D/P^M, 20,000 scenarios | 0.02% at 10 years, 0.20% at 30, 0.49% at 50, 1.35% at 100, 2.33% at 150 |
| standard deviation of ln D(T), √V(0,T) | 0.11 at 10 years, 0.60 at 50, 1.24 at 150 |
| variance and covariance of x(50), y(50) | 3.08e-4 vs 3.13e-4, 6.65e-4 vs 6.59e-4, -1.870e-4 vs -1.873e-4 (simulated vs theory) |
| ZBP(0, 10, 15), at the money | Monte Carlo 0.02404 ± 0.00043, closed form 0.02395 |
| E[D(10) P(10,15)] / P^M(0,15) | 1.0001 |
| call on D(10), strike 0.9 P^M(0,10); this is the §4 GMAB with AV0 = 0.9 SA P^M(0,10) | Monte Carlo 0.085848, closed form 0.085835 |
| C13, C23, C33 closed form vs `quad` | relative differences 2e-13, 4e-13, 2e-10 |
| naive exp(-Σ r_i Δt) vs exact, mean D/P^M | 30 years: 0.999248 vs 0.999230; 50 years: 0.997159 vs 0.997156 |

The ZBP's ± treats the 20,000 paths as independent, so it overstates the standard error
under antithetic sampling.

**Bond funds** (third run). The §4 return formula matched the ratio of full bond prices to
4e-16 in the log return, and the s² recursion matched the direct quadratic form to 1e-14.
The deflated value of every fund stayed within 1.7 SE of AV0 at every month. The table
shows a GMAB with T = 10, SA = 50M and AV0 = 40M. Its CE value is 0, so the PV is the TVOG.
Standard errors come from antithetic pair means.

| Fund | s/√T | Monte Carlo PV | Closed form |
|---|---|---|---|
| cash | 3.39% | 1,451,159 ± 14,020 | 1,445,854 |
| 5-year zeros | 1.77% | 657,448 ± 6,708 | 647,802 |
| 10-year zeros | 3.31% | 1,415,454 ± 10,476 | 1,407,136 |
| 20-year zeros | 6.19% | 2,852,814 ± 16,530 | 2,839,772 |
| 20% cash, 30% 5-year, 50% 10-year | 2.00% (sample) | 764,323 ± 7,192 | none |

With AV0 = 30M, deep in the money, every closed form was within 1 SE as well. The least
risky maturity grows with the term of the guarantee. Of the maturities in the s² recursion
(1 month, 5, 10 and 20 years), it is 5 years for a 10-year guarantee and 20 years for a
50-year one.

**Validation runs** (with the delivered parameters and seed). Each cell shows the
largest |z| and its limit (§8):

| Run | martingale | fund martingale | curve fit | moments |
|---|---|---|---|---|
| 10,000 scenarios, 50 years | 1.24 / 4.59 | 1.84 / 4.59 | 1.23 / 4.04 | 2.58 / 4.47 |
| 2,000 scenarios, 150 years | 2.56 / 4.81 | 2.61 / 4.81 | 2.56 / 4.29 | 4.66 / 4.70 |

In the 150-year run, `moments_test` passes only narrowly. The variance of y at year 46 is
17% below theory, and the z-score is inflated because the standard error is estimated from
that same low sample. It is sampling noise, not bias. Two other seeds give at most 3.6, and
400,000 independent scenarios with the model's own step covariance put the variances of x
and y and their covariance within 0.6% of theory (|z| ≤ 1.5) at 10, 46, 100 and 150
years. The 150-year statistical test therefore checks the martingale, fund martingale and
curve fit only.

**TVOG example** (the delivered input with 1,000 scenarios). In every scenario
the GMAB cost matched D(T)(SA - AV0 × fund growth)⁺ to 3e-15 of the sum assured, for all
three funds. GMAB TVOG of the single-premium points, Monte Carlo with its SE against the
closed form:

| Point | AV0 / (SA P(0,10)) | `CASH` | closed form | `BOND_10Y` | closed form | `BOND_MIX` |
|---|---|---|---|---|---|---|
| 1 | 1.267 | 30,139 (11,152) | 22,775 | 20,830 (7,190) | 19,166 | 0 (0) |
| 2 | 1.203 | 95,945 (19,976) | 79,078 | 74,277 (13,677) | 69,855 | 618 (453) |
| 5 | 1.013 | 1,499,775 (66,074) | 1,445,854 | 1,423,709 (46,774) | 1,407,136 | 771,177 (31,328) |
| 6 | 0.950 | 903,679 (61,062) | 843,310 | 820,980 (32,955) | 809,690 | 285,048 (21,916) |
| 9 | 0.760 | 24,362 (18,318) | 6,112 | -18,990 (21,597) | 4,931 | -2,084 (10,635) |

Every |z| is at most 1.11. The closed-form values of point 5 are the prototype's to the
unit (1,445,854 and 1,407,136, from the third run above).
