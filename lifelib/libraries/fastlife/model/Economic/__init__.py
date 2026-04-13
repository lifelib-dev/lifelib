"""Economic Assumptions

This Space includes economic assumptions, such as discount rates
and inflation rates. This Space is parametrized with :attr:`ScenID`.

.. rubric:: Space Parameters

Attributes:
    ScenID(:obj:`int`): Scenario ID

.. rubric:: References

Attributes:
    AsmpLookup: Reference to :func:`fastlife.model.Projection.Assumptions.AsmpLookup`
    Scenarios: `ExcelRange`_ object holding scenario data read from
        the input file.

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

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

Scenarios = ("Pickle", 3020541690632)

AsmpLookup = ("Interface", ("..", "Projection", "Assumptions", "AsmpLookup"), "auto")