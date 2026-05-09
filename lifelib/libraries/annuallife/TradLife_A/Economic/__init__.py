# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

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

``Economic`` Space is parameterized with :attr:`scen_id`::

        >>> simplelife.Economic.parameters
        ('ScenID',)

Each ItemSpace represents economic scenarios for a specific :attr:`scen_id`.
For example, ``Economic[1]`` contains economic scenarios for scen_id 1.

Attributes:
    scen_id(:obj:`int`): Scenario ID

.. rubric:: References

Attributes:
    Scenario: `ExcelRange`_ object holding the data of interest rate
        assumptions. The data is read from *Scenarios* range in *input.xlsx*.

Example:

    An example of ``Economic`` in the :mod:`simplelife` model::

        >>> simplelife.Economic[1].disc_rate_mth(0)
        0.015

"""

from modelx.serialize.jsonvalues import *

_formula = lambda scen_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def disc_rate_mth(t):
    """Rates for discount cashflows"""
    return input_data.scenarios()['IntRate'].at[(scen_id, t)]


def invst_ret_rate(t):
    """Rate of investment return

    Set equal to the :func:`disc_rate_mth`
    """
    return disc_rate_mth(t)


# ---------------------------------------------------------------------------
# References

scen_id = 1

input_data = ("Interface", ("..", "InputData"), "auto")