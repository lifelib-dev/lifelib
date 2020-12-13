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
    """Rates for discount cashflows"""
    return Scenarios[ScenID, "IntRate", t]


def InflFactor(t):
    """Inflation factors to adjust expense cashflows"""
    if t == 0:
        return 1
    else:
        return InflFactor(t-1) / (1 + AsmpLookup("InflRate"))


def InvstRetRate(t):
    """Rate of investment return

    Set equal to the :func:`DiscRate`
    """
    return DiscRate(t)


# ---------------------------------------------------------------------------
# References

ScenID = 1

AsmpLookup = ("Interface", ("..", "Input", "AsmpLookup"), "auto")

Scenarios = ("Pickle", 2233390044744)