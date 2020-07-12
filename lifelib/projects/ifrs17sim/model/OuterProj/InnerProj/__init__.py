from modelx.serialize.jsonvalues import *

def _formula(t0):
    refs = {'pol': _space.parent.pol,
            'asmp': _space.parent.asmp,
            'scen': _space.parent.scen,
            'outer': _space.parent}

    return {'refs': refs}


_bases = [
    "..BaseProj"
]

_allow_none = None

_spaces = [
    "PresentValue"
]

# ---------------------------------------------------------------------------
# Cells

def PolsIF_End(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.PolsIF_End(t)
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


def IntAccumCF(t):
    """Intrest on accumulated cashflows"""
    return (AccumCF(t)
            + PremIncome(t)
            - ExpsTotal(t)) * DiscRate(t)


def SurrRateMult(t):
    """Surrender rate multiple for the inner projection (Default: 1)"""
    if t == 0:
        return outer.SurrRateMult(t)

    elif t == t0:
        return _space.parent(t-1).SurrRateMult(t-1)

    else:
        return SurrRateMult(t-1)


def DiscRate(t):
    """Discount rates for the inner projection"""
    return outer.DiscRate(t0, t)


