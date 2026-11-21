```{module} economic.CashValue_ME_G2PP
```

# The **CashValue_ME_G2PP** Model

## Overview

{mod}`~economic.CashValue_ME_G2PP` calculates the time value of options and guarantees
(TVOG) of savings policies under the G2++ interest rate scenarios of
{mod}`~economic.BasicG2PP`. It is `CashValue_ME_EX4`, a model in the {mod}`savings` library,
with its economic inputs replaced. `CashValue_ME_EX1`, the model of
{doc}`/libraries/savings/savings_example1`, calculates the TVOG of a guaranteed minimum
accumulation benefit (GMAB) with lognormal fund returns, and `CashValue_ME_EX4` is its faster
version, made in {doc}`/libraries/savings/savings_example4`. Like them, this model assumes no
mortality, no lapses and no fees, so its results can be checked against a closed form.

Its space `ESG` is a copy of the {mod}`~economic.BasicG2PP.G2PP` space of
{mod}`~economic.BasicG2PP`, so the model folder is self-contained. `ESG` reads
`g2pp_input.xlsx` from the folder that contains the model folder, the workbook that
{mod}`~economic.BasicG2PP` reads too. In every scenario, the account values earn the returns
of the bond fund that the workbook selects, and the cash flows are discounted with the
deflators of the scenario. Scenario 0 is the certainty-equivalent (CE) scenario, which
follows the initial forward curve, so one run gives both terms of the TVOG:

```{math}
\mathrm{TVOG} = \frac{1}{N}\sum_{k=1}^{N} PV_k - PV_0
```

where {math}`PV_k` is the present value in scenario {math}`k`.

```{seealso}
* {doc}`g2pp-tvog`, a notebook that shows the TVOG of the GMAB and how it depends on the
  bond fund
* {doc}`BasicG2PP`, for the scenarios
```

### Changes from **CashValue_ME_EX4**

```{py:currentmodule} economic.CashValue_ME_G2PP.Projection
```

The {mod}`~economic.CashValue_ME_G2PP.Projection` space is EX4's, with these changes:

| Cells                     | Change                                                                                                                                                                                                   |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| {func}`scen_index`        | `ESG`'s scenario IDs: 0 is the CE scenario and 1 to N are stochastic, so {func}`model_point` repeats every model point N+1 times.                                                                        |
| {func}`inv_return_table`  | The market-value returns of the bond fund that `fund_id` selects in the workbook, instead of EX4's lognormal returns. In the CE scenario, every fund earns the one-month forward rates of the initial curve. |
| {func}`disc_factors`      | `ESG`'s deflators, which differ by scenario, instead of EX4's flat discount rate.                                                                                                                        |
| {func}`check_pv_net_cf`   | Discounts each month's net cash flows with the deflators of their scenarios.                                                                                                                             |
| {func}`result_tvog`       | New. The TVOG by model point.                                                                                                                                                                            |
| {func}`formula_gmab_g2pp` | New. The closed-form GMAB cost, in place of EX4's `formula_option_put`.                                                                                                                                  |

EX4's `scen_size`, `scen_id`, `std_norm_rand`, `disc_rate_ann`, `disc_rate_mth` and
`formula_option_put` are removed, and the Reference {attr}`esg` refers to `ESG`. The run
needs as many months of scenarios as the projection: {func}`inv_return_table` raises an
error if `step_size` in the workbook is shorter than {func}`max_proj_len`.
{func}`check_margin` is unchanged, and returns `False` here as it does in EX4, because the
margins leave out the GMAB claims.

### TVOG and its standard error

{func}`result_tvog` gives three present values by model point: the GMAB cost, which is the
maturity claim in excess of the account value (`pv_claims_over_av("MATURITY")`), the cost of
the guaranteed minimum death benefit (GMDB, `pv_claims_over_av("DEATH")`), and the net cash
flows ({func}`pv_net_cf`). For each of them it gives

* `CE`, the present value in the CE scenario,
* `mean`, the mean over the stochastic scenarios 1 to N,
* `TVOG`, `mean` minus `CE`,
* `SE`, the standard error of `mean`.

With antithetic variates, a scenario and its antithetic partner are not independent, so the
standard error comes from the means of the N/2 antithetic pairs. Treating the N scenarios as
independent would overstate it.

### Closed-form check

The single-premium model points have no fees or decrements, so their GMAB is a put on the
account value at maturity {math}`T`. When the fund is all cash or holds bonds of a single
maturity, the deflator and the deflated account value are jointly lognormal, and the
exchange-option formula gives the GMAB cost:

```{math}
PV = SA\,P^M(0, T)\,\Phi(d_1) - AV_0\,\Phi(d_1 - s), \qquad
d_1 = \frac{\ln\left(SA\,P^M(0, T)/AV_0\right) + s^2/2}{s}
```

{math}`SA` is the sum assured, {math}`AV_0` the account value at time 0 and {math}`s^2` the
variance of {math}`\ln(AV(T)/AV_0)`, which
{func}`~economic.BasicG2PP.G2PP.fund_logvar` calculates. {func}`formula_gmab_g2pp` gives this
value for the single-premium model points maturing at a given month. For an all-cash fund,
it is the Black-Scholes put of EX4's `formula_option_put`, with {math}`e^{-rT}` replaced by
{math}`P^M(0, T)` and {math}`\sigma^2 T` by {math}`V(0, T)`. A fund with several maturities,
such as `BOND_MIX`, has no exact closed form.

## Basic Usage

Create your copy of the **economic** library as explained on the {doc}`index` page, and read
the model from the library folder:

```python
>>> import modelx as mx

>>> cv = mx.read_model("CashValue_ME_G2PP")

>>> proj = cv.Projection
```

The example has nine model points of 10-year policies. Points 1, 2, 5, 6 and 9 are single
premium, and their account values at time 0 range from below to above the present value of
the sum assured. The GMAB part of {func}`result_tvog`, for the workbook's fund `BOND_MIX`:

```python
>>> proj.result_tvog()["GMAB"]
                    CE          mean           TVOG            SE
point_id
1         0.000000e+00  0.000000e+00       0.000000      0.000000
2         0.000000e+00  6.184628e+02     618.462780    453.317316
3         0.000000e+00  0.000000e+00       0.000000      0.000000
4         0.000000e+00  0.000000e+00       0.000000      0.000000
5         0.000000e+00  7.711766e+05  771176.626277  31327.931456
6         1.970018e+06  2.255066e+06  285048.026688  21915.760460
7         0.000000e+00  0.000000e+00       0.000000      0.000000
8         0.000000e+00  0.000000e+00       0.000000      0.000000
9         9.470018e+06  9.467934e+06   -2084.313487  10634.997900
```

To try another fund without editing the workbook, assign its ID to `fund_id` of `ESG`. With
the all-cash fund `CASH`, the closed form applies, and the Monte Carlo means are within about
one standard error of it:

```python
>>> cv.ESG.fund_id[()] = "CASH"

>>> proj.result_tvog()["GMAB"]
                    CE          mean          TVOG            SE
point_id
1         0.000000e+00  3.013865e+04  3.013865e+04  11151.987676
2         0.000000e+00  9.594523e+04  9.594523e+04  19976.459120
3         0.000000e+00  0.000000e+00  0.000000e+00      0.000000
4         0.000000e+00  0.000000e+00  0.000000e+00      0.000000
5         0.000000e+00  1.499775e+06  1.499775e+06  66073.513526
6         1.970018e+06  2.873698e+06  9.036792e+05  61062.244150
7         0.000000e+00  0.000000e+00  0.000000e+00      0.000000
8         0.000000e+00  0.000000e+00  0.000000e+00      0.000000
9         9.470018e+06  9.494380e+06  2.436156e+04  18318.211981

>>> proj.formula_gmab_g2pp(120)
point_id
1    2.277524e+04
2    7.907802e+04
5    1.445854e+06
6    2.813328e+06
9    9.476130e+06
Name: GMAB, dtype: float64

>>> cv.ESG.fund_id.clear_all()    # back to the workbook's fund
```

## Model Specifications

{mod}`~economic.CashValue_ME_G2PP` has two spaces:
{mod}`~economic.CashValue_ME_G2PP.Projection`, the liability model, and `ESG`, which
supplies the scenarios.

### The {mod}`~economic.CashValue_ME_G2PP.Projection` Space

```{eval-rst}
.. currentmodule:: economic.CashValue_ME_G2PP

.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~Projection
```

### The ESG Space

`ESG` is a copy of the {mod}`~economic.BasicG2PP.G2PP` space of {mod}`~economic.BasicG2PP`,
with the same Cells and References, so the {mod}`~economic.BasicG2PP.G2PP` page describes
it. The library's tests check that the two spaces stay the same.
