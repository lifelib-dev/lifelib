```{module} economic.BasicLMM
```

# The **BasicLMM** Model

## Overview

{mod}`~economic.BasicLMM` generates risk-neutral interest rate scenarios on a monthly grid
from the LIBOR market model (LMM), with shifted-lognormal forward rates fitted exactly to an
initial yield curve. It reads all its inputs at run time from an Excel file. Like
{mod}`~economic.BasicG2PP`, it makes scenarios for calculating the time value of options
and guarantees (TVOG) of lifelib's liability models, and its outputs have the same names
and shapes, so a liability model written for one runs on the other. The example model
`CashValue_ME_LMM` calculates the TVOG of savings policies with a maturity guarantee under
these scenarios (see {doc}`lmm-tvog`).

The model's variables are the forward rates {math}`F_k` for the periods
{math}`(T_{k-1}, T_k]` between the tenor dates {math}`T_k = k\tau`. The tenor {math}`\tau`
is 1, 2, 3, 4, 6 or 12 months, set in the input. Under the spot-LIBOR measure, whose
numeraire is the bank account that rolls over at each tenor date, {math}`F_k + \alpha` is
lognormal for a shift {math}`\alpha \ge 0`:

```{math}
\frac{d(F_k + \alpha)}{F_k + \alpha} = {} & \lambda_k \cdot \sum_{j=\beta(t)}^{k}
\frac{\tau(F_j + \alpha)}{1 + \tau F_j}\lambda_j\,dt \\
& + \lambda_k \cdot dW(t)
```

where {math}`W` is a Brownian motion with one dimension per factor, {math}`\lambda_k` the
volatility vector of {math}`F_k`, and {math}`\beta(t)` the first rate not yet set at
{math}`t`. The rates stay above {math}`-\alpha`, and a caplet on {math}`F_k` is priced by
Black's formula with the shifted rate and strike. A shift of 0 gives the lognormal LMM.

Time is in years, and month {math}`i` is {math}`t_i = i/12`. The scenarios are defined in
the {mod}`~economic.BasicLMM.LMM` space, and checks of them in the
{mod}`~economic.BasicLMM.Validation` space. As in {mod}`~economic.BasicG2PP`, formulas
operate on numpy arrays that hold all the scenarios at once.

```{seealso}
* [Damiano Brigo, Fabio Mercurio (2001, 2nd Ed. 2006). Interest Rate Models - Theory and Practice with Smile, Inflation and Credit](https://link.springer.com/book/10.1007/978-3-540-34604-3), chapter 6 and section 10.1
* [Erik Schlögl (2002). Arbitrage-Free Interpolation in Models of Market Observable Interest Rates](https://arxiv.org/abs/1806.08107), in K. Sandmann and P. Schönbucher (eds), Advances in Finance and Stochastics
* [Paul Glasserman (2003). Monte Carlo Methods in Financial Engineering](https://link.springer.com/book/10.1007/978-0-387-21617-1), section 3.7
* {doc}`lmm-simulation`, a notebook that shows the scenarios
```

### Volatility

The `Vol` sheet of the input gives the volatility vector of a forward rate as a function of
its time to expiry, with one column per factor, so the number of factors is the number of
columns. The length of a row is the rate's volatility, and the angle between two rows gives
the correlation of two rates. In the month from {math}`t_i`, a rate with {math}`m` months
to its expiry has the vector {math}`\lambda(m)` read from the table at the middle of the
month, {math}`(m - \frac{1}{2})/12` years, linearly between rows
({func}`~economic.BasicLMM.LMM.vol_loadings`). The volatility of each rate is constant
within each month, so the Black volatility {math}`\sigma_k` of a caplet on {math}`F_k`,
whose expiry {math}`T_{k-1}` is {math}`(k-1)\tau`, is an exact sum
({func}`~economic.BasicLMM.LMM.caplet_vol`):

```{math}
\sigma_k^2\,T_{k-1} = \frac{1}{12}\sum_{m=1}^{12T_{k-1}} \left|\lambda(m)\right|^2
```

Parametric forms of the volatility and the correlation, and the reduction of a full
correlation matrix to a few factors, are ways to make the table outside the model, like
the calibration. Because the factors do not depend on the run, extending the projection
leaves earlier months unchanged. The table is not extrapolated: it must reach the expiry of
the last forward rate that a run needs.

Volatility must fall with the time to expiry. High rates raise their own drift, so if the
volatility stays at 10% for long expiries, rates explode over long horizons: with a 2%
shift, the 99th percentile of the 1-year rate in 50 years is about 350%. The example table
holds two exponential factors with correlation −0.7, written as two independent ones, whose
volatility falls from 21% at expiry to 9% at 10 years and 2% at 30 years. It gives caplet
volatilities of 16% at 1 year, 13% at 10 years and 8% at 30 years, and keeps the 99th
percentile of the 1-year rate between 15% and 17% from 50 to 140 years.

### Monthly step

Each month, the logarithm of every rate not yet set, plus the shift, takes an Euler step
with the drift of the start of the month ({func}`~economic.BasicLMM.LMM.fwd_rates`). With
{math}`\Delta = 1/12`, a standard normal vector {math}`Z` and the rates
{math}`j = c+2, \dots, k` not yet set at {math}`t_i`:

```{math}
\ln(F_k(t_{i+1}) + \alpha) = {} & \ln(F_k(t_i) + \alpha)
+ \left(\mu_k - \tfrac{1}{2}|\lambda_k|^2\right)\Delta + \sqrt{\Delta}\,\lambda_k \cdot Z \\
\mu_k = {} & \lambda_k \cdot \sum_{j=c+2}^{k} \frac{\tau(F_j(t_i) + \alpha)}{1 + \tau F_j(t_i)}\lambda_j
```

Unlike the exact step of {mod}`~economic.BasicG2PP`, this step is not exact, but with the
example volatilities its error is too small to measure: on the same random numbers, the
deflators differ from those of a scheme that makes them exact martingales by less than
their Monte Carlo errors, and caplets agree with Black's formula. The caplet tests of the
{mod}`~economic.BasicLMM.Validation` space check this on any input. The random numbers are
laid out month by month, so extending the projection leaves the earlier months unchanged,
up to rounding. Antithetic variates are a setting of the input.

### Bonds, the bank account and the deflators

A bond that matures on a tenor date has a deflated price, its price divided by the bank
account, equal to a product of the rates
({func}`~economic.BasicLMM.LMM.defl_tenor_zcb`). With {math}`c` the last tenor date on or
before {math}`t_i`:

```{math}
D(t_i; T_k) = D(T_c)\prod_{j=c+1}^{k}\frac{1}{1 + \tau F_j(t_i)}
```

Each of these is a martingale. A bond that matures at month {math}`j = l p + r` between
two tenor dates, with {math}`p` the tenor in months and {math}`w = r/p`, has a deflated
price linear in maturity between those of the two tenor bonds
({func}`~economic.BasicLMM.LMM.defl_zcb`):

```{math}
D(t_i; t_j) = \kappa_j\left[(1 - w)D(t_i; T_l) + wD(t_i; T_{l+1})\right]
```

This is Schlögl's interpolation, in which a bond that matures within the current tenor
period has no volatility. As a fixed combination of martingales it is a martingale, so
every bond, the bank account and the bond fund are priced consistently. The factor
{math}`\kappa_j` ({func}`~economic.BasicLMM.LMM.curve_adj`), within 1.5e-4 of 1 on the
example curves, makes the model reproduce the initial curve at every month, not only at
tenor dates. With a tenor of one month nothing is interpolated.

The deflator, the reciprocal of the bank account, is the deflated price of the bond that
matures at {math}`t_i`, {math}`D(t_i) = D(t_i; t_i)`, so {math}`E[D(t_i)] = P^M(0, t_i)` at
every month. Bond prices are {math}`P(t_i, t_j) = D(t_i; t_j)/D(t_i)`, and yields of any
whole number of months follow without a nested simulation. The deflated price of a bond does
not change in its last month, so the bank-account return over a month is known at its
start. With a tenor longer than a month, the bank account earns the rate set at the last
tenor date until the next one. The LIBOR rate
{func}`~economic.BasicLMM.LMM.libor_rate` is the simply compounded rate for one tenor from
{math}`t_i`; on a tenor date it is the forward rate just set.

The rates that a run simulates must be fixed before it starts, so they cover `step_size`
plus `maturity_size` months of the input: bonds, and so the fund and yields, are
available up to `maturity_size` months after any projection month.

### Bond fund

As in {mod}`~economic.BasicG2PP`, the scenarios include the returns of a bond fund, in
which liability models can invest account values. The fund holds zero-coupon bonds in fixed
shares by years to maturity, and optionally a share in the bank account. Each month it sells
its bonds and buys new ones at the same maturities, so its market-value return over
{math}`[t_i, t_{i+1})` is

```{math}
R^F_i = w_c R_i + \sum_m w_m\left[\frac{P(t_{i+1}, t_i + \tau_m)}{P(t_i, t_i + \tau_m)} - 1\right]
```

where {math}`w_c` is the share in the bank account, {math}`R_i` the bank-account return,
and {math}`w_m` the share in bonds with {math}`\tau_m` years to maturity. Because the fund
trades only bonds and the bank account, its deflated value is a martingale whatever the
shares. An all-cash fund earns the bank-account return.

### The certainty-equivalent scenario

The outputs hold one row per scenario. Row 0 is the certainty-equivalent (CE) scenario, in
which every forward rate keeps its initial value: its deflators are {math}`P^M(0, t_i)`,
and every bond, and so every fund, earns the one-month forward rate. It equals
{mod}`~economic.BasicG2PP`'s CE scenario on the same curve. Rows 1 to N are the stochastic
scenarios. A single run of a liability model then gives both terms of the TVOG:

```{math}
\mathrm{TVOG} = \frac{1}{N}\sum_{k=1}^{N} PV_k - PV_0
```

where {math}`PV_k` is the present value of the liability cash flows in scenario {math}`k`.
When you average over the stochastic scenarios yourself, use rows 1 to N.

### Excel input

The model reads `lmm_input.xlsx` from the folder that contains the model folder, so a copy
of the library runs as it is. To read another workbook, assign its file name or absolute
path to {attr}`~economic.BasicLMM.LMM.input_file`. The workbook has four sheets of input:

| Sheet    | Contents                                                                                                                                                                                                                                                                                       |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Params` | The shift `shift`, the tenor of the forward rates in months `tenor_mth`, the number of monthly bond maturities to carry `maturity_size`, and the run settings: `scen_size` (N), `step_size` (the number of months, n), `seed`, `antithetic`, `curve_id`, `compounding` (`annual` or `continuous`) and `fund_id`. |
| `Curve`  | Spot rates by maturity in years, one column per curve ID: the same twelve curves to 150 years as in `g2pp_input.xlsx`, EUR, GBP, JPY and USD, each BASE, UP and DOWN, from the EIOPA risk-free rates of December 2023 in {mod}`appliedlife`.                                                       |
| `Vol`    | The volatility of the forward rates by time to expiry in years, one column per factor. The example holds two factors on 25 times to expiry from 0 to 150 years.                                                                                                                                    |
| `Fund`   | The shares of each fund, one column per fund ID, by years to maturity of zero-coupon bonds, or `cash` for the bank account: `CASH`, `BOND_10Y` and `BOND_MIX`, as in `g2pp_input.xlsx`.                                                                                                       |

The example runs 1,000 antithetic scenarios over 50 years on `EUR_BASE`, with annual
forward rates, a shift of 2%, 10 years of bond maturities and `BOND_MIX`. The example shift
and volatility table are illustrative only. The model does not calibrate them, so replace
them with calibrated values; a table is calibrated for one tenor.

Neither the curve nor the volatility table is extrapolated. The curve must reach the first
tenor date at or after `step_size` plus `maturity_size` months, 60 years for the example,
and the table the expiry of the last forward rate, one tenor earlier. Each sheet is checked
as it is read, and an invalid input raises an error that lists every problem, or names the
maturity that a run needs. The model caches what it reads: after editing the workbook in
place, call `clear_all()` on the model. Assigning another
{attr}`~economic.BasicLMM.LMM.input_file` recalculates automatically.

### Run time and memory

The model keeps the array of the forward rates of every month, so its memory grows with
the number of scenarios, the number of months and the number of rates, and with the square
of the horizon. For 1,000 scenarios with 10 years of bond maturities and two factors, the
main outputs take:

| Months | Tenor     | Forward rates | Time  | Memory   |
|--------|-----------|---------------|-------|----------|
| 120    | 12 months | 20            | 0.2 s | 45 MB    |
| 120    | 1 month   | 240           | 1.1 s | 200 MB   |
| 600    | 12 months | 60            | 1 s   | 320 MB   |
| 600    | 6 months  | 120           | 2 s   | 500 MB   |
| 600    | 3 months  | 240           | 4 s   | 880 MB   |
| 600    | 1 month   | 720           | 10 s  | 2.3 GB   |
| 1,680  | 12 months | 150           | 9 s   | 1.7 GB   |

So a monthly tenor suits horizons up to about 20 years, and a run to 140 years needs fewer
scenarios or more memory.

### Validation

The {mod}`~economic.BasicLMM.Validation` space checks the scenarios of the current input
against closed forms and martingale properties: the mean deflators against the initial
curve, the deflated value of the fund against 1, the curve implied by the mean deflators,
deflated bond prices, and caplets against Black's formula. Each test returns the Monte Carlo
estimate, the value it should converge to, its standard error and the z-score of the
difference. With antithetic variates, the standard errors come from the means of antithetic
pairs. In the first tenor period the deflators are known at time 0, and their z-scores are
0.

A test over many months or rates holds many z-scores, so a larger maximum is expected by
chance. {func}`~economic.BasicLMM.Validation.summary` passes a test with {math}`m` z-scores
if its largest {math}`|z|` is below

```{math}
\Phi^{-1}\left(1 - \frac{0.00135}{m}\right)
```

which gives the same chance of a false alarm as a single 3-sigma check. The power of the
tests grows with the number of scenarios, and 10,000 antithetic scenarios is a good setting
for validation. {func}`~economic.BasicLMM.Validation.swaption_test` compares the Monte Carlo
price of a swaption with Rebonato's approximation of its volatility,
{func}`~economic.BasicLMM.Validation.swaption_vol`. It is a diagnostic, left out of the
summary, because the formula is an approximation.

## Basic Usage

Create your copy of the **economic** library as explained on the {doc}`index` page, and read
the model from the library folder:

```python
>>> import modelx as mx

>>> model = mx.read_model("BasicLMM")

>>> lmm = model.LMM
```

{func}`~economic.BasicLMM.LMM.disc_factor_paths` gives the deflators, and
{func}`~economic.BasicLMM.LMM.fund_return_paths` the returns of the bond fund, with one
row per scenario and one column per month:

```python
>>> lmm.disc_factor_paths().shape
(1001, 601)

>>> lmm.fund_return_paths().shape
(1001, 600)
```

{func}`~economic.BasicLMM.LMM.scenario_table` puts the deflators, the returns and the
LIBOR rates of every scenario and month in one table, for inspection and export:

```python
>>> lmm.scenario_table()
             disc_factor  bank_return_mth  fund_return_mth  libor_rate
scen_id t
0       0       1.000000         0.002755         0.002755    0.033570
        1       0.997252         0.002755         0.002755    0.032455
        2       0.994512         0.002755         0.002755    0.031342
        3       0.991779         0.002755         0.002755    0.030230
        4       0.989054         0.002755         0.002755    0.029119
...                  ...              ...              ...         ...
1000    596     0.124002         0.004564        -0.004451    0.054950
        597     0.123439         0.004577        -0.002374    0.056668
        598     0.122876         0.004590        -0.001693    0.050275
        599     0.122315         0.004604         0.007876    0.050088
        600     0.121754              NaN              NaN    0.047920

[601601 rows x 4 columns]
```

{func}`~economic.BasicLMM.Validation.summary` runs every check of the Validation space on
the current input:

```python
>>> model.Validation.summary()
                               checks  max_abs_z     limit    ok          at
martingale_test()                 601   0.883662  4.587190  True         324
fund_martingale_test()            601   1.717591  4.587190  True           4
curve_fit_test()                   50   0.884137  4.037604  True        27.0
caplet_test()                      50   2.316520  4.037604  True  (21, 20.0)
zcb_martingale_test(300, 420)       1   1.550688  2.999977  True  (300, 420)
```

### Using the scenarios in a liability model

The outputs that a liability model needs have the names and shapes of
{mod}`~economic.BasicG2PP`'s, and follow the timing of lifelib's savings models: cash flows
at {math}`t` are discounted with {math}`D(t)`, and returns apply over {math}`[t, t+1)`.
Time 0 is the valuation date of the initial curve, and `step_size` must cover the liability
model's projection.

| Cells                                                   | Shape      | Use in a liability model                                                    |
|---------------------------------------------------------|------------|-----------------------------------------------------------------------------|
| {func}`~economic.BasicLMM.LMM.disc_factor_paths`        | (N+1, n+1) | deflators, in place of the discount factors                                 |
| {func}`~economic.BasicLMM.LMM.fund_return_paths`        | (N+1, n)   | returns of the bond fund, in place of the investment returns                |
| {func}`~economic.BasicLMM.LMM.bank_return_paths`        | (N+1, n)   | risk-free returns                                                           |
| {func}`~economic.BasicLMM.LMM.spot_rate_paths`          | (N+1, n+1) | market yields of up to `maturity_size` months, for dynamic lapses or crediting rates |
| {func}`~economic.BasicLMM.LMM.libor_rate_paths`         | (N+1, n+1) | LIBOR rates of one tenor                                                    |

The example model `CashValue_ME_LMM`, described in {doc}`lmm-tvog`, shows how. It is the
G2++ example model `CashValue_ME_G2PP` with a copy of the {mod}`~economic.BasicLMM.LMM`
space as its space `ESG`, which reads `lmm_input.xlsx` next to its own model folder. Its
`Projection` space needed no change, apart from the closed form it is checked against.

## Model Specifications

{mod}`~economic.BasicLMM` has two spaces: {mod}`~economic.BasicLMM.LMM`, which defines the
scenarios, and {mod}`~economic.BasicLMM.Validation`, which checks them.

### The {mod}`~economic.BasicLMM.LMM` Space

```{eval-rst}
.. currentmodule:: economic.BasicLMM

.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~LMM
```

### The {mod}`~economic.BasicLMM.Validation` Space

```{eval-rst}
.. currentmodule:: economic.BasicLMM

.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~Validation
```
