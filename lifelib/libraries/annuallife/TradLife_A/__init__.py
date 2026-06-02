# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Annual new business projection model of basic traditional life policies.

Overview
--------

:mod:`~annuallife.TradLife_A` is an annual new business projection model
of basic traditional life policies, covering term, whole life and
endowment products, built with
`modelx <https://modelx.io/>`__.

It projects liability cashflows and their present values for policies
represented by model points. Projected items include:

* Premiums,
* Commissions and expenses,
* Claims.

Premiums are calculated using commutation functions. Cells for investment
income reserves are defined but not implemented.

Computation flow
^^^^^^^^^^^^^^^^

Model point data, product specifications, assumptions and economic
scenarios are all held in an external Excel workbook, *input.xlsx*.

The spaces are wired together as shown below, and the computation
proceeds as follows.

.. mermaid::

    graph LR
        Projection --> PolicyAttrs
        Projection --> Assumptions
        Projection --> CommTable
        Projection --> Economic
        PolicyAttrs --> InputData
        Assumptions --> InputData
        CommTable --> InputData
        Economic --> InputData

* The data is read into the model from the input file in
  :mod:`~annuallife.TradLife_A.InputData`, and held there as
  :mod:`pandas` DataFrames and dicts.
* :mod:`~annuallife.TradLife_A.InputData` is referenced by
  :mod:`~annuallife.TradLife_A.PolicyAttrs` and
  :mod:`~annuallife.TradLife_A.Assumptions`, where policy attributes and
  assumptions are mapped to model points.
* :mod:`~annuallife.TradLife_A.InputData` is also referenced by
  :mod:`~annuallife.TradLife_A.Economic`, where discount rates are
  calculated.
* :mod:`~annuallife.TradLife_A.CommTable` calculates commutation
  functions, and defines actuarial notations. They are used by
  :mod:`~annuallife.TradLife_A.Projection` to calculate the premium rate
  for each model point. Mortality rates are provided through
  :mod:`~annuallife.TradLife_A.InputData`.
  :mod:`~annuallife.TradLife_A.CommTable` takes three parameters,
  ``Sex``, ``IntRate`` and ``Table`` (sex, interest rate and mortality
  table id).
* :mod:`~annuallife.TradLife_A.Projection` carries out the projection by
  model point. It takes two parameters: ``idx`` (mandatory) to identify
  a model point, and ``scen_id`` (optional) to select the economic
  scenario, defaulting to 1. Policy attributes and assumptions are
  received from cells in
  :mod:`~annuallife.TradLife_A.PolicyAttrs` and
  :mod:`~annuallife.TradLife_A.Assumptions`, which return their values by
  model point in 1-D :mod:`numpy` arrays, so the ``idx`` parameter
  indicates the array index, starting from 0.
* The projection logic is not defined directly in
  :mod:`~annuallife.TradLife_A.Projection`. Instead, the space inherits
  all of its logic from two base spaces,
  :mod:`~annuallife.TradLife_A.BaseProj` and
  :mod:`~annuallife.TradLife_A.PV`.

For example, the present value of net cashflows for the first model
point is obtained as::

    >>> m.Projection[0].pv_net_cf(0)

Model Structure
---------------

In :mod:`~annuallife.TradLife_A`, the following spaces are defined.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Space
     - Description
   * - :mod:`~annuallife.TradLife_A.InputData`
     - Reads *input.xlsx* and holds its named ranges as :mod:`pandas`
       DataFrames and dicts.
   * - :mod:`~annuallife.TradLife_A.Economic`
     - Parametric space holding scenario-dependent economic assumptions;
       parameter ``scen_id``.
   * - :mod:`~annuallife.TradLife_A.BaseProj`
     - Base space of :mod:`~annuallife.TradLife_A.Projection` containing
       the cells that produce the per-period cashflow projections.
   * - :mod:`~annuallife.TradLife_A.PV`
     - Base space of :mod:`~annuallife.TradLife_A.Projection` containing
       the cells that compute the present values of those cashflows.
   * - :mod:`~annuallife.TradLife_A.Projection`
     - Parametric space whose dynamic ItemSpaces carry out projections
       for each model point; parameters ``idx`` and ``scen_id``.
   * - :mod:`~annuallife.TradLife_A.Assumptions`
     - Holds assumption parameters and rates used by
       :mod:`~annuallife.TradLife_A.Projection`.
   * - :mod:`~annuallife.TradLife_A.PolicyAttrs`
     - Holds policy attributes and policy-level values such as premium
       and surrender rates used by
       :mod:`~annuallife.TradLife_A.Projection`.
   * - :mod:`~annuallife.TradLife_A.Utilities`
     - Base space of :mod:`~annuallife.TradLife_A.Assumptions` and
       :mod:`~annuallife.TradLife_A.PolicyAttrs` providing helper cells.
   * - :mod:`~annuallife.TradLife_A.CommTable`
     - Parametric space providing commutation functions and actuarial
       notations; parameters ``Sex``, ``IntRate`` and ``Table``.
   * - :mod:`~annuallife.TradLife_A.Enums`
     - Container for the enum types used across the model.

:mod:`~annuallife.TradLife_A.Enums` contains the enum types as child
spaces, and :mod:`~annuallife.TradLife_A.Assumptions` contains an
``AsmpID`` child space.

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

.. mermaid::

    %%{init: {"class": {"hideEmptyMembersBox": true}}}%%
    classDiagram
        BaseProj <|-- Projection
        PV <|-- Projection
        Utilities <|-- Assumptions
        Utilities <|-- PolicyAttrs

Cross-space references
^^^^^^^^^^^^^^^^^^^^^^

The cells in :mod:`~annuallife.TradLife_A.Projection` and its base
spaces resolve a number of References to other spaces:

* ``scen`` -> :mod:`~annuallife.TradLife_A.Economic`
* ``asmp`` -> :mod:`~annuallife.TradLife_A.Assumptions`
* ``pol`` -> :mod:`~annuallife.TradLife_A.PolicyAttrs`
* ``comm_table`` -> :mod:`~annuallife.TradLife_A.CommTable`

:mod:`~annuallife.TradLife_A.Economic`,
:mod:`~annuallife.TradLife_A.Assumptions` and
:mod:`~annuallife.TradLife_A.PolicyAttrs` each reference the
:mod:`~annuallife.TradLife_A.InputData` space as ``input_data``, while
:mod:`~annuallife.TradLife_A.CommTable` references the
:func:`~annuallife.TradLife_A.InputData.mortality_tables` cells defined
in :mod:`~annuallife.TradLife_A.InputData` as ``mortality_tables``.

.. mermaid::

    graph LR
        Projection -- scen --> Economic
        Projection -- asmp --> Assumptions
        Projection -- pol --> PolicyAttrs
        Projection -- comm_table --> CommTable
        Economic -- input_data --> InputData
        Assumptions -- input_data --> InputData
        PolicyAttrs -- input_data --> InputData
        CommTable -- mortality_tables --> InputData

Input File
----------

:mod:`~annuallife.TradLife_A` reads its data from *input.xlsx*, which is
located next to the *TradLife_A* model directory inside the library
folder. The default file name is set by the
:attr:`~annuallife.TradLife_A.InputData.input_file_name` reference.

The workbook defines the named ranges described below. Each one is read
through a Cells in :mod:`~annuallife.TradLife_A.InputData`.

.. seealso::

   :mod:`~annuallife.TradLife_A.InputData` for the Cells that load these
   named ranges and the helpers that turn them into :mod:`pandas`
   objects.

Model point data
^^^^^^^^^^^^^^^^

Named range: ``PolicyData``

Per-policy attributes for the model points the projection runs over.
One row per policy, loaded by
:func:`~annuallife.TradLife_A.InputData.policy_data` and indexed by
the ``Policy`` column.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``Policy``
     - Policy ID. Becomes the DataFrame index.
   * - ``Product``
     - Product code (``TERM``, ``WL`` or ``ENDW``); a value of the
       :mod:`~annuallife.TradLife_A.Enums.ProductID` enum.
   * - ``PolType``
     - Policy-type sub-category within the product.
   * - ``Gen``
     - Product generation / cohort identifier.
   * - ``Channel``
     - Distribution channel.
   * - ``Duration``
     - Elapsed policy duration in years at the projection start.
   * - ``Sex``
     - Insured sex (``M`` or ``F``); a value of the
       :mod:`~annuallife.TradLife_A.Enums.SexID` enum.
   * - ``IssueAge``
     - Age at policy issue.
   * - ``PaymentMode``
     - Premium payment mode (number of payments per year).
   * - ``PremFreq``
     - Premium-paying period in years.
   * - ``PolicyTerm``
     - Term of the policy in years.
   * - ``MaxPolicyTerm``
     - Maximum policy term used to cap term-dependent items.
   * - ``PolicyCount``
     - Number of policies represented by the model point.
   * - ``SumAssured``
     - Sum assured per policy.

Product specifications
^^^^^^^^^^^^^^^^^^^^^^

Named range: ``ProductSpecTable``

Per-product specification table holding loading parameters, surrender
charges and the mortality, interest and lapse references used on the
premium and valuation bases. Read column-by-column by
:func:`~annuallife.TradLife_A.InputData.product_spec`, which returns
each column as a Series keyed by ``Product`` / ``PolType`` / ``Gen``.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``Product``, ``PolType``, ``Gen``
     - Lookup keys. ``Product`` matches ``Product`` in ``PolicyData``;
       ``PolType`` and ``Gen`` are optional refinements and may be left
       blank for product-wide entries.
   * - ``LoadAcqSAParam<N>``
     - Linear parameters of the sum-assured-based acquisition loading,
       with ``N`` = 1, 2 (see
       :func:`~annuallife.TradLife_A.PolicyAttrs.load_acq_sa`).
   * - ``LoadMaintSA``, ``LoadMaintSA2``
     - Sum-assured-based maintenance loadings during and after the
       premium-paying period.
   * - ``LoadMaintPremParam<N>``
     - Linear parameters of the premium-based maintenance loading,
       with ``N`` = 1, 2 (see
       :func:`~annuallife.TradLife_A.PolicyAttrs.load_maint_prem`).
   * - ``SurrChargeParam<N>``
     - Parameters of the initial surrender charge, with ``N`` = 1, 2
       (see :func:`~annuallife.TradLife_A.PolicyAttrs.init_surr_charge`).
   * - ``MortTable<Basis>``
     - Mortality table ID (column of ``MortalityTables``) for
       ``<Basis>``, where ``Basis`` is ``Prem`` (premium basis) or
       ``Val`` (valuation basis).
   * - ``IntRate<Basis>``
     - Interest rate for ``<Basis>``; ``Basis`` as above.
   * - ``LapseRate<Basis>``
     - Annual lapse rate for ``<Basis>``; ``Basis`` as above.
   * - ``Hsx``, ``Tsx``, ``Hax``, ``Tax``
     - Optional commutation-function parameters for products that need
       them (left blank for products that do not).

Assumption parameters
^^^^^^^^^^^^^^^^^^^^^

Named range: ``AssumptionTable``

Table of actuarial assumption parameters — mortality and lapse
references, commission rates, expense factors, and tax/inflation
rates — keyed by ``Product`` / ``PolType`` / ``Gen``. Read
column-by-column by
:func:`~annuallife.TradLife_A.InputData.assumption`, which returns each
column as a Series. Rows are sparse: a product-level row sets the
defaults, and more specific (``PolType`` / ``Gen``) rows override
individual columns.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``Product``, ``PolType``, ``Gen``
     - Lookup keys for the assumption set.
   * - ``BaseMort``
     - Base mortality table ID (column of ``MortalityTables``).
   * - ``MortFactor``
     - Name of the ``AsmpByDuration`` column used as a duration-based
       mortality factor; resolved via
       :mod:`~annuallife.TradLife_A.Assumptions.AsmpID`.
   * - ``Surrender``
     - Name of the ``AsmpByDuration`` column used as the duration-based
       lapse rate.
   * - ``Renewal``
     - Renewal-premium retention assumption.
   * - ``InvstRet``
     - Assumed investment return.
   * - ``CommInitPrem``, ``CommRenPrem``
     - First-year and renewal-year commission rates as a fraction of
       premium.
   * - ``CommRenTerm``
     - Number of renewal years over which ``CommRenPrem`` applies.
   * - ``ExpsAcq<Unit>``
     - Acquisition expense factor per ``<Unit>``, where ``Unit`` is
       ``SA`` (per sum assured), ``AnnPrem`` (per annualised premium),
       or ``Pol`` (per policy).
   * - ``ExpsMaint<Unit>``
     - Maintenance expense factor per ``<Unit>``, where ``Unit`` is
       ``SA`` (per sum assured), ``Prem`` (per premium), or ``Pol``
       (per policy).
   * - ``InflRate``
     - Expense inflation rate applied to maintenance expenses.
   * - ``CnsmpTax``
     - Consumption-tax rate applied to expenses.

Assumptions by duration
^^^^^^^^^^^^^^^^^^^^^^^

Named range: ``AsmpByDuration``

Duration-indexed tables of mortality factors, morbidity rates, and
lapse rates. Read by
:func:`~annuallife.TradLife_A.InputData.assumption_tables`, which
returns a ``DataFrame`` indexed by ``Year``. Columns of this range are
referenced by name from ``AssumptionTable`` (e.g. ``MortFactor`` and
``Surrender``).

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``Year``
     - Policy duration in years; becomes the DataFrame index.
   * - ``MortAsmp<N>``
     - Duration-based mortality-factor tables (``N`` = 1, 2) selectable
       from ``MortFactor`` in ``AssumptionTable``.
   * - ``Morb<N>``
     - Duration-based morbidity-rate tables (``N`` = 1..5; defined for
       future use, not consumed by the current projection Cells).
   * - ``LapseRate<N>``
     - Duration-based lapse-rate tables (``N`` = 1) selectable from
       ``Surrender`` in ``AssumptionTable``.

Mortality tables
^^^^^^^^^^^^^^^^

Named range: ``MortalityTables``

Mortality rates by attained age and (mortality table ID, sex), with a
two-row header (``MortTable`` over ``Sex``). Read by
:func:`~annuallife.TradLife_A.InputData.mortality_tables`, which
returns a ``DataFrame`` indexed by age with a column ``MultiIndex`` of
``(MortTable, Sex)``.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``Age`` (row index)
     - Attained age in years.
   * - ``MortTable`` (top header)
     - Mortality table ID (integer); referenced by ``BaseMort`` in
       ``AssumptionTable`` and by ``MortTablePrem`` / ``MortTableVal``
       in ``ProductSpecTable``.
   * - ``Sex`` (sub-header)
     - Sex code (``M`` or ``F``) within each table.
   * - Cell value
     - Annual mortality rate for the (table, sex, age).

Economic scenarios
^^^^^^^^^^^^^^^^^^

Named range: ``Scenarios``

Read by :func:`~annuallife.TradLife_A.InputData.scenarios`, which
returns a ``DataFrame`` indexed by ``(ScenID, Year)``.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``ScenID``
     - Scenario ID. Selected through the ``scen_id`` parameter of
       :mod:`~annuallife.TradLife_A.Economic`.
   * - ``Year``
     - Time index (year) within the scenario.
   * - ``IntRate``
     - Annual interest rate at time ``Year`` under scenario ``ScenID``.

Large-policy premium discount
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Named range: ``LargePolDiscount``

Two-column range mapping sum-assured bands to a premium discount. Read
as a :obj:`dict` and turned into a per-policy ``Series`` by
:func:`~annuallife.TradLife_A.InputData.discount_rate`, which uses the
keys as left-closed band boundaries.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - First column
     - Upper bound of the sum-assured band. The last row may be left
       blank, in which case the final band has no upper bound.
   * - Second column
     - Premium discount applied to policies whose ``SumAssured`` falls
       in that band.

Premium-waiver cost
^^^^^^^^^^^^^^^^^^^

Named range: ``PremiumWaiverCost``

Two-column range mapping policy-term bands to a premium-waiver loading.
Read as a :obj:`dict` by
:func:`~annuallife.TradLife_A.InputData.prem_waiver_cost`.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - First column
     - Upper bound of the policy-term band. The last row may be left
       blank, in which case the final band has no upper bound.
   * - Second column
     - Premium-waiver cost loading for that band.

Constant parameters
^^^^^^^^^^^^^^^^^^^

Named range: ``ConstParams``

Two-column range of scalar parameters used across the model. Read as a
:obj:`dict` by :func:`~annuallife.TradLife_A.InputData.const_params`.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - First column
     - Parameter name (e.g. ``InflRate``, ``CnsmpTax``).
   * - Second column
     - Parameter value.

.. _tradlife_a-basic-usage:

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

Exporting the model
^^^^^^^^^^^^^^^^^^^

The model can be exported to a pure-Python (nomx) module that does not
depend on modelx. Use the ``export`` method on the model object::

    >>> m.export("TradLife_A_nomx")

This command exports the model as a Python package named
``TradLife_A_nomx`` in the current directory. You can test the exported
(nomx) model by importing it and accessing its cells::

    >>> from TradLife_A_nomx import mx_model

    >>> mx_model.Projection[0].pv_net_cf(0)

(Here, ``mx_model`` is the nomx model object.)

Global References
-----------------

Global references are names that can be referenced from formulas in any
space in the model. The third-party modules
`pandas <https://pandas.pydata.org/>`__ and
`numpy <https://numpy.org/>`__ are defined here, as are the enum types
defined as child spaces under :mod:`~annuallife.TradLife_A.Enums`.

Attributes:
    pd: The `pandas <https://pandas.pydata.org/>`__ module.
    np: The `numpy <https://numpy.org/>`__ module.
    ProductID: The product-type enum,
        :mod:`~annuallife.TradLife_A.Enums.ProductID` (``TERM`` term
        insurance, ``WL`` whole life, ``ENDW`` endowment).
    SexID: The sex enum,
        :mod:`~annuallife.TradLife_A.Enums.SexID` (``M`` male,
        ``F`` female).
    RateBasisID: The rate-basis enum,
        :mod:`~annuallife.TradLife_A.Enums.RateBasisID` (``PREM`` premium
        basis, ``VAL`` valuation basis).

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