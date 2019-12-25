# README
## Overview
This Python package provides an implementation of the Smith-Wilson yield curve fitting algorithm for interpolations and extrapolations of zero-coupon bond rates. This algorithm is used for the extrapolation of [EIOPA risk-free term structures](https://eiopa.europa.eu/Publications/Standards/Technical%20Documentation%20(31%20Jan%202018).pdf) in the Solvency II framework. Details are available in the Technical Paper [QIS 5  Risk-free interest rates](https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf). Examples of extrapolated yield curves including the parameters applied can be found [here](https://eiopa.europa.eu/Publications/Standards/EIOPA_RFR_20190531.zip).
<br /><br />

## Implementation
The algorithm has been implemented in vectorized form with numpy. This should guarantee good performance. All functions are in [core.py](https://github.com/simicd/smith-wilson-py/blob/master/smithwilson/core.py).

The function `fit_smithwilson_rates()` expects following parameters:
- Observed rates 
- Observed maturities
- Target maturities
- Convergence parameter alpha 
- Ultimate forward rate (UFR)

The observed rates and maturities are assumed to be before the Last LiquidPoint (LLP). The targeted maturity vector can
contain both, more granular maturity structure (interpolation) or terms after the LLP (extrapolation).
<br /><br />


The fitting algorithm of the Smith-Wilson method calculates first the Wilson-matrix (EIOPA, 2010, p. 16):

    `W = e^(-UFR * (t1 + t2)) * (α * min(t1, t2) - 0.5 * e^(-α * max(t1, t2))
        * (e^(α * min(t1, t2)) - e^(-α * min(t1, t2))))`

Given the Wilson-matrix `W`, vector of UFR discount factors `μ` and prices `P`, the parameter vector `ζ` can be calculated as follows (EIOPA, 2010, p.17):

    `ζ = W^-1 * (μ - P)`

With the Smith-Wilson parameter `ζ` and Wilson-matrix `W`, the zero-coupon bond prices can be represented as (EIOPA, 2010, p. 18) in matrix notation:

    `P = e^(-t * UFR) - W * ζ`

In the last case, `t` can be any maturity vector, i.e. with additional maturities to extrapolate rates.
<br /><br />

## Usage
To use the Smith-Wilson fitting algorithm import the Python package and call `fit_smithwilson_rates()` with the required parameters. An example can be found in [main.py](https://github.com/simicd/smith-wilson-py/blob/master/main.py)
<br /><br />

## Sources
[EIOPA (2010). QIS 5 Technical Paper; Risk-free interest rates – Extrapolation method](https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf); p.11ff

[EIOPA (2018). Technical documentation of the methodology to derive EIOPA’srisk-free interest rate term structures](https://eiopa.europa.eu/Publications/Standards/Technical%20Documentation%20(31%20Jan%202018).pdf); p.37-46
<br /><br />

## Author
[Dejan Simic](https://www.linkedin.com/in/dejsimic/)
