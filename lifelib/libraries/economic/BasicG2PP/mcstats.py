"""Monte Carlo summary statistics for the Validation space of BasicG2PP.

:func:`check` turns simulated samples into a DataFrame of Monte Carlo estimates,
theoretical values, standard errors and z-scores. With antithetic variates, scenarios
k and k + N/2 form a pair, and the standard error comes from the N/2 pair means, which
are independent. Treating the N paths as independent would overstate it.
"""
import numpy as np
import pandas as pd


def mean_se(samples, antithetic):
    """Mean and standard error of samples over their first axis (scenarios)."""
    samples = np.asarray(samples, dtype=float)
    if antithetic:
        half = len(samples) // 2
        samples = 0.5 * (samples[:half] + samples[half:])
    return samples.mean(axis=0), samples.std(axis=0, ddof=1) / np.sqrt(len(samples))


def check(samples, theory, antithetic, index=None):
    """DataFrame with columns mc, theory, se and z of samples against theory.

    ``samples`` has one row per stochastic scenario, with shape (N,) or (N, k), and
    ``theory`` is a scalar or has shape (k,). z = (mc - theory) / se. Where se is below
    1e-12 of the value, the estimate is exact by construction (for example the mean of
    x with antithetic variates, or the deflated value of an all-cash fund): z is then 0
    if mc matches theory to 1e-9, and infinite otherwise.
    """
    mc, se = mean_se(samples, antithetic)
    mc, se = np.atleast_1d(mc), np.atleast_1d(se)
    theory = np.array(np.broadcast_to(np.asarray(theory, dtype=float), mc.shape))
    tol = 1e-12 * np.maximum(1.0, np.abs(theory))
    diff = mc - theory
    z = np.where(np.abs(diff) <= 1e3 * tol, 0.0, np.copysign(np.inf, diff))
    np.divide(diff, se, out=z, where=se > tol)
    return pd.DataFrame({"mc": mc, "theory": theory, "se": se, "z": z}, index=index)
