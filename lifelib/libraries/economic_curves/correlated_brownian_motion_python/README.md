<h1 align="center" style="border-botom: none">
  <b>
    🐍 Sampled increments from two or more correlated Brownian motions (BM) 🐍     
  </b>
</h1>

</br>

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

```bash
import numpy as np

mu = [1,0]
VarCovar = np.matrix('1.5, 0.8; 0.8, 2')
sampleSize = 480

out = CorBrownian(mu, VarCovar, sampleSize)
print(out)
>> [out] = [[ 3.01432184  0.21246299]
 [ 0.98350335  2.68478661]
 [ 1.42922771 -0.9489711 ]
 [-0.49778143 -3.0404678 ]
 [ 0.29396451  0.64626096]
 [ 0.80811248 -0.4542567 ]
 [ 0.29441548  0.41880222]
 [ 2.11883666  1.0262339 ]
 [ 3.17777954 -1.94769166]
 [ 0.02836758 -0.89723843]
 [ 1.41159275 -0.91685134]
 [ 0.80002199  0.94750505]
 [ 2.10351657 -0.97580137]
 [-0.67431779 -2.1930151 ]
 [-0.10431932 -0.00665984]
 [ 1.18779711  0.41885266]
 [ 1.54634453 -3.74537725]
 [ 4.10357654  3.50137711]
 [ 1.27666983 -0.202701  ]
 [ 1.45607394 -1.29394992]
 [ 4.42056013  1.17314064]
 [ 0.17981926  0.02718553]
 [ 2.08776471 -1.2151297 ]
 [ 0.00975734 -1.87426259]
 [ 0.44370952 -0.84889546]
 [-0.91702991 -0.64974021]
 [ 2.41707492 -0.48260669]
 [ 0.26420335 -1.08896695]
 [ 2.62254181 -0.06424235]
 [ 2.17341372  1.99310141]
 [ 2.71013259 -1.83770762]
 [-0.48606994 -0.92329548]
 [ 0.62851221 -2.64537566]
 [ 1.78415689  2.56601775]
 [ 0.85502579  1.50565467]
 [ 1.16226566 -0.49576818]
 [ 0.97005964  1.3292272 ]
 [ 0.74111532 -2.0000361 ]
 [ 1.52058537  0.32836389]
 [ 2.45704707  1.73679504]
 [ 1.46771852  1.08691729]
 [-1.23507574 -1.16338738]
 [ 0.16330948 -1.72058513]
 [-0.11886678 -0.71182892]
 [ 1.64520848  1.89947365]
 [-0.29259006 -0.13394478]
 [-0.32839732 -0.83890525]
 [-1.00189062 -0.14614664]
 [ 1.37039228  0.16268565]
 [ 3.35019224 -1.41428558]
 [ 2.35659306 -0.65411604]
 [ 1.04461038  1.3945269 ]
 [ 0.46508655  0.93780721]
 [-0.28913945 -0.60518967]
 [ 1.80189922  0.35159355]
 [ 0.57657657 -1.39084704]
 [ 1.27479344  0.27996933]
 [-0.30639903  2.54723502]
 [ 2.5373733   1.87532831]
 [-1.14445785 -2.47072282]
 [-0.59016974  0.66626821]
 [ 0.7555812  -1.30411159]
 [-1.08346996  2.02117262]
 [-0.41431095  1.37450613]
 [-1.06265565 -1.18989157]
 [ 1.80578244  1.79412479]
 [ 4.19777057  0.99893666]
 [ 0.50213584 -0.77556348]
 [ 1.9186039   1.09613311]
 [ 1.6930982   2.03285367]
 [-0.27571345 -0.98032212]
 [ 2.81264489 -1.780791  ]
 [ 0.06394456 -1.71073406]
 [ 1.73889537  1.51100972]
 [ 0.39641242 -0.351381  ]
 [ 2.99119662 -0.23606054]
 [ 2.93104271  1.63527194]
 [-0.53147698 -0.67081085]
 [ 1.6547926   0.16459858]
 [ 0.43974066 -0.0947692 ]
 [ 1.74082625  1.67718711]
 [ 0.99803465 -1.11834038]
 [ 0.20050859  0.25441171]
 [ 1.04611722  0.92303653]
 [ 0.77831377  0.25247936]
 [ 0.15764237 -1.45322145]
 [ 2.32716896  1.50761654]
 [ 0.46371323 -0.89645604]
 [ 2.08381869  2.13579417]
 [ 1.56593025  2.4389585 ]
 [-0.81187929  0.60117895]
 [ 0.32764279 -0.01306386]
 [ 1.41249816  0.24986421]
 [ 2.06642759  1.30855174]
 [-0.19649758 -0.63859554]
 [ 1.19242652  0.89506971]
 [ 0.35556785 -3.65657223]
 [ 1.74584652  0.79949231]
 [ 2.21807447 -0.14098937]
 [ 2.81308771  2.65884627]]
```
