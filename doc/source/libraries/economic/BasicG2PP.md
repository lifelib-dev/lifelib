```{module} economic.BasicG2PP
```

# The **BasicG2PP** Model

## Overview

{mod}`~economic.BasicG2PP` generates risk-neutral interest rate scenarios on a monthly
grid from G2++, the two-additive-factor Gaussian model, fitted exactly to an initial yield
curve. It reads all its inputs at run time from an Excel file. The scenarios are made for
calculating the time value of options and guarantees (TVOG) of lifelib's liability models,
as {mod}`~economic.CashValue_ME_G2PP` does for savings policies with a maturity guarantee.

Under the risk-neutral measure, the short rate is the sum of two correlated Gaussian
factors and a deterministic shift:

```{math}
r(t) = x(t) + y(t) + \varphi(t)

dx(t) = -a\,x(t)\,dt + \sigma\,dW_1(t), \qquad x(0) = 0

dy(t) = -b\,y(t)\,dt + \eta\,dW_2(t), \qquad y(0) = 0, \qquad dW_1(t)\,dW_2(t) = \rho\,dt
```

Time is in years, and month {math}`i` is {math}`t_i = i/12`. The scenarios are defined in
the {mod}`~economic.BasicG2PP.G2PP` space, and checks of them in the
{mod}`~economic.BasicG2PP.Validation` space. As in {mod}`~economic.BasicHullWhite`,
formulas operate on numpy arrays that hold all the scenarios at once.

```{seealso}
* [Damiano Brigo, Fabio Mercurio (2001, 2nd Ed. 2006). Interest Rate Models - Theory and Practice with Smile, Inflation and Credit](https://link.springer.com/book/10.1007/978-3-540-34604-3), section 4.2
* [Paul Glasserman (2003). Monte Carlo Methods in Financial Engineering](https://link.springer.com/book/10.1007/978-0-387-21617-1)
* {doc}`g2pp-simulation`, a notebook that shows the scenarios
```

### Fit to the initial curve

The shift {math}`\varphi` makes the model reproduce the initial discount factors
{math}`P^M(0, t)` exactly:

```{math}
\varphi(t) = f^M(0, t) + \frac{\sigma^2}{2a^2}\left(1 - e^{-at}\right)^2
+ \frac{\eta^2}{2b^2}\left(1 - e^{-bt}\right)^2
+ \frac{\rho\sigma\eta}{ab}\left(1 - e^{-at}\right)\left(1 - e^{-bt}\right)
```

where {math}`f^M(0, t)` is the initial instantaneous forward rate. The curve is entered as
spot rates at any set of maturities, annually or continuously compounded, and
{math}`\ln P^M(0, t)` is interpolated linearly between them, so the forward rates are flat
between maturities.

The curve is not extrapolated. It must reach every maturity a run needs: the projection
horizon {math}`t_n` for the deflators and the fund returns, and {math}`t_n` plus the tenor
for yields. A run that needs a maturity past the curve's last one raises an error that
names the maturity. The example curves run to 150 years.

### Exact monthly step

Each month, {math}`x`, {math}`y` and the integral of {math}`x + y` over the month are drawn
together from their exact Gaussian transition. With {math}`\Delta = 1/12`:

```{math}
x(t_{i+1}) = e^{-a\Delta}x(t_i) + \varepsilon_1, \qquad
y(t_{i+1}) = e^{-b\Delta}y(t_i) + \varepsilon_2

\int_{t_i}^{t_{i+1}} \left(x(u) + y(u)\right)du
= \frac{1 - e^{-a\Delta}}{a}\,x(t_i) + \frac{1 - e^{-b\Delta}}{b}\,y(t_i) + \varepsilon_3
```

The shocks {math}`(\varepsilon_1, \varepsilon_2, \varepsilon_3)` are normal, with the same
covariance every month ({func}`~economic.BasicG2PP.G2PP.cov_step`). The deflator, the
reciprocal of the bank account, is then

```{math}
D(t_i) = P^M(0, t_i)\exp\left(-\frac{1}{2}V(0, t_i) - \int_0^{t_i}\left(x(u) + y(u)\right)du\right)
```

where {math}`V(0, t)` is the variance of {math}`\int_0^t (x(u) + y(u))\,du`. So the expected
deflator equals the initial discount factor at every month, and the scenarios reproduce the
initial curve up to Monte Carlo noise, without any error from the time step. Zero-coupon
bond prices {math}`P(t_i, T)` follow in closed form from {math}`x(t_i)` and {math}`y(t_i)`
({func}`~economic.BasicG2PP.G2PP.P_t_T`), so yields of any tenor need no nested simulation.

The random numbers are laid out month by month, so extending the projection leaves the
earlier months unchanged. Antithetic variates are a setting of the input.

### Bond fund

The scenarios include the returns of a bond fund, in which liability models can invest
account values. The fund holds zero-coupon bonds in fixed shares by years to maturity, and
optionally a share in the bank account. Each month it sells its bonds and buys new ones at
the same maturities. Its market-value return over {math}`[t_i, t_{i+1})` is

```{math}
R^F_i = w_c R_i + \sum_m w_m\left[\frac{P(t_{i+1}, t_i + \tau_m)}{P(t_i, t_i + \tau_m)} - 1\right]
```

where {math}`w_c` is the share in the bank account, {math}`R_i = D(t_i)/D(t_{i+1}) - 1` the
bank-account return, and {math}`w_m` the share in bonds with {math}`\tau_m` years to
maturity. The return depends on interest rates only, and needs the curve only up to
{math}`t_{i+1}`. Because the fund trades only bonds and the bank account, its deflated value
is a martingale whatever the shares. An all-cash fund earns the bank-account return.

### The certainty-equivalent scenario

The outputs hold one row per scenario. Row 0 is the certainty-equivalent (CE) scenario,
which follows the initial forward curve: its deflators are {math}`P^M(0, t_i)`, and every
bond, and so every fund, earns the one-month forward rate. Rows 1 to N are the stochastic
scenarios. A single run of a liability model then gives both terms of the TVOG:

```{math}
\mathrm{TVOG} = \frac{1}{N}\sum_{k=1}^{N} PV_k - PV_0
```

where {math}`PV_k` is the present value of the liability cash flows in scenario {math}`k`.
The CE scenario is not the path with {math}`x = y = 0`, whose short rate
{math}`\varphi(t)` includes the convexity terms above. When you average over the stochastic
scenarios yourself, use rows 1 to N.

### Excel input

The model reads `g2pp_input.xlsx` from the folder that contains the model folder, so a copy
of the library runs as it is. To read another workbook, assign its file name or absolute
path to {attr}`~economic.BasicG2PP.G2PP.input_file`. The workbook has three sheets:

| Sheet    | Contents                                                                                                                                                                                                                      |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Params` | The G2++ parameters `a`, `b`, `sigma`, `eta` and `rho`, and the run settings: `scen_size` (N), `step_size` (the number of months, n), `seed`, `antithetic`, `curve_id`, `compounding` (`annual` or `continuous`) and `fund_id`. |
| `Curve`  | Spot rates by maturity in years, one column per curve ID. The example holds twelve curves to 150 years: EUR, GBP, JPY and USD, each BASE, UP and DOWN, from the EIOPA risk-free rates of December 2023 in {mod}`appliedlife`.  |
| `Fund`   | The shares of each fund, one column per fund ID, by years to maturity of zero-coupon bonds, or `cash` for the bank account. The example funds are `CASH`, `BOND_10Y` and `BOND_MIX`.                                          |

`BOND_10Y` holds 10-year bonds only, and `BOND_MIX` holds 20% in cash, 30% in 5-year bonds
and 50% in 10-year bonds. The example runs 1,000 antithetic scenarios over 50 years on
`EUR_BASE`, with `BOND_MIX`.

The example G2++ parameters are illustrative only. The model does not calibrate them, so
replace them with calibrated values. Each sheet is checked as it is read, and an invalid
input raises an error that lists every problem. The model caches what it reads: after
editing the workbook in place, call `clear_all()` on the model. Assigning another
{attr}`~economic.BasicG2PP.G2PP.input_file` recalculates automatically.

### Validation

The {mod}`~economic.BasicG2PP.Validation` space checks the scenarios of the current input
against closed forms and martingale properties: the mean deflators against the initial
curve, the deflated value of the fund against 1, the curve implied by the mean deflators,
the moments of {math}`x`, {math}`y` and {math}`r`, deflated bond prices, a put on a
zero-coupon bond and a call on the deflator. Each test returns the Monte Carlo estimate, the
value it should converge to, its standard error and the z-score of the difference. With
antithetic variates, the standard errors come from the means of antithetic pairs.

A test over many months or moments holds many z-scores, so a larger maximum is expected by
chance. {func}`~economic.BasicG2PP.Validation.summary` passes a test with {math}`m`
z-scores if its largest {math}`|z|` is below

```{math}
\Phi^{-1}\left(1 - \frac{0.00135}{m}\right)
```

which gives the same chance of a false alarm as a single 3-sigma check. The limit is about 3
for one z-score, and 4.6 for the 601 months of a 50-year run. The power of the tests grows
with the number of scenarios, and 10,000 antithetic scenarios is a good setting for
validation.

## Basic Usage

Create your copy of the **economic** library as explained on the {doc}`index` page, and read
the model from the library folder:

```python
>>> import modelx as mx

>>> model = mx.read_model("BasicG2PP")

>>> g2pp = model.G2PP
```

{func}`~economic.BasicG2PP.G2PP.disc_factor_paths` gives the deflators, and
{func}`~economic.BasicG2PP.G2PP.fund_return_paths` the returns of the bond fund, with one
row per scenario and one column per month:

```python
>>> g2pp.disc_factor_paths().shape
(1001, 601)

>>> g2pp.fund_return_paths().shape
(1001, 600)
```

{func}`~economic.BasicG2PP.G2PP.scenario_table` puts the deflators, the returns and the
short rates of every scenario and month in one table, for inspection and export:

```python
>>> g2pp.scenario_table()
             disc_factor  bank_return_mth  fund_return_mth  short_rate
scen_id t
0       0       1.000000         0.002755         0.002755    0.033019
        1       0.997252         0.002755         0.002755    0.033019
        2       0.994512         0.002755         0.002755    0.033019
        3       0.991779         0.002755         0.002755    0.033019
        4       0.989054         0.002755         0.002755    0.033019
...                  ...              ...              ...         ...
1000    596     0.240904         0.003531         0.002165    0.039056
        597     0.240056         0.003830         0.006053    0.045519
        598     0.239140         0.003739         0.000304    0.046216
        599     0.238249         0.003937         0.000180    0.046356
        600     0.237315              NaN              NaN    0.046273

[601601 rows x 4 columns]
```

{func}`~economic.BasicG2PP.Validation.summary` runs every check of the Validation space on
the current input:

```python
>>> model.Validation.summary()
                                checks  max_abs_z     limit    ok                              at
martingale_test()                  601   1.790468  4.587190  True                             198
fund_martingale_test()             601   2.043954  4.587190  True                             134
curve_fit_test()                    50   1.789351  4.037604  True                            17.0
moments_test()                     350   2.902763  4.472964  True                   (468, cov xy)
zcb_martingale_test(300, 360)        1   0.941041  2.999977  True                      (300, 360)
zbp_mc(300, 360, at the money)       1   0.108391  2.999977  True  (300, 360, 0.8632293178757527)
deflator_call_test(300, 0.9)         1   1.359685  2.999977  True                      (300, 0.9)
```

### Using the scenarios in a liability model

The outputs that a liability model needs follow the timing of lifelib's savings models:
cash flows at {math}`t` are discounted with {math}`D(t)`, and returns apply over
{math}`[t, t+1)`. Time 0 is the valuation date of the initial curve, and `step_size` must
cover the liability model's projection.

| Cells                                                   | Shape      | Use in a liability model                                                    |
|---------------------------------------------------------|------------|-----------------------------------------------------------------------------|
| {func}`~economic.BasicG2PP.G2PP.disc_factor_paths`      | (N+1, n+1) | deflators, in place of the discount factors                                 |
| {func}`~economic.BasicG2PP.G2PP.fund_return_paths`      | (N+1, n)   | returns of the bond fund, in place of the investment returns                |
| {func}`~economic.BasicG2PP.G2PP.bank_return_paths`      | (N+1, n)   | risk-free returns                                                           |
| {func}`~economic.BasicG2PP.G2PP.spot_rate_paths`        | (N+1, n+1) | market yields of any tenor, for dynamic lapses or crediting rates           |

{mod}`~economic.CashValue_ME_G2PP` shows how. It holds a copy of the
{mod}`~economic.BasicG2PP.G2PP` space as its space `ESG`, so that its model folder is
self-contained, and its Projection space refers to `ESG` through the Reference `esg`. The
copy reads `g2pp_input.xlsx` next to its own model folder.

## Model Specifications

{mod}`~economic.BasicG2PP` has two spaces: {mod}`~economic.BasicG2PP.G2PP`, which defines
the scenarios, and {mod}`~economic.BasicG2PP.Validation`, which checks them.

### The {mod}`~economic.BasicG2PP.G2PP` Space

```{eval-rst}
.. currentmodule:: economic.BasicG2PP

.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~G2PP
```

### The {mod}`~economic.BasicG2PP.Validation` Space

```{eval-rst}
.. currentmodule:: economic.BasicG2PP

.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~Validation
```
