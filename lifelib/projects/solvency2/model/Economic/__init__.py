"""Source module to create ``Economic`` space from.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

References:
    Scenario

"""

from modelx.serialize.jsonvalues import *

_formula = lambda ScenID: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def DiscRate(t):
    return Scenarios[ScenID, "IntRate", t]


def InflFactor(t):
    if t == 0:
        return 1
    else:
        return InflFactor(t-1) / (1 + AsmpLookup("InflRate"))


def InvstRetRate(t):
    return DiscRate(t)


# ---------------------------------------------------------------------------
# References

ScenID = 1

AsmpLookup = ("Interface", ("..", "Input", "AsmpLookup"), "auto")

Scenarios = ("IOSpec", 1401491066160, 1401491066160)