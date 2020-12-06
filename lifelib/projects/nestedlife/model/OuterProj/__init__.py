from modelx.serialize.jsonvalues import *

_formula = lambda PolicyID, ScenID=1: None

_bases = [
    ".BaseProj",
    ".PV"
]

_allow_none = None

_spaces = [
    "InnerProj",
    "Policy",
    "Assumptions"
]

# ---------------------------------------------------------------------------
# References

pol = ("Interface", (".", "Policy"), "auto")