def SWCalibrate(r, M, ufr, alpha):
# SWCALIBRATE Calculate the calibration vector using a Smith-Wilson algorithm
# b = SWCalibrate(r, T, ufr, alpha) calculates the vector b used for
# interpolation and extrapolation of rates.
#
# Arguments: 
#    r =     n x 1 ndarray of rates, for which you wish to calibrate the algorithm. Each rate belongs to an observable zero-coupon bond with a known maturity. Ex. r = [[0.0024], [0.0034]]
#    M =     n x 1 ndarray of maturities of bonds, that have rates provided in input (r). Ex. u=[[1], [3]]
#    ufr =   1 x 1 floating number, representing the ultimate forward rate. Ex. ufr = 0.042
#    alpha = 1 x 1 floating number representing the convergence speed parameter alpha. Ex. alpha = 0.05
#
# Returns:
#    n x 1 ndarray array for the calibration vector needed to interpolate and extrapolate b = [[14], [-21]]
#    rates
# For more information see https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf

    import numpy as np
    from SWHeart import SWHeart as SWHeart

    C = np.identity(M.size)
    p = (1+r) **(-M)  # Transform rates to implied market prices of a ZCB bond
    d = np.exp(-np.log(1+ufr) * M)    # Calculate vector d described in paragraph 138
    Q = np.diag(d) @ C                  # Matrix Q described in paragraph 139
    q = C.transpose() @ d                         # Vector q described in paragraph 139
    H = SWHeart(M, M, alpha) # Heart of the Wilson function from paragraph 132

    return np.linalg.inv(Q.transpose() @ H @ Q) @ (p-q)          # Calibration vector b from paragraph 149
