# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Annual projection model for traditional life insurance policies.

:mod:`~annuallife.TradLife_A` is the modern successor of the
:mod:`simplelife` model. It projects insurance cashflows and their
present values for traditional life policies on an annual time step,
re-expressed in snake-case naming and refactored for an array-based
input.

A projection is performed by selecting a model point through the integer
parameter ``idx``, the 0-based index into the policy data array read
from *input.xlsx*. For example, the present value of net cashflows for
the first policy is obtained as::

    >>> m.Projection[0].pv_net_cf(0)


.. rubric:: Spaces

The model is composed of the following spaces:

* :mod:`~annuallife.TradLife_A.InputData`: References to Excel ranges
  read from *input.xlsx* and helper cells for converting them to pandas
  objects.
* :mod:`~annuallife.TradLife_A.Economic`: Parametric space holding
  scenario-dependent economic assumptions (parameter ``scen_id``).
* :mod:`~annuallife.TradLife_A.BaseProj`: Base space of
  :mod:`~annuallife.TradLife_A.Projection` containing per-period
  cashflow projection cells.
* :mod:`~annuallife.TradLife_A.PV`: Mix-in base space of
  :mod:`~annuallife.TradLife_A.Projection` containing the present-value
  cells.
* :mod:`~annuallife.TradLife_A.Projection`: Parametric space whose
  ItemSpaces carry out projections for each model point (parameters
  ``idx`` and ``scen_id``).
* :mod:`~annuallife.TradLife_A.Assumptions`: Assumption parameters and
  rates used by :mod:`~annuallife.TradLife_A.Projection`.
* :mod:`~annuallife.TradLife_A.PolicyAttrs`: Policy attributes and
  policy-level values such as premium and surrender rates.
* :mod:`~annuallife.TradLife_A.Utilities`: Base space of
  :mod:`~annuallife.TradLife_A.Assumptions` and
  :mod:`~annuallife.TradLife_A.PolicyAttrs` providing helper cells.
* :mod:`~annuallife.TradLife_A.CommTable`: Parametric space providing
  commutation functions and actuarial notations (parameters ``Sex``,
  ``IntRate`` and ``Table``).
* :mod:`~annuallife.TradLife_A.Enums`: Container for enum types
  (``ProductID``, ``SexID``, ``RateBasisID``) used across the model.

.. rubric:: References

Attributes:
    pd: The :mod:`pandas` module.
    np: The :mod:`numpy` module.
    ProductID: Alias for :mod:`~annuallife.TradLife_A.Enums.ProductID`.
    SexID: Alias for :mod:`~annuallife.TradLife_A.Enums.SexID`.
    RateBasisID: Alias for :mod:`~annuallife.TradLife_A.Enums.RateBasisID`.

"""

from modelx.serialize.jsonvalues import *

_name = "TradLife_A"

_allow_none = False

_spaces = [
    "InputData",
    "Economic",
    "BaseProj",
    "PV",
    "Projection",
    "Assumptions",
    "PolicyAttrs",
    "Utilities",
    "CommTable",
    "Enums"
]

# ---------------------------------------------------------------------------
# References

pd = ("Module", "pandas")

np = ("Module", "numpy")

ProductID = ("Interface", (".", "Enums", "ProductID"), "None")

SexID = ("Interface", (".", "Enums", "SexID"), "None")

RateBasisID = ("Interface", (".", "Enums", "RateBasisID"), "None")