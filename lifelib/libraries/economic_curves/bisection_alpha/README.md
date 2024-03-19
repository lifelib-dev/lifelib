# Bisection method that finds the optimal parameter α for the Smith & Wilson algorithm     

This repository has an implementation for a simple bisection method that finds the optimal parameter α for the Smith & Wilson algorithm often used in insurance to interpolate/extrapolate rates or yields.

The implementation is based on [Technical documentation of the Methodology to derive EIOPA's risk-free interest rate term structure](https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf) and [Wiki on Bisection method](https://en.wikipedia.org/wiki/Bisection_method)

## Problem
Before using the Smith & Wilson algorithm, the user needs to provide the convergence speed parameter α. This parameter needs to be calibrated primarily so that that the extrapolated result matches the desired long-term behaviour.

## Solution
By transforming the minimization problem at the point of convergence into a problem of finding a root of the shifted function g(α) - τ, this repository implements a simple bisection algorithm to find the optimal α.

### Input
 - The minimum allowed value of the convergence speed parameter α.
 - The maximum allowed value of the convergence speed parameter α.
 - Maturities of bonds, observed on the market and provided as output.
 - Zero-coupon rates, for which the user wishes to calibrate the algorithm. Each rate belongs to an observable zero-coupon bond with a known maturity. 
 - The ultimate forward rate towards which the user wishes the resulting curve to converge.
 - Allowed difference between the given ultimate forward rate and the resulting curve. 
 - The numeric precision of the calculation. Higher the precision, more accurate the estimation of the root.
 - The maximum number of iterations allowed. This is to prevent an infinite loop in case the method does not converge to a solution.        
 
### Output
  - Optimal value of the parameter α (if the bisection method converged).
 
 Note that to be consistent with EIOPA's recommandations, the lower bound of the interval should be set to 0.05. 
 
## Getting started

```python
import numpy as np
from smith_wilson_funcs import SWCalibrate, SWExtrapolate
from bisection_alpha import Galfa as Galfa
from bisection_alpha import BisectionAlpha as BisectionAlpha

# maturities of bonds observed on the market
M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))

# yields observed on the market
r_Obs = np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]))

# ultimate forward rate
ufr = 0.04
# Numeric precision of the optimisation
Precision = 0.0000000001

# Targeted distance between the extrapolated curve and the ultimate forward rate at the convergence point
Tau = 0.0001 # 1 basis point

# Examples of a call to Galfa and BisectionAlpha
print("Example in the documentation for Galfa: "+ str(Galfa(M_Obs, r_Obs, ufr, 0.15, Tau)))
print("Example in the documentation for BisectionAlpha: "+ str(BisectionAlpha(0.05, 0.5, M_Obs, r_Obs, ufr, Tau, Precision, 1000)))
```

Note that this implementation use functions {func}`~economic_curves.smith_wilson.smith_wilson_funcs.SWCalibrate()` from 
the {doc}`smith_wilson` algorithm. 
They are duplicated to this repository for completeness. 

If there are any inconsistencies or suggestions, raise an [issue](https://github.com/lifelib-dev/lifelib/issues),
or contact [the original authors](https://github.com/open-source-modelling), 
or start a discussion at [lifelib Discussions](https://github.com/lifelib-dev/lifelib/discussions).
