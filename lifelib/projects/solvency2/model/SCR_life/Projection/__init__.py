from modelx.serialize.jsonvalues import *

def _formula(Risk='base', Shock=None, Scope=None):


    if Risk == 'mort' or Risk == 'longev':
        bases = [_space.model.Override.Mortality, _space]  

    elif Risk == 'lapse':
        if Shock == 'mass':
            bases = [_space.model.Override.LapseMass, _space]
        else:
            bases = [_space.model.Override.Lapse, _space]
    elif Risk == 'exps':
            bases = [_space.model.Override.Expense, _space]   
    else:
        bases = [_space]

    refs = {'pol': Policy[PolicyID],
            'asmp': Assumptions[PolicyID],
            'scen': Economic[ScenID],
            'DiscRate': Economic[ScenID].DiscRate,
            'Factor': _space.model.Input.Factor}

    return {'bases':bases, 'refs': refs}


_bases = [
    "..BaseProj",
    "..PV"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

Economic = ("Interface", ("...", "Economic"), "auto")

Policy = ("Interface", ("...", "Policy"), "auto")

Assumptions = ("Interface", ("...", "Assumptions"), "auto")