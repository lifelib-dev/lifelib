# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Scenario economic rates for a single traditional life projection.

The ``Economic`` Space provides the per-scenario interest rates used
to discount cashflows and to credit investment return, read from
*input.xlsx*.

Parameters and References
-------------------------

``Economic`` is parameterized with :attr:`scen_id`::

        >>> m.Economic.parameters
        ('scen_id',)

Each ItemSpace represents economic scenarios for a specific
:attr:`scen_id`. For example, ``Economic[1]`` contains economic
scenarios for ``scen_id`` 1.

Attributes:
    scen_id(:obj:`int`): Scenario ID.

.. rubric:: References

Attributes:
    input_data: Alias for :mod:`~annuallife.TradLife_A.InputData`.
        Scenario interest rates are read from the ``Scenarios`` range
        in *input.xlsx* through
        :func:`~annuallife.TradLife_A.InputData.scenarios`.

Example:

    An example of ``Economic`` in :mod:`~annuallife.TradLife_A`::

        >>> m.Economic[1].disc_rate(0)
        0.015


Cells Summary
-------------

The discount rate and the investment return rate for the selected
scenario at time ``t``.

.. autosummary::

   ~disc_rate
   ~invst_ret_rate

"""

from modelx.serialize.jsonvalues import *

_formula = lambda scen_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def disc_rate(t):
    """Discount rate at time ``t``.

    Read from the ``Scenarios`` range in *input.xlsx* (column
    ``IntRate``) through
    :func:`~annuallife.TradLife_A.InputData.scenarios`,
    keyed by the current :attr:`scen_id` and ``t``.
    """
    return input_data.scenarios()['IntRate'].at[(scen_id, t)]


def invst_ret_rate(t):
    """Rate of investment return at time ``t``.

    Set equal to :func:`disc_rate`.
    """
    return disc_rate(t)


# ---------------------------------------------------------------------------
# References

scen_id = 1

input_data = ("Interface", ("..", "InputData"), "auto")