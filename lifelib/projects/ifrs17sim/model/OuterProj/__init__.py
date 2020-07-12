from modelx.serialize.jsonvalues import *

def _formula(PolicyID, ScenID=1):
    refs = {'pol': Pol[PolicyID],
            'asmp': Asmp[PolicyID],
            'scen': Scen[ScenID]}

    return {'refs': refs}


_bases = [
    ".IFRS",
    ".BaseProj"
]

_allow_none = None

_spaces = [
    "InnerProj"
]

# ---------------------------------------------------------------------------
# Cells

def IntAccumCF(t):
    """Intrest on accumulated cashflows"""
    return (AccumCF(t)
            + PremIncome(t)
            - ExpsTotal(t)) * DiscRate(t, 0)


def DiscRate(t, dur):
    """Discount rates for the outer projection"""
    return scen.DiscRate(dur) + DiscRateAdj(t)


def DiscRateAdj(t):
    """Adjustment to the outer discount rates"""
    if t == 0:
        return 0
    else:
        return DiscRateAdj(t-1)


# ---------------------------------------------------------------------------
# References

Asmp = ("Interface", ("..", "Assumption"))

Pol = ("Interface", ("..", "Policy"))

Scen = ("Interface", ("..", "Economic"))