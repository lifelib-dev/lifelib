<h1 align="center" style="border-botom: none">
  <b>
    🐍 Nelson-Siegel-Svannson algorithm 🐍     
  </b>
</h1>

</br>

Popular algorithm for fitting a yield curve to obseved data. 

## Problem
Data on bond yields is usualy avalible only for a small set of maturities, while the user is normaly interested in a wider range of yields. 
  
## Solution
A popular solution is to use an algorithm to find a function that fits the existing datapoints. This way, the function can be used to interpolate/extrapolate any other point. The Nelson-Siegel-Svannson model is a curve-fitting-algorithm that is flexible enough to approximate most real world applications.

The Nelson-Siegel-Svensson is an extension of the 4-parameter Nelson-Siegel method to 6 parameters. The Scennson introduced two extra parameters to better fit the variety of shapes of either the instantaneous forward rate or yield curves that are observed in practice. 

Advantages:
-  It produces a smooth and well behaved forward rate curve. 
-  The intuitive explanation of the parameters. `beta0` is the long term interest rate and `beta0+beta1` is the instantaneous short-term rate. 

To find the optimal value of the parameters, the Nelder-Mead simplex algorithm is used (Already implemented in the scipy package). The link to the optimization algorithm is Gao, F. and Han, L. Implementing the Nelder-Mead simplex algorithm with adaptive parameters. 2012. Computational Optimization and Applications. 51:1, pp. 259-277.

The furmula for the yield curve (Value of the yield for a maturity at time 't') is given by the formula:

![formula](https://render.githubusercontent.com/render/math?math=\r(t)=\beta_{1}) +
![formula](https://render.githubusercontent.com/render/math?math=\beta_{2})
![formula](https://render.githubusercontent.com/render/math?math=\big(\frac{1-exp(\frac{-t}{\lambda_1})}{\frac{t}{\lambda_1}}\big)) +
![formula](https://render.githubusercontent.com/render/math?math=\beta_{3})
![formula](https://render.githubusercontent.com/render/math?math=\big(\frac{1-exp(\frac{-t}{\lambda_1})}{\frac{t}{\lambda_1}}-exp(\frac{-t}{\lambda_1})\big)) +
![formula](https://render.githubusercontent.com/render/math?math=\beta_{4})
![formula](https://render.githubusercontent.com/render/math?math=\big(\frac{1-exp(\frac{-t}{\lambda_2})}{\frac{t}{\lambda_2}}-exp(\frac{-t}{\lambda_2})\big))

### Parameters

   - Observed yield rates `YieldVec`.
   - Maturity of each observed yield `TimeVec`.
   - Initial guess for parameters `beta0`, `beta1`, `beta2`, `beta3`, `labda0`, and `lambda1`.
   - Target maturities `TimeResultVec`.

### Desired output

   - Calculated yield rates for maturities of interest `TimeResultVec`.

## Getting started

The user is interested in the projected yield for government bonds with a maturity in 1,2,5,10,25,30, and 31 years. They have data on government bonds maturing in 
1, 2, 5, 10, and 25 years. The calculated yield for those bonds are 0.39%, 0.61%, 1.66%, 2.58%, and 3.32%. 

  ```bash
from nelsonsiegelsvensson import *
import numpy as np

TimeVec = np.array([1,2,5,10,25])
YieldVec = np.array([0.0039, 0.0061, 0.0166, 0.0258, 0.0332])
beta0   = 0.1 # initial guess
beta1   = 0.1 # initial guess
beta2   = 0.1 # initial guess
beta3   = 0.1 # initial guess
lambda0 = 1 # initial guess
lambda1 = 1 # initial guess

TimeResultVec = np.array([1,2,5,10,25,30,31]) # Maturities for yields that we are interested in

## Implementation
OptiParam = NSSMinimize(beta0, beta1, beta2, beta3, lambda0, lambda1, TimeVec, YieldVec) # The Nelder-Mead simplex algorithem is used to find the parameters that result in a curve with the minimum residuals compared to the market data.

# Print the yield curve with optimal parameter to compare with the data provided
print(NelsonSiegelSvansson(TimeResultVec, OptiParam[0], OptiParam[1], OptiParam[2], OptiParam[3], OptiParam[4], OptiParam[5]))
```
