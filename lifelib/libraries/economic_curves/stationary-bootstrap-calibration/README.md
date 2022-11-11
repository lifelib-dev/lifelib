<h1 align="center" style="border-botom: none">
  <b>
    🐍 Automatic calibration of the stationary bootstrap algorithm 🐍     
  </b>
</h1>

</br>

## Problem

Implementation of a stationary bootstrap method for weakly dependent stationary data requires the selection of the average block length as input. This can be time-consuming and introduce a degree of subjectivity into the implementation.

## Solution

The proposed methodology automatically estimates the optimal block size. As mentioned in the original paper, the methodology is based on the notion of spectral estimation via the flat-top lag-windows of Politis and Romano (1995). The proposed solution is described in the paper [Polis and White (2004)](http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf) 

### Input
- The time-series for which the calibration is necessary `data`

### Output
- Integer specifying the optimal block length

## Getting started
Given a time series with values 0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, and 0.2 the user desires to use the stationary bootstrap algorithm for resampling. The objective is to automatically retrieve the "optimal" value of the parameter needed for stationary bootstrap algorithm. 

```bash

import numpy as np

from stationary_bootstrap_calibrate import OptimalLength

data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])

m = OptimalLength(data)
```
