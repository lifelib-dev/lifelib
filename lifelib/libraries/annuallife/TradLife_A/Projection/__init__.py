# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Space for cashflow projection.

This Space is for projecting cashflows of individual model points.

.. rubric:: Inheritance Structure

The ``Projection`` Space inherits its contents from its base Spaces,
:mod:`~annuallife.TradLife_A.BaseProj` and
:mod:`~annuallife.TradLife_A.PV`.
The projection cells are inherited from
:mod:`~annuallife.TradLife_A.BaseProj`, and the present values of those
cashflow items are inherited from :mod:`~annuallife.TradLife_A.PV`.

.. rubric:: Parameters

This Space is parameterized with ``idx`` and ``scen_id``::

    >>> m.Projection.parameters
    ('idx', 'scen_id')

Calling this Space with a pair of integers returns the ItemSpace for
the policy index and scenario ID. ``scen_id`` has a default value of 1,
so for example ``Projection[0]`` represents the Projection Space for
the first policy under scenario 1.

Attributes:
    idx(:obj:`int`): 0-based policy index into the policy data array.
    scen_id(:obj:`int`, optional): Scenario ID, defaults to 1.

.. rubric:: References

The following references are resolved in this Space and its base
Spaces:

Attributes:
    pol: Alias for :mod:`~annuallife.TradLife_A.PolicyAttrs`.
    asmp: Alias for :mod:`~annuallife.TradLife_A.Assumptions`.
    scen: Alias for :mod:`~annuallife.TradLife_A.Economic`.
    comm_table: Alias for :mod:`~annuallife.TradLife_A.CommTable`.

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