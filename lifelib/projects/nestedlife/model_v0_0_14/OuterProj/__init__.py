from modelx.serialize.jsonvalues import *

def _formula(PolicyID, ScenID=1):
    refs = {'pol': Pol[PolicyID],
            'asmp': Asmp[PolicyID],
            'scen': Scen[ScenID]}
    return {'refs': refs}


_bases = [
    ".BaseProj"
]

_allow_none = None

_spaces = [
    "InnerProj"
]

# ---------------------------------------------------------------------------
# References

Asmp = ("Interface", ("..", "Assumption"))

Pol = ("Interface", ("..", "Policy"))

Scen = ("Interface", ("..", "Economic"))