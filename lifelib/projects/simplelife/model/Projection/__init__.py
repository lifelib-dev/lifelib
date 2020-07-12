from modelx.serialize.jsonvalues import *

def _formula(PolicyID, ScenID=1):
    refs = {'pol': Policy[PolicyID],
            'asmp': Assumption[PolicyID],
            'scen': Economic[ScenID],
            'DiscRate': Economic[ScenID].DiscRate}
    return {'refs': refs}


_bases = [
    ".BaseProj",
    ".PV"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

Assumption = ("Interface", ("..", "Assumption"))

Economic = ("Interface", ("..", "Economic"))

Policy = ("Interface", ("..", "Policy"))