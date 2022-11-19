"""Smith-Wilson functions"""

import numpy as np


def SWCalibrate(r, M, ufr, alpha):
    """Calculate the calibration vector using a Smith-Wilson algorithm

    b = SWCalibrate(r, T, ufr, alpha) calculates the vector b used for
    interpolation and extrapolation of rates.

    Arguments:
       r:     n x 1 ndarray of rates, for which you wish to calibrate the algorithm. Each rate belongs to an observable zero-coupon bond with a known maturity. Ex. r = [[0.0024], [0.0034]]
       M:     n x 1 ndarray of maturities of bonds, that have rates provided in input (r). Ex. u=[[1], [3]]
       ufr:   1 x 1 floating number, representing the ultimate forward rate. Ex. ufr = 0.042
       alpha: 1 x 1 floating number representing the convergence speed parameter alpha. Ex. alpha = 0.05

    Returns:
       n x 1 ndarray array for the calibration vector needed to interpolate and extrapolate b = [[14], [-21]]
       rates

    For more information see https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
    """
    C = np.identity(M.size)
    p = (1+r) **(-M)  # Transform rates to implied market prices of a ZCB bond
    d = np.exp(-np.log(1+ufr) * M)    # Calculate vector d described in paragraph 138
    Q = np.diag(d) @ C                  # Matrix Q described in paragraph 139
    q = C.transpose() @ d                         # Vector q described in paragraph 139
    H = SWHeart(M, M, alpha) # Heart of the Wilson function from paragraph 132

    return np.linalg.inv(Q.transpose() @ H @ Q) @ (p-q)          # Calibration vector b from paragraph 149


def SWExtrapolate(M_Target, M_Obs, b, ufr, alpha):
    """Interpolate or/and extrapolate rates for targeted maturities using a Smith-Wilson algorithm.

    r = SWExtrapolate(T_Target,T_Obs, b, ufr, alpha) calculates the rates for maturities specified in M_Target using the calibration vector b.

    Arguments:
       M_Target:  k x 1 ndarray. Each element represents a bond maturity of interest. Ex. M_Target = [[1], [2], [3], [5]]
       M_Obs:     n x 1 ndarray. Observed bond maturities used for calibrating the calibration vector b. Ex. M_Obs = [[1], [3]]
       b:         n x 1 ndarray calibration vector calculated on observed bonds.
       ufr:       1 x 1 floating number, representing the ultimate forward rate. Ex. ufr = 0.042
       alpha:    1 x 1 floating number representing the convergence speed parameter alpha. Ex. alpha = 0.05

    Returns:
       k x 1 ndarray. Represents the targeted rates for a zero-coupon bond.
       Each rate belongs to a targeted zero-coupon bond with a maturity from T_Target. Ex. r = [0.0024; 0.0029; 0.0034; 0.0039]

    For more information see https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
    """
    C = np.identity(M_Obs.size)
    d = np.exp(-np.log(1+ufr) * M_Obs)     # Calculate vector d described in paragraph 138
    Q = np.diag(d) @ C                     # Matrix Q described in paragraph 139
    H = SWHeart(M_Target, M_Obs, alpha)    # Heart of the Wilson function from paragraph 132
    p = np.exp(-np.log(1+ufr)* M_Target) + np.diag(np.exp(-np.log(1+ufr) * M_Target)) @ H @ Q @ b # Discount pricing function for targeted maturities from paragraph 147
    return p ** (-1/ M_Target) -1   # Convert obtained prices to rates and return prices


def SWHeart(u, v, alpha):
    """Calculate the heart of the Wilson function.

    H = SWHeart(u, v, alpha) calculates the matrix H (Heart of the Wilson
    function) for maturities specified by vectors u and v. The formula is
    taken from the EIOPA technical specifications paragraph 132.

    Arguments:
       u:     n_1 x 1 vector of maturities. Ex. u = [1; 3]
       v:     n_2 x 1 vector of maturities. Ex. v = [1; 2; 3; 5]
       alpha: 1 x 1 floating number representing the convergence speed parameter alpha. Ex. alpha = 0.05

    Returns:
       n_1 x n_2 matrix representing the Heart of the Wilson function for selected maturities and parameter alpha.
       H is calculated as in the paragraph 132 of the EIOPA documentation.

    For more information see https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
    """
    u_Mat = np.tile(u, [v.size, 1]).transpose()
    v_Mat = np.tile(v, [u.size, 1])
    return 0.5 * (alpha * (u_Mat + v_Mat) + np.exp(-alpha * (u_Mat + v_Mat)) - alpha * np.absolute(
        u_Mat - v_Mat) - np.exp(
        -alpha * np.absolute(u_Mat - v_Mat)))  # Heart of the Wilson function from paragraph 132
