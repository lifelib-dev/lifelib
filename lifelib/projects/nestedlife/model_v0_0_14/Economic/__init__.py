"""Source module to create ``Economic`` space from.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

References:
    Scenario

"""

from modelx.serialize.jsonvalues import *

def _formula(ScenID):
    refs = {'Scenario': Input.Scenarios[ScenID]}
    return {'refs': refs}


_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def DiscRate(t):
    return Scenario.IntRate(t)


def InflFactor(t):
    if t == 0:
        return 1
    else:
        return InflFactor(t-1) / (1 + asmp.InflRate)


def InvstRetRate(t):
    return Scenario.IntRate(t)


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("..", "Input"))

asmp = ("Interface", ("..", "Assumption"))