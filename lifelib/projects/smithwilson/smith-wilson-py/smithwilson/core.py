
from math import exp, log
import numpy as np

def calculate_prices(rates: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Calculate prices from zero-coupon rates

    Args:
        rates: zero-coupon rates vector of length n
        t: time to maturity vector (in years) of length n

    Returns:
        Prices as vector of length n
    """

    return np.power(1 + rates, -t)


def ufr_discount_factor(ufr: float, t: np.ndarray) -> np.ndarray:
    """Calculate Ultimate Forward Rate (UFR) discount factors.

    Takes the UFR with a vector of maturities and returns for each of the
    maturities the discount factor
        d_UFR = e^(-UFR * t)

    Note that UFR is expected to be annualy compounded and that
    this function performs the calculation of the log return prior
    to applying the formula above.

    Args:
        ufr: Ultimate Forward Rate (annualized/annual compounding)
        t: time to maturity vector (in years) of length n

    Returns:
        UFR discount factors as vector of length n
    """

    # Convert annualized ultimate forward rate to log-return
    ufr = log(1 + ufr)
    return np.exp(-ufr * t)


def wilson_function(t1: np.ndarray, t2: np.ndarray, alpha: float, ufr: float) -> np.ndarray:
    """Calculate matrix of Wilson functions

    The Smith-Wilson method requires the calculation of a series of Wilson
    functions. The Wilson function is calculated for each maturity combination
    t1 and t2. If t1 and t2 are scalars, the result is a scalar. If t1 and t2
    are vectors of shape (m, 1) and (n, 1), then the result is a matrix of
    Wilson functions with shape (m, n) as defined on p. 16:
        W = e^(-UFR * (t1 + t2)) * (α * min(t1, t2) - 0.5 * e^(-α * max(t1, t2))
            * (e^(α * min(t1, t2)) - e^(-α * min(t1, t2))))

    Source: EIOPA QIS 5 Technical Paper; Risk-free interest rates – Extrapolation method; p.11ff
    https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf

    Args:
        t1: time to maturity vector of length m
        t2: time to maturity vector of length n
        alpha: Convergence speed parameter
        ufr: Ultimate Forward Rate (annualized/annual compounding)

    Returns:
        Wilson-matrix of shape (m, n) as numpy matrix
    """

    # Take time vectors of shape (nx1) and (mx1) and turn them into matrices of shape (mxn).
    # This is achieved by repeating the vectors along the axis 1. The operation is required
    # because the Wilson function needs all possible combinations of maturities to construct
    # the Wilson matrix
    m = len(t1)
    n = len(t2)
    t1_Mat = np.repeat(t1, n, axis=1)
    t2_Mat = np.repeat(t2, m, axis=1).T

    # Calculate the minimum and maximum of the two matrices
    min_t = np.minimum(t1_Mat, t2_Mat)
    max_t = np.maximum(t1_Mat, t2_Mat)

    # Calculate the UFR discount factor - p.16
    ufr_disc = ufr_discount_factor(ufr=ufr, t=(t1_Mat + t2_Mat))
    W = ufr_disc * (alpha * min_t - 0.5 * np.exp(-alpha * max_t) * \
        (np.exp(alpha * min_t) - np.exp(-alpha * min_t)))

    return W


def fit_parameters(rates: np.ndarray, t: np.ndarray, alpha: float, ufr: float) -> np.ndarray:
    """Calculate Smith-Wilson parameter vector ζ

    Given the Wilson-matrix, vector of discount factors and prices,
    the parameter vector can be calculated as follows (p.17):
        ζ = W^-1 * (μ - P)

    Source: EIOPA QIS 5 Technical Paper; Risk-free interest rates – Extrapolation method; p.11ff
    https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf

    Args:
        rates: Observed zero-coupon rates vector of length n
        t1: Observed time to maturity vector (in years) of length n
        alpha: Convergence speed parameter
        ufr: Ultimate Forward Rate (annualized/annual compounding)

    Returns:
        Wilson-matrix of shape (m, n) as numpy matrix
    """

    # Calcualte square matrix of Wilson functions, UFR discount vector and price vector
    # The price vector is calculated with zero-coupon rates and assumed face value of 1
    # For the estimation of zeta, t1 and t2 correspond both to the observed maturities
    W = wilson_function(t1=t, t2=t, alpha=alpha, ufr=ufr)
    mu = ufr_discount_factor(ufr=ufr, t=t)
    P = calculate_prices(rates=rates, t=t)

    # Calculate vector of parameters (p. 17)
    # To invert the Wilson-matrix, conversion to type matrix is required
    zeta = np.matrix(W).I * (mu - P)
    zeta = np.array(zeta) # Convert back to more general array type

    return zeta


def fit_smithwilson_rates(rates_obs: np.ndarray, t_obs: np.ndarray, t_target: np.ndarray,
                                alpha: float, ufr: float) -> np.ndarray:
    """Calculate zero-coupon yields with Smith-Wilson method based on observed rates.

    This function expects the rates and initial maturity vector to be
    before the Last Liquid Point (LLP). The targeted maturity vector can
    contain both, more granular maturity structure (interpolation) or terms after
    the LLP (extrapolation).

    The Smith-Wilson method calculated first the Wilson-matrix (p. 16):
        W = e^(-UFR * (t1 + t2)) * (α * min(t1, t2) - 0.5 * e^(-α * max(t1, t2))
            * (e^(α * min(t1, t2)) - e^(-α * min(t1, t2))))

    Given the Wilson-matrix, vector of discount factors and prices,
    the parameter vector can be calculated as follows (p.17):
        ζ = W^-1 * (μ - P)

    With the Smith-Wilson parameter and Wilson-matrix, the zero-coupon bond
    prices can be represented as (p. 18) in matrix notation:
        P = e^(-t * UFR) - W * zeta

    In the last case, t can be any maturity vector

    Source: EIOPA QIS 5 Technical Paper; Risk-free interest rates – Extrapolation method; p.11ff
    https://eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf

    Args:
        rates_obs: Initially observed zero-coupon rates vector before LLP of length n
        t_obs: Initially observed time to maturity vector (in years) of length n
        t_target: New targeted maturity vector (in years) with interpolated/extrapolated terms
        alpha: Convergence speed parameter
        ufr: Ultimate Forward Rate (annualized/annual compounding)

    Returns:
        Vector of zero-coupon rates with Smith-Wilson interpolated or extrapolated rates
    """

    # Convert list to numpy array and use reshape to convert from 1-d to 2-d array
    # E.g. reshape((-1, 1)) converts an input of shape (10,) with second dimension
    # being empty (1-d vector) to shape (10, 1) where second dimension is 1 (2-d vector)
    rates_obs = np.array(rates_obs).reshape((-1, 1))
    t_obs = np.array(t_obs).reshape((-1, 1))
    t_target = np.array(t_target).reshape((-1, 1))

    zeta = fit_parameters(rates=rates_obs, t=t_obs, alpha=alpha, ufr=ufr)
    ufr_disc = ufr_discount_factor(ufr=ufr, t=t_target)
    W = wilson_function(t1=t_target, t2=t_obs, alpha=alpha, ufr=ufr)

    # Price vector - equivalent to discounting with zero-coupon yields 1/(1 + r)^t
    # for prices where t_obs = t_target. All other matuirites are interpolated or extrapolated
    P = ufr_disc - W @ zeta  # '@' in numpy is the dot product of two matrices

    # Transform price vector to zero-coupon rate vector (1/P)^(1/t) - 1
    return np.power(1/P, 1/t_target) - 1
