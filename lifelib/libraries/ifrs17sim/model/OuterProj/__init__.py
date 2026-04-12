from modelx.serialize.jsonvalues import *

_formula = lambda PolicyID, ScenID=1: None

_bases = [
    ".IFRS",
    ".BaseProj"
]

_allow_none = None

_spaces = [
    "InnerProj",
    "Policy",
    "Assumptions"
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

pol = ("Interface", (".", "Policy"), "auto")