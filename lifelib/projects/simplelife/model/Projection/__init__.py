"""Space for cashflow projection.

This Space is for projecting cashflows of individual model points.

.. rubric:: Inheritance Structure

The ``Projection`` Space inherits its contents from its
base Spaces,
:mod:`~simplelife.model.BaseProj` and :mod:`~simplelife.model.PV`.
Projection items are inherited from :mod:`~simplelife.model.BaseProj`
and the present values of the cashflow items are
inherited from :mod:`~simplelife.model.BaseProj`.

.. figure:: /images/projects/simplelife/model/Projection/diagram1.png

.. rubric:: Parameters

This Space is parametrized with ``PolicyID`` and ``ScenID``::

    >>> simplelife.Projection.parameters
    ('PolicyID', 'ScenID')

Calling this space with a pair of integers returns the ItemSpace
for the policy ID and scenario ID. ``ScenID`` has a default value of 1,
so for example ``Projection[1]`` represents the Projection Space for Policy 1.

Attributes:
    PolicyID(:obj:`int`): Policy ID
    ScenID(:obj:`int`, optional): Scenario ID, defaults to 1.

.. rubric:: Composition Structure

This Space has child Spaces,
:mod:`~simplelife.model.Projection.Policy` and :mod:`~simplelife.model.Projection.Assumptions`.
The :mod:`~simplelife.model.Projection.Policy` Space contains Cells representing policy attributes, such as
product type, issue age, sum assured, etc.
It also contains Cells for calculating policy values such as premium rates and
cash surrender value rates.
The :mod:`~simplelife.model.Projection.Assumptions` Space contains Cells to pick up assumption data for
its model point.

.. figure:: /images/projects/simplelife/model/Projection/diagram2.png



.. rubric:: References

The following attributes are referenced in this Space by its base Spaces.

Attributes:
    pol: Alias for :mod:`~simplelife.model.Projection.Policy` child Space
    asmp: Alias for :mod:`~simplelife.model.Projection.Assumptions` child Space
    scen: Alias for :mod:`~simplelife.model.Economic` Space


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
    """Rates for discount cashflows

    Refers to :func:`Economic[ScenID].DiscRate<simplelife.model.Economic.DiscRate>`
    """
    return scen[ScenID].DiscRate(t)


def InflFactor(t):
    """Inflation factors to adjust expense cashflows

    Refers to :func:`Economic[ScenID].InflFactor<simplelife.model.Economic.InflFactor>`
    """
    return scen[ScenID].InflFactor(t)


def InvstRetRate(t):
    """Rate of investment return

    Refers to :func:`Economic[ScenID].InvstRetRate<simplelife.model.Economic.InvstRetRate>`
    """
    return scen[ScenID].InvstRetRate(t)


# ---------------------------------------------------------------------------
# References

pol = ("Interface", (".", "Policy"), "auto")

asmp = ("Interface", (".", "Assumptions"), "auto")

scen = ("Interface", ("..", "Economic"), "auto")