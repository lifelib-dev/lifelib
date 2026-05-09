# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

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

This Space is parametrized with ``idx`` and ``scen_id``::

    >>> simplelife.Projection.parameters
    ('PolicyID', 'ScenID')

Calling this space with a pair of integers returns the ItemSpace
for the policy ID and scenario ID. ``scen_id`` has a default value of 1,
so for example ``Projection[1]`` represents the Projection Space for Policy 1.

Attributes:
    idx(:obj:`int`): Policy ID
    scen_id(:obj:`int`, optional): Scenario ID, defaults to 1.

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

_formula = lambda idx, scen_id=1: None

_bases = [
    ".BaseProj",
    ".PV"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

scen = ("Interface", ("..", "Economic"), "auto")

asmp = ("Interface", ("..", "Assumptions"), "auto")

pol = ("Interface", ("..", "PolicyAttrs"), "auto")

comm_table = ("Interface", ("..", "CommTable"), "auto")