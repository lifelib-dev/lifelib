"""Override module for the expense risk calculation

The formulas in this module add or overrides cells related to expense in
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

def SizeExpsAcq(t):
    """Acquisition expense per policy at time t"""
    if t == 0:
        return (SizeAnnPrem(t) * asmp.ExpsAcqAnnPrem()
                + (SizeSumAssured(t) * asmp.ExpsAcqSA() + asmp.ExpsAcqPol())
                * InflFactor(t) / InflFactor(0))
    else:
        return 0


def SizeExpsMaint(t):
    """Maintenance expense per policy at time t"""

    shock = Factor(Risk, Shock, Scope)

    return (SizeAnnPrem(t) * asmp.ExpsMaintAnnPrem()
            + (SizeSumAssured(t) * asmp.ExpsMaintSA() + asmp.ExpsMaintPol())
            * InflFactor(t)) * (1 + shock)


def InflFactor(t):
    """Inflation factor reflecting expense shocks"""
    if t == 0:
        return 1
    else:        
        if t >= t0:
            shock = Factor(Risk, Shock, Scope, 'inflation')
        else:
            shock = 0

        return InflFactor(t-1) * (1 + asmp.InflRate() + shock)


