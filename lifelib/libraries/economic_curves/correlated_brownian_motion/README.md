# Sampled increments from two or more correlated Brownian motions (BM)   


Popular algorithm for generating a matrix of increments from a multidimensional Brownian motion (BM) with a given vector of means and a Variance-Covariance matrix.

## Problem

Offten when using multifactor models, the model requires correlated sources of noise. A popular choice is to use a multidimensional Brownian motion.

## Solution

The proposed algorithm uses two propoerties of BM:
-  Increments of a BM are normaly distributed.
-  assuming n independent BM's whose increments are generated from a standard normal distribution (denoted N(0,1)), a derived proces 
Y = μ + L\*z has its increments distributed as N(μ, E) where μ is the vector of means and L is the square root of the Variance-Covariance matrix (denoted E in the code).

### Inputs

- Vecor of means for each BM `mu`.
- Variance-Covariance matrix whose diagonal elements describe the volatility of each BM and the off-diagonal elements describe the covariance `E`.
- Number of samples needed `sampleSize`.

### Output

- Matrix of samples where each column represents a BM and each row a new increment.

## Getting started

The user is interested in generating samples from 2 Brownian motions with a correlation of 0.8. Additionaly, the first BM has a mean of 1 and a variance of 1.5. The second BM has a mean of 0 and a variance of 2. The user is interested in 100 samples.

```python
>>> import numpy as np

>>> from CorBM import CorBrownian

>>> mu = [1,0]

>>> VarCovar = np.matrix('1.5, 0.8; 0.8, 2')

>>> sampleSize = 480

>>> out = CorBrownian(mu, VarCovar, sampleSize)

>>> print(out)
[[ 3.01432184  0.21246299]
 [ 0.98350335  2.68478661]
 [ 1.42922771 -0.9489711 ]
 ...
 [ 1.74584652  0.79949231]
 [ 2.21807447 -0.14098937]
 [ 2.81308771  2.65884627]]
```
