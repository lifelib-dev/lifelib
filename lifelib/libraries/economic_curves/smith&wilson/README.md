<h1 align="center" style="border-botom: none">
  <b>
    🐍 Smith & Wilson algorithm 🐍     
  </b>
</h1>

</br>

Popular algorithm for interpolating and extrapolating various curves such as bond yields and risk-free rates. 

This implementation is based on the [Technical documentation of the Methodology to derive EIOPA's risk-free interest rate term structure](https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf).

The link is for version published on 12/09/2019. See Section 7.

## Problem

When analysing market expectations of future rates, a common approach is to look at fixed income instruments such as government or corporate bonds that mature in the future. In practice, the maturities observable (and liquid) on the market rarely covers all the maturities that are needed.

## Solution

This implementation takes as input the <b>available market information</b>, <b>parameters</b> describing the long-term behaviour of the curve and the data on <b>desired (target) maturities</b> for which the yields are needed.

### Avalible market information
- Observed yields of the zero-coupon bonds (ZCB).
- Maturity of the observed ZCB.

### Parameters
- Ultimate froward rate `ufr` represents the rate to which the rate curve will converge as time increases.
- Convergence speed parameter α controls the speed at which the curve converges towards the ufr parameter from the last liquid point (last data point avalible in the market information input).

### Desired output
- List of maturities for which the SW algorithm will calculate the yields.

Note that this implementation assumes that the yields were calculated on ZCB. This assumption can be easily relaxed in future releases.

The implementation is split in two parts: 

- The available market data and the parameters are used to "calibrate" the algorithm. This returns a calibration vector that can be used to interpolate or extrapolate target maturities. This is done by calibrating the kernel functions. Look at the function `SWCalibrate()`.
- The yields for ZCB with targeted maturities are Interpolated/extrapolated. Look at the function `SWExtrapolate()`.

The syntax in the functions tries to be consistent with EIOPA technical specifications.

## Getting started

Given the data on 6 ZCB with maturities of 1, 2, 4, 5, 6, and 7 years with observed yields 1%, 2%, 3%, 3.2%, 3.5%, and 4% respectively. The user is interested in yields for ZCB at maturities 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, and 20 years. The given calibration for the parameter alpha is 0.15 and the ultimate forward rate is 4%. 

```bash
import numpy as np
from SWCalibrate import SWCalibrate as SWCalibrate
from SWExtrapolate import SWExtrapolate as SWExtrapolate

# yields observed on the market
r_Obs = np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04])) 

# maturities of bonds observed on the market
M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))  

# ultimate forward rate
ufr = 0.04 

# convergence speed parameter
alpha = 0.15 

# targeted maturities for interpolation/extrapolation
M_Target = np.transpose(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20])) 

# calibration vector calculation
b = SWCalibrate(r_Obs,M_Obs, ufr, alpha) 

# calculation of target yields
r_Target = SWExtrapolate(M_Target,M_Obs, b, ufr, alpha)

# display target yields
print("The interpolated/extrapolated rates are:") 
print(r_Target)
```

## About the example in main.py

Example.py contains a script with an example from EIOPA's own Excel implementation tool ( Smith-Wilson Risk-Free Interest Rate Extrapolation Tool 27102015.xlsb ). In this example, the yields are available for ZCB maturing in 1 year, 2 years, ..., 20 years. The output is the curve for up to 65 years.

###Note:
To extrapolate the curve, it is enough to know the additional parameters(alpha, ufr), the maturities used for calibration and the vector b*Q. If this is the case, it is not difficult to modify the function `SWExtrapolate()` to take as input Qb instead of b. To see an example of this, see the Jupyter Notebook at https://github.com/qnity/insurance_python/tree/main/EIOPA_smith_wilson_test .

An example of this format is the monthly risk free rate published by turopean Insurance and Occupational Pensions Authority (https://www.eiopa.europa.eu/tools-and-data/).

</br>

If you have any suggestions for improving the code/comments etc., please let us know.
