from modelx.serialize.jsonvalues import *

def _formula(Risk='base', Shock=None, Scope=None):


    if Risk == 'mort' or Risk == 'longev':
        base = _model.Override.Mortality
    elif Risk == 'lapse':
        if Shock == 'mass':
            base = _model.Override.LapseMass
        else:
            base = _model.Override.Lapse
    elif Risk == 'exps':
            base = _model.Override.Expense
    else:
        base = _space

    refs = {'pol': Policy[PolicyID],
            'asmp': Assumptions[PolicyID],
            'scen': Economic[ScenID],
            'DiscRate': Economic[ScenID].DiscRate,
            'Factor': _model.Input.Factor}

    return {'base': base, 'refs': refs}


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