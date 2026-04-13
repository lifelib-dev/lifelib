"""Economic scenarios

The ``Economic`` spaces provides economic assumptions such as
interest rate scenarios.

This Space is included in:

* :mod:`simplelife`
* :mod:`nestedlife`
* :mod:`ifrs17sim`
* :mod:`solvency2`


.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

.. rubric:: Parameters

``Economic`` Space is parameterized with :attr:`ScenID`::

        >>> simplelife.Economic.parameters
        ('ScenID',)

Each ItemSpace represents economic scenarios for a specific :attr:`ScenID`.
For example, ``Economic[1]`` contains economic scenarios for ScenID 1.

Attributes:
    ScenID(:obj:`int`): Scenario ID

.. rubric:: References

Attributes:
    Scenario: `ExcelRange`_ object holding the data of interest rate
        assumptions. The data is read from *Scenarios* range in *input.xlsx*.

Example:

    An example of ``Economic`` in the :mod:`simplelife` model::

        >>> simplelife.Economic[1].DiscRate(0)
        0.015

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

Scenarios = ("IOSpec", 2333220036880, 2333220036880)