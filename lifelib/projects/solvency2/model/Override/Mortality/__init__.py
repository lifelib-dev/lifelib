"""Override module for the mortality/longevity risk calculation

The formulas in this module overrides cells related to mortality in
:mod:`projection <solvency2.projection>` module.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = [
    "..BaseProj",
    "..PV"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def PolsDeath(t):
    """Number of policies: Death override"""

    return (PolsIF_Beg1(t) * asmp.BaseMortRate(AttAge(t)) 
            * asmp.MortFactor(t) * MortRateFactor(t))


def MortRateFactor(t):
    """Mortality rate factor applied from time ``t0`` and there after"""
    if t >= t0:        

        if AttAge(t) < asmp.LastAge():

            if Risk == 'mort':
                return 1 + Factor(Risk, Shock, Scope)
            elif Risk == 'longev':
                return 1 - Factor(Risk, Shock, Scope)
            else:
                ValueError("invalid Risk: %s" % Risk)

        else:
            return 1
    else:
        return 1


