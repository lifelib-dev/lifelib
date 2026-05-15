# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Annual projection model for traditional life insurance policies.

Overview
--------

:mod:`~annuallife.TradLife_A` is an annual projection model for basic
traditional life policies. It is the modern successor of the
:ref:`project_simplelife` model and shares the same calculation logic,
re-expressed in snake-case naming and refactored for an array-based
input.

A projection is performed by selecting a model point through the integer
parameter ``idx``, which is the 0-based index into the policy data array
read from *input.xlsx*. For example, the present value of net cashflows
for the first policy is obtained as::

    >>> m.Projection[0].pv_net_cf(0)

For the same model, ``m.Projection[idx].pv_net_cf(0)`` matches the legacy
``simplelife.Projection[idx + 1].PV_NetCashflow(0)``.

Model Structure
---------------

In :mod:`~annuallife.TradLife_A`, the following spaces are defined.

* :mod:`~annuallife.TradLife_A.InputData`: Holds References to the
  Excel ranges read from *input.xlsx* and helper cells for converting
  them to pandas objects.
* :mod:`~annuallife.TradLife_A.Economic`: Parametric space holding
  scenario-dependent economic assumptions; parameter ``scen_id``.
* :mod:`~annuallife.TradLife_A.BaseProj`: Base space of
  :mod:`~annuallife.TradLife_A.Projection` containing the cells that
  produce the per-period cashflow projections.
* :mod:`~annuallife.TradLife_A.PV`: Mixin base space of
  :mod:`~annuallife.TradLife_A.Projection` containing the cells that
  compute the present values of those cashflows.
* :mod:`~annuallife.TradLife_A.Projection`: Parametric space whose
  dynamic ItemSpaces carry out projections for each model point;
  parameters ``idx`` and ``scen_id``.
* :mod:`~annuallife.TradLife_A.Assumptions`: Holds assumption parameters
  and rates used by :mod:`~annuallife.TradLife_A.Projection`.
* :mod:`~annuallife.TradLife_A.PolicyAttrs`: Holds policy attributes and
  policy-level values such as premium and surrender rates used by
  :mod:`~annuallife.TradLife_A.Projection`.
* :mod:`~annuallife.TradLife_A.Utilities`: Base space of
  :mod:`~annuallife.TradLife_A.Assumptions` and
  :mod:`~annuallife.TradLife_A.PolicyAttrs` providing helper cells.
* :mod:`~annuallife.TradLife_A.CommTable`: Parametric space providing
  commutation functions and actuarial notations; parameters ``Sex``,
  ``IntRate`` and ``Table``.
* :mod:`~annuallife.TradLife_A.Enums`: Container for enum types
  (``ProductID``, ``SexID``, ``RateBasisID``) used across the model.

Inheritance
^^^^^^^^^^^

:mod:`~annuallife.TradLife_A.Projection` inherits from
:mod:`~annuallife.TradLife_A.BaseProj` and
:mod:`~annuallife.TradLife_A.PV`, so projection cells and their
present-value counterparts share the same parameter scope.
:mod:`~annuallife.TradLife_A.Assumptions` and
:mod:`~annuallife.TradLife_A.PolicyAttrs` inherit from
:mod:`~annuallife.TradLife_A.Utilities`, which contributes the
``pandas_to_array`` and ``map_to_policies`` helpers.

Cross-space references
^^^^^^^^^^^^^^^^^^^^^^

The cells in :mod:`~annuallife.TradLife_A.Projection` and its base
spaces resolve a number of References to other spaces:

* ``pol`` -> :mod:`~annuallife.TradLife_A.PolicyAttrs`
* ``asmp`` -> :mod:`~annuallife.TradLife_A.Assumptions`
* ``scen`` -> :mod:`~annuallife.TradLife_A.Economic`
* ``comm_table`` -> :mod:`~annuallife.TradLife_A.CommTable`

In :mod:`~annuallife.TradLife_A.Assumptions` and
:mod:`~annuallife.TradLife_A.PolicyAttrs`, the data space is referenced
as ``input_data`` (renamed from the legacy ``Input``) and points at
:mod:`~annuallife.TradLife_A.InputData`.

Input File
----------

:mod:`~annuallife.TradLife_A` reads its data from *input.xlsx*, which is
located next to the *TradLife_A* model directory inside the library
folder. The default file name is set by the
:attr:`~annuallife.TradLife_A.InputData.input_file_name` reference.

The workbook defines the following named ranges, picked up through cells
in :mod:`~annuallife.TradLife_A.InputData`:

.. table::
   :widths: 30 30 40

   ============================================================== ====================== =========================================
   Cell                                                           Excel named range      Purpose
   ============================================================== ====================== =========================================
   :func:`~annuallife.TradLife_A.InputData.policy_data`            ``PolicyData``         Per-policy attributes for model points
   :func:`~annuallife.TradLife_A.InputData.product_spec`           ``ProductSpecTable``   Per-product loading and rate tables
   :func:`~annuallife.TradLife_A.InputData.assumption`             ``AssumptionTable``    Lookup table of assumption keys
   :func:`~annuallife.TradLife_A.InputData.assumption_tables`      ``AsmpByDuration``     Duration-based mortality / lapse tables
   :func:`~annuallife.TradLife_A.InputData.mortality_tables`       ``MortalityTables``    Mortality tables keyed by Sex / Table
   :func:`~annuallife.TradLife_A.InputData.scenarios`              ``Scenarios``          Scenario interest-rate paths
   :func:`~annuallife.TradLife_A.InputData.discount_rate`          ``LargePolDiscount``   Premium discount by sum-assured band
   :func:`~annuallife.TradLife_A.InputData.prem_waiver_cost`       ``PremiumWaiverCost``  Premium-waiver cost lookup
   :func:`~annuallife.TradLife_A.InputData.const_params`           ``ConstParams``        Scalar parameters used across the model
   ============================================================== ====================== =========================================

Basic Usage
-----------

Reading the model
^^^^^^^^^^^^^^^^^

Create your copy of the *annuallife* library by following the steps on
the :doc:`/quickstart/index` page. The model is saved as the folder
``TradLife_A`` in the copied folder, with *input.xlsx* placed next to
it.

To read the model from Spyder with the modelx plug-in, right-click on
the empty space in *MxExplorer*, select *Read Model*, and choose the
*TradLife_A* folder.

To read the model on an IPython console, use ``read_model`` after
changing the current directory to the library folder so the workbook is
discoverable:

.. code-block:: python

    >>> import modelx as mx

    >>> m = mx.read_model("TradLife_A")

Running results
^^^^^^^^^^^^^^^

Projection results are obtained by calling the cells of an ItemSpace of
:mod:`~annuallife.TradLife_A.Projection` with a specific ``idx`` (and
optionally ``scen_id``):

.. code-block:: python

    >>> m.Projection[0].pv_net_cf(0)            # PV of net cashflow at t=0
    >>> m.Projection[0].net_cf(5)               # Net cashflow at t=5
    >>> m.Projection[0].premiums(0)             # Premium income at t=0
    >>> m.Projection[0].claims(0)               # Death claims at t=0

The plot scripts ``plot_tradlife_a.py`` and ``plot_pvcashflows_tradlife_a.py``
in the library folder demonstrate how to produce stacked-bar charts of
the cashflow components and their present values.

Global References
-----------------

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