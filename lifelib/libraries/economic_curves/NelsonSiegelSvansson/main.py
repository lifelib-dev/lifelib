# The Nelson-Siegel-Svensson is a popular extension of the 4-parameter Nelson-Siegel method to 6 parameters. It is an algorithm for interpolatin/extrapolating the yield curve among other uses.
# The Scennson introduces two extra parameters to better fit the variety of shapes of either the instantaneous forward rate or yield curves that are observed in practice.
# A desirable property of the model is that it produces a smooth and well behaved forward rate curve.
# Another desirable property is the intuitive explanation of the parameters. beta0 is the long term interest rate and beta0+beta1 is the instantaneous short-term rate.
# To find the optimal value of the parameters, the Nelder-Mead simplex algorithm is used (Already implemented in the scipy package). The link to the optimization algorithm is 
# Gao, F. and Han, L. Implementing the Nelder-Mead simplex algorithm with adaptive parameters. 2012. Computational Optimization and Applications. 51:1, pp. 259-277

from nelsonsiegelsvensson import *
import numpy as np

## Inputs
#   - Observed yield rates (YieldVec)
#   - Maturity of each observed yield (TimeVec)
#   - Initial guess for parameters (beta0, beta1, beta2,beta3, labda0 , and lambda1) 
#   - Target maturities (TimeResultVec)

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

