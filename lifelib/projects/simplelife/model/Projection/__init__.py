"""Space for cashflow projection.

This Space serves as a base Space for :mod:`~simplelife.model.Projection`
Space, and it contains Cells for cashflow projection.

.. rubric:: Projects

This module is included in the following projects.

* :mod:`simplelife`
* :mod:`nestedlife`
* :mod:`ifrs17sim`
* :mod:`solvency2`

.. rubric:: References

The following attributes are referenced in this Space by its base Spaces.

Attributes:
    pol: Alias for :mod:`~simplelife.model.Projection.Policy` child Space
    asmp: Alias for :mod:`~simplelife.model.Projection.Assumptions` child Space
    scen: :mod:`~simplelife.model.Economic` Space

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- OuterProj [hstyle=generalization]
     PresentValue[style=dotted]
     PresentValue <- OuterProj [hstyle=generalization];
   }

"""

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

pol = ("Interface", (".", "Policy"), "auto")

asmp = ("Interface", (".", "Assumptions"), "auto")

scen = ("Interface", ("..", "Economic"), "auto")