from modelx.serialize.jsonvalues import *

_formula = lambda PolicyID, ScenID=1: None

_bases = [
    ".BaseProj",
    ".PV"
]

_allow_none = None

_spaces = [
    "Policy",
    "Assumptions"
]

# ---------------------------------------------------------------------------
# Cells

def DiscRate(t):
    return scen[ScenID].DiscRate(t)


def InflFactor(t):
    return scen[ScenID].InflFactor(t)


def InvstRetRate(t):
    return scen[ScenID].InvstRetRate(t)


# ---------------------------------------------------------------------------
# References

Economic = ("Interface", ("..", "Economic"))

pol = ("Interface", (".", "Policy"))

asmp = ("Interface", (".", "Assumptions"))

scen = ("Interface", ("..", "Economic"))