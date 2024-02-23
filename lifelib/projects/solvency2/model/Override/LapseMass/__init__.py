"""Override module for the mass lapse risk calculation

The formulas in this module overrides cells related to lapse in
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

def BenefitSurr(t):
    """Surrender benefits"""
    return SizeBenefitSurr(t) * (PolsSurr(t) + PolsSurrMass(t))


def PolsIF_Beg1(t):
    """Number of policies: Beginning of period 1"""
    return PolsIF_Beg(t) + PolsRenewal(t) + PolsNewBiz(t) - PolsSurrMass(t)


def PolsSurrMass(t):
    """Number of policies: Surrender"""
    factor = Factor(Risk, Shock, Scope) if t == t0 else 0

    return (PolsIF_Beg(t) + PolsRenewal(t) + PolsNewBiz(t)) * factor


