"""Override module for the lapse risk calculation

The formulas in this module overrides cells related to lapse in
:mod:`projection <solvency2.projection>` module.
"""


def SurrRateShock(t):
    """Surrender rate multiple for the inner projection (Default: 1)"""

    if t >= t0:
        return Factor(Risk, Shock, Scope)
    else:
        return 0


def SurrRate(t):
    """Surrender rate reflecting up/down lapse shocks"""

    limit = Factor(Risk, Shock, Scope, 'limit')

    if Shock == 'up':
        return min(asmp.SurrRate(t) * (1 + SurrRateShock(t)), limit)
    elif Shock == 'down':
        return max(asmp.SurrRate(t) * (1 - SurrRateShock(t)), 
                   asmp.SurrRate(t) - limit)
    else:
        raise ValueError


def PolsSurr(t):
    """Number of policies: Surrender override"""
    return PolsIF_Beg1(t) * SurrRate(t)


