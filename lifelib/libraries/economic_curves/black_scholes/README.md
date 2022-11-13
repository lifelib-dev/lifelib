<h1 align="center" style="border-botom: none">
  <b>
    🐍 Black-Sholes model for simulating the price of a stock🐍     
  </b>
</h1>

Black Sholes model is one of oldest models for simulating the stock market.

## Problem

Modelling the stock market is a well researced field. There are numerous models each with their advantages and drawbacks.

## Solution

One of the oldest and simplest models developed is the [Black-Sholes-Merton](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) model which assumes that the asset prices can be described by the [Black-Sholes equation](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation). This implementation simulates the price of a stock in time.

### Input

Black Sholes simulation:
 - `S0`    ... integer, specifying the initial value of the underlying asset.
 - `mu`    ... float, specifying the drift rate of the underlying asset.
 - `sigma` ... float, standard deviation of the underlying asset's return.
 - `T`     ... integer, specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2.
 - `dt`    ... float, specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time.
 - `rho`  ... float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two Brownian motions have a correlation coefficient of 0.4.

### Output

Return:
 - `stock_price_simulation` ... N x 2 pandas DataFrame where index is modeling time and values are a realisation of the uderlying's price.

## Getting started

Model the price of a stock whitch is worth today 100. The market has a future annualized risk free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years)

``` python
import pandas as pd
import numpy as np
from typing import Any
from Black_Sholes import generate_weiner_process, simulate_Black_Scholes
print(simulate_Black_Scholes(100, 0.05, 0.3, 10, 0.5))

    #   [out] = Time    Stock Price                
    #       0.0    100.000000
    #       0.5    131.721286
    #       1.0    124.924654
    #       1.5    209.302935
    #       2.0    222.085955
    #       2.5    208.085678
    #       3.0    165.550253
    #       3.5    239.512165
    #       4.0    176.886669
    #       4.5    148.687363
    #       5.0    181.235262
    #       5.5    164.280753
    #       6.0    172.861576
    #       6.5    170.698562
    #       7.0    141.613940
    #       7.5    121.070316
    #       8.0    116.508183
    #       8.5    104.524616
    #       9.0    146.124924
    #       9.5    202.368581
    #       10.0   262.282989
```
## Risk neutral pricing
When an ESG simulation output is presented, a standard test is applied to confirm that the scenarios are risk neutral. Black Sholes can be one such model. This test relies on the fact that in a risk-neutral framework, there is an explicit relationship between the price of an fixed income financial instrument and the expected discounted cash flows. Bellow is the martingale test for the hypothetical example from above. To pass the test, the expected discounted cash flows should equal the initial stock price of 100.

``` python
import numpy as np
from Black_Sholes import simulate_Black_Scholes

r = 0.05
dt = 0.5
t = 10
S = 100
sigma = 0.3
bank_end = np.exp(t*r) # return of the risk-free asset
nIter = 500000
result = np.zeros(nIter)

for iter in range(1,nIter):
    out = simulate_Black_Scholes(S, r, sigma, t, dt)
    martingale = out.values[-1] / bank_end
    result[iter] = martingale

print(np.mean(result))
#   [out] = 99.8743118539787                

```
