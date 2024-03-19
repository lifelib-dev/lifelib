```{eval-rst}
:html_theme.sidebar_secondary.remove:
```
```{module} economic_curves
```

# The **economic_curves** library

## Overview

This library includes Python scripts and notebooks
that contain practical algorithms for modeling economic scenarios, 
many of which are relevant to regulatory requirements
in UK and EU countries under the Solvency 2 regime.

```{seealso}
This library was based on 
[insurance_python](https://github.com/open-source-modelling/insurance_python), a library in an external project, 
the [Actuarial Algorithms](https://github.com/open-source-modelling), 
developed and maintained by Qnity Consultants and Gregor Fabjan.
```

```{seealso}
* {doc}`/libraries/economic/index` for a Hull-White model based on modelx
* {doc}`/projects/smithwilson` for a primitive Smith-Wilson implementation based on modelx
```

## How to Use the Library

As explained in the {ref}`create-a-project` section,
create you own copy of the *economic_curve* library.
For example, to copy as a folder named *curves*
under the path *C:\\path\\to\\your\\*, type below in an IPython console:

```python
>>> import lifelib

>>> lifelib.create("economic_curves", r"C:\path\to\your\curves")
```

This library does not use modelx.

This library uses the following packages. 
Most of the packages are pre-installed in major Python distributions,
but if any of them are missing, install them by `pip` or `conda` manually.

```{admonition} Additional packages used
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [SciPy](https://docs.scipy.org) ({doc}`Nelson-Siegel-Svensson<NelsonSiegelSvensson>` only) 
* [Matplotlib](https://matplotlib.org/)
```

## Algorithms available

Scripts and notebooks for each algorythm
are put in a sub-folder dedicated for the algorythm in this library.

```{toctree}
---
hidden:
--- 
smith_wilson
stationary_bootstrap_calibration
stationary_bootstrap
bisection_alpha
correlated_brownian_motion
NelsonSiegelSvensson
black_scholes
EIOPA_smith_wilson_test
Metropolis_Hastings
```

| Algorithm (Folder)                                                        | Source                    | Description                                                                 |
|---------------------------------------------------------------------------|---------------------------| ----------------------------------------------------------------------      |
| {doc}`smith_wilson<smith_wilson>`                                         | [Technical-documentation] | Interpolation and extrapolation of missing interest rates                   |
| {doc}`stationary_bootstrap_calibration<stationary_bootstrap_calibration>` | [Whitepaper-2004]         | Automatic calibration of the stationary bootstrap algorithm                 |
| {doc}`stationary_bootstrap<stationary_bootstrap>`                         | [Politis-Romano-1994]     | Resampling procedure for weakly dependent stationary observations           |
| {doc}`bisection_alpha<bisection_alpha>`                                   | [Technical-documentation] | Calibration of the Smith & Wilson's alpha parameter                         |
| {doc}`correlated_brownian_motion<correlated_brownian_motion>`             | [Wiki Brownian motion]    | Simple function to generate correlated Brownian motion in multiple dim.     |
| {doc}`NelsonSiegelSvensson<NelsonSiegelSvensson>`                         | [BIS whitepaper]          | Nelson-Siegel-Svansson model for approximating the yield curve              |
| {doc}`black_scholes<black_scholes>`                                       | [Wiki Black&Sholes]       | Black&Scholes model for pricing option contracts                            |
| {doc}`EIOPA_smith_wilson_test<EIOPA_smith_wilson_test>`                   | [EIOPA RFR website]       | Calculation of the risk free rate from the monthly EIOPA publication        |
| {doc}`Metropolis_Hastings<Metropolis_Hastings>`                           | Original work by OSM      | Bayesian maximum likelihood of a Black Sholes stochastic scenario generator |


[EIOPA RFR website]: https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en
[Technical-documentation]: https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
[Whitepaper-2004]: http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf
[Politis-Romano-1994]: https://www.jstor.org/stable/2290993
[Wiki Brownian motion]: https://en.wikipedia.org/wiki/Brownian_motion
[BIS whitepaper]: https://www.bis.org/publ/bppdf/bispap25l.pdf
[Wiki Black&Sholes]: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
[Wiki Vasicek]: https://en.wikipedia.org/wiki/Vasicek_model


