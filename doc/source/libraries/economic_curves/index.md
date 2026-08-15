```{module} economic_curves
```

# The **economic_curves** library

```{warning}
The **economic_curves** library is now only a placeholder and no longer
contains any code or notebooks.

Between lifelib v0.8.0 and v0.13.0, this library mirrored
[insurance_python], a repository developed by [Open-Source Modelling].
Open-Source Modelling has kept improving their repositories since,
while the copy in lifelib was left untouched and became outdated.
Instead of shipping and rendering stale copies, lifelib now links
directly to the upstream repositories, so that you always get the
latest version of the algorithms and notebooks.

The sections below introduce Open-Source Modelling and their repositories.
```

## About Open-Source Modelling

[Open-Source Modelling] is an open-source project publishing
*"open-source algorithms for actuaries and risk managers"*,
developed and maintained by Gregor Fabjan and Qnity Consultants.
The project was formerly known as **Actuarial Algorithms**
and was rebranded as **Open-Source Modelling**.

Their algorithms cover the areas that actuaries and risk managers in the
UK and EU deal with in practice, such as interest rate extrapolation,
yield curve fitting, short rate models, resampling of economic time series
and option pricing. Many of them are directly relevant to the regulatory
requirements under the Solvency II regime, in particular to the
risk-free rate term structures published monthly by [EIOPA].

All of their repositories are published on GitHub under the MIT License.
The two entry points are:

* **[insurance_python]** — all the Python algorithms in one place.
* **[insurance_jupyter]** — all the Jupyter notebooks in one place.

## Algorithms in insurance_python

Each algorithm lives in its own folder in [insurance_python],
together with a `README.md` describing the algorithm, a module
implementing it and a `main.py` showing how to use it.

| Algorithm (Folder)                      | Source                    | Description                                                             |
| --------------------------------------- | ------------------------- | ----------------------------------------------------------------------- |
| [smith_wilson]                          | [Technical-documentation] | Interpolation and extrapolation of missing interest rates               |
| [stationary_bootstrap_calibration]      | [Whitepaper-2004]         | Automatic calibration of the stationary bootstrap algorithm             |
| [stationary_bootstrap]                  | [Politis-Romano-1994]     | Resampling procedure for weakly dependent stationary observations       |
| [bisection_alpha]                       | [Technical-documentation] | Calibration of the Smith & Wilson's alpha parameter                     |
| [correlated_brownian_motion]            | [Wiki Brownian motion]    | Simple function to generate correlated Brownian motion in multiple dim. |
| [nelson_siegel_svansson]                | [BIS whitepaper]          | Nelson-Siegel-Svansson model for approximating the yield curve          |
| [black_sholes]                          | [Wiki Black&Sholes]       | Black&Scholes model for pricing option contracts                        |
| [vasicek_one_factor]                    | [Wiki Vasicek]            | Vasicek model of the evolution of interest rates                        |
| [vasicek_two_factor]                    | [Wiki Vasicek]            | Vasicek model of the evolution of a pair of interest rates              |
| [hull_white_one_factor]                 | [Wiki Hull White]         | One factor Hull-White model of short rates                              |
| [dothan_one_factor]                     | [Quant Exchange]          | One factor Dothan model of short rates                                  |
| [singular_spectrum_analysis]            | [Paper SSA]               | Non-parametric technique for time series analysis and forecasting       |

(notebooks_economic_curves)=
## Notebooks in insurance_jupyter

[insurance_jupyter] collects the notebooks that Open-Source Modelling use
in model validation and when interacting with the European regulator.

| Notebook                                 | Source                    | Description                                                                 |
| ---------------------------------------- | ------------------------- | --------------------------------------------------------------------------- |
| [EIOPA RFR monthly tests]                | [EIOPA RFR website]       | Each monthly EIOPA submission is recalculated to check the published curve   |
| [EIOPA RFR custom maturities]            | [EIOPA RFR website]       | How to calculate a yield curve with custom maturities                        |
| [EIOPA RFR historic curves]              | [EIOPA RFR website]       | 134 months of EIOPA RFR curves that can be interpolated to any maturity      |
| [Metropolis-Hastings likelihood test]    | [Wiki Metropolis-Hastings]| Bayesian maximum likelihood of a Black-Scholes stochastic scenario generator |
| [Hull-White scenarios check]             | [Wiki Hull White]         | Checks if the number of stochastic scenarios covers the term structure       |

## Other repositories by Open-Source Modelling

Open-Source Modelling maintain a number of other repositories.
The ones below are the most actively developed at the time of writing.

| Repository                                     | Description                                                                                      |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [Open_Source_Economic_Model]                   | An open-source asset-liability model                                                             |
| [Light_Economic_Generator]                     | An open-source stochastic economic scenario generator                                            |
| [Validation_Economic_Stochastic_Generator]     | A validation framework for a monthly economic stochastic generator                               |
| [EIOPA_all_curves]                             | All the historical EIOPA risk-free curves for all countries                                      |
| [SFCR_using_Mistral_2025]                      | Solvency and Financial Condition Report tables of 22 Italian life insurers, extracted with OCR   |
| [IMF_GDP_pipeline]                             | Downloads and validates the latest IMF PPP GDP data                                              |
| [EDGAR_pipeline]                               | Downloads and cross-validates the EDGAR country level carbon emission data                       |
| [insurance_matlab]                             | All the Matlab algorithms in one place                                                           |

```{seealso}
* {doc}`/libraries/economic/index` for a Hull-White model based on modelx
* {doc}`/projects/smithwilson` for a primitive Smith-Wilson implementation based on modelx
```

[Open-Source Modelling]: https://github.com/open-source-modelling
[insurance_python]: https://github.com/open-source-modelling/insurance_python
[insurance_jupyter]: https://github.com/open-source-modelling/insurance_jupyter
[EIOPA]: https://www.eiopa.europa.eu/

[smith_wilson]: https://github.com/open-source-modelling/insurance_python/tree/main/smith_wilson
[stationary_bootstrap_calibration]: https://github.com/open-source-modelling/insurance_python/tree/main/stationary_bootstrap_calibration
[stationary_bootstrap]: https://github.com/open-source-modelling/insurance_python/tree/main/stationary_bootstrap
[bisection_alpha]: https://github.com/open-source-modelling/insurance_python/tree/main/bisection_alpha
[correlated_brownian_motion]: https://github.com/open-source-modelling/insurance_python/tree/main/correlated_brownian_motion
[nelson_siegel_svansson]: https://github.com/open-source-modelling/insurance_python/tree/main/nelson_siegel_svansson
[black_sholes]: https://github.com/open-source-modelling/insurance_python/tree/main/black_sholes
[vasicek_one_factor]: https://github.com/open-source-modelling/insurance_python/tree/main/vasicek_one_factor
[vasicek_two_factor]: https://github.com/open-source-modelling/insurance_python/tree/main/vasicek_two_factor
[hull_white_one_factor]: https://github.com/open-source-modelling/insurance_python/tree/main/hull_white_one_factor
[dothan_one_factor]: https://github.com/open-source-modelling/insurance_python/tree/main/dothan_one_factor
[singular_spectrum_analysis]: https://github.com/open-source-modelling/insurance_python/tree/main/singular_spectrum_analysis

[EIOPA RFR monthly tests]: https://github.com/open-source-modelling/insurance_jupyter/tree/main/EIOPA_smith_wilson_test
[EIOPA RFR custom maturities]: https://github.com/open-source-modelling/insurance_jupyter/blob/main/EIOPA_different_maturities/EIOPA%20RISK-FREE%20CURVE%20MONTHLY%20YIELD%20CALCULATION.ipynb
[EIOPA RFR historic curves]: https://github.com/open-source-modelling/insurance_jupyter/blob/main/EIOPA_historical_curves/EIOPA%20RISK-FREE%20CURVE%3B%20ALL%20OF%20THEM.ipynb
[Metropolis-Hastings likelihood test]: https://github.com/open-source-modelling/insurance_jupyter/blob/main/Metropolis_Hastings_Black_Sholes_ESG/METROPOLIS_HASTINGS_BLACK_SHOLES.ipynb
[Hull-White scenarios check]: https://github.com/open-source-modelling/insurance_jupyter/blob/main/hull_white_checks/HULL-WHITE%20AND%20EIOPA%20RISK-FREE%20CURVE%20TERM%20STRUCTURE%20COVERAGE%20AND%20VARIANCE%20CHECK.ipynb

[Open_Source_Economic_Model]: https://github.com/open-source-modelling/Open_Source_Economic_Model
[Light_Economic_Generator]: https://github.com/open-source-modelling/Light_Economic_Generator
[Validation_Economic_Stochastic_Generator]: https://github.com/open-source-modelling/Validation_Economic_Stochastic_Generator
[EIOPA_all_curves]: https://github.com/open-source-modelling/EIOPA_all_curves
[SFCR_using_Mistral_2025]: https://github.com/open-source-modelling/SFCR_using_Mistral_2025
[IMF_GDP_pipeline]: https://github.com/open-source-modelling/IMF_GDP_pipeline
[EDGAR_pipeline]: https://github.com/open-source-modelling/EDGAR_pipeline
[insurance_matlab]: https://github.com/open-source-modelling/insurance_matlab

[EIOPA RFR website]: https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en
[Technical-documentation]: https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
[Whitepaper-2004]: http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf
[Politis-Romano-1994]: https://www.jstor.org/stable/2290993
[Wiki Brownian motion]: https://en.wikipedia.org/wiki/Brownian_motion
[BIS whitepaper]: https://www.bis.org/publ/bppdf/bispap25l.pdf
[Wiki Black&Sholes]: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
[Wiki Vasicek]: https://en.wikipedia.org/wiki/Vasicek_model
[Wiki Hull White]: https://en.wikipedia.org/wiki/Hull%E2%80%93White_model
[Quant Exchange]: https://quant.stackexchange.com/questions/16017/for-the-dothan-model-eqbt-infty
[Paper SSA]: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5136637
[Wiki Metropolis-Hastings]: https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm
