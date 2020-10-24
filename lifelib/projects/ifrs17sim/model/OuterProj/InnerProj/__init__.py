from modelx.serialize.jsonvalues import *

def _formula(t0):
    refs = {'outer': _space.parent,
            'pol': _space.parent.Policy}
    return {'refs': refs}


_bases = [
    "..BaseProj"
]

_allow_none = None

_spaces = [
    "Assumptions",
    "PV"
]

# ---------------------------------------------------------------------------
# Cells

def PolsIF_End(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.PolsIF_End(t)
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


Product = lambda: _space.parent.parent.Policy.Product()

PolicyType = lambda: _space.parent.parent.Policy.PolicyType()

Gen = lambda: _space.parent.parent.Policy.Gen()

Sex = lambda: _space.parent.parent.Policy.Sex()

def DiscRate(t):
    """Discount rates for the inner projection"""
    return outer.DiscRate(t0, t)


