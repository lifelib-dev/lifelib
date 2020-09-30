from modelx.serialize.jsonvalues import *

def _formula(t0):
    refs = {'pol': _space.parent.pol,
            'asmp': _space.parent.asmp,
            'scen': _space.parent.scen,
            'outer': _space.parent,
            'DiscRate': _space.parent.scen.DiscRate}

    return {'refs': refs}


_bases = [
    "..BaseProj"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def PolsIF_End(t):
    """Number of policies: End of period"""
    if t == t0:
        return outer.PolsIF_End(t)
    else:
        return PolsIF_Beg1(t-1) - PolsDeath(t-1) - PolsSurr(t-1)


