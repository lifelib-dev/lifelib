# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Example of a nested projection model, illustrated with a Solvency II life-risk SCR and risk margin.

Overview
--------

The purpose of :mod:`~annuallife.TradLife_A_EX1` is to demonstrate how to
build a **nested projection** in modelx — a projection that, at each
step, runs further *inner* projections. It is not intended as a complete
Solvency II model; the Solvency II life-risk SCR and risk margin are used
only as a concrete example to motivate the nested projection.

The model extends :mod:`~annuallife.TradLife_A`. At a valuation time
``t0`` it re-runs the per-policy cashflow projection under each
prescribed life stress (the *inner* projections) and compares the
stressed and unstressed present values of net cashflows to obtain:

* the capital requirement for each life sub-risk (mortality, longevity,
  lapse and expense),
* the aggregated life underwriting SCR, and
* the risk margin.

The inner projections are carried out by a new Space,
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`, nested under
:mod:`~annuallife.TradLife_A_EX1.Projection` and anchored at the
valuation time ``t0``.

The products, projection logic, assumptions, economic scenarios and input
workbook are otherwise the same as :mod:`~annuallife.TradLife_A`. Only
the Spaces that change are described below and on their own pages; for
everything else, refer to :mod:`~annuallife.TradLife_A`.

How the nested projection is implemented
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To represent a projection that starts a fresh projection at each
projection step, a child Space of
:mod:`~annuallife.TradLife_A_EX1.Projection`,
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`, is defined.
``Projection[idx].InnerProj[t0]`` is the inner projection of model point
``idx`` started at time ``t0``.

:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj` is parameterized
with ``t0``, the start time of the inner projection (together with
``risk`` and ``shock``, which select the life stress). The whole
projection logic is inherited from :mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>`
and :mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`; only the Cells specific to the
inner projection are overridden.

The inner projection starts from the state of the outer projection at
``t0``. The overridden
:func:`~annuallife.TradLife_A_EX1.Projection.InnerProj.pols_if` returns
the *outer* projection's in-force at ``t == t0`` and projects forward for
``t > t0``::

    def pols_if(t):
        if t == t0:
            return _space._parent._parent.pols_if(t)
        else:
            return pols_if_beg1(t - 1) - pols_death(t - 1) - pols_lapse(t - 1)

In a Cells formula ``_space`` is the current ``InnerProj[t0, risk,
shock]`` ItemSpace; its parent is the ``InnerProj`` Space and that
Space's parent is the enclosing ``Projection[idx]`` ItemSpace. So
``_space._parent._parent`` is the outer projection, and
``_space._parent._parent.pols_if(t)`` reads its in-force at ``t0``. The
same idiom is used by the other overridden rate Cells —
:func:`~annuallife.TradLife_A_EX1.Projection.InnerProj.mort_rate`,
:func:`~annuallife.TradLife_A_EX1.Projection.InnerProj.lapse_rate` and
:func:`~annuallife.TradLife_A_EX1.Projection.InnerProj.commissions_ren_pp`
— which read the unstressed rate from the outer projection and apply the
life shock to it.

The outer :mod:`~annuallife.TradLife_A_EX1.Projection` reads results back
from the inner projection by indexing into the child Space. For example,
:func:`~annuallife.TradLife_A_EX1.Projection.risk_life_sub` evaluates the
present value of net cashflows of the unstressed and stressed inner
projections started at ``t`` and takes their difference::

    def risk_life_sub(t, risk):
        base_pv = InnerProj[t].pv_net_cf(t)
        ...
        return max(base_pv - InnerProj[t, risk].pv_net_cf(t), 0)

``InnerProj[t]`` is the unstressed inner projection started at ``t`` and
``InnerProj[t, risk]`` the one under the ``risk`` stress, with
:func:`TradLife_A.PV.pv_net_cf <annuallife.TradLife_A.PV.pv_net_cf>` evaluated at ``t`` on each.

Changes from TradLife_A
^^^^^^^^^^^^^^^^^^^^^^^

.. rubric:: New Spaces

* :mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj` — an inner
  projection, parameterized by the valuation time ``t0`` and a
  ``(risk, shock)`` pair, that re-runs the cashflow projection under a
  single prescribed life stress. It inherits from
  :mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>` and
  :mod:`TradLife_A.PV <annuallife.TradLife_A.PV>` and overrides the decrement,
  mortality, lapse and expense Cells to apply the shock, taking the
  unstressed rates from the outer projection.
* Four enum child Spaces under
  :mod:`~annuallife.TradLife_A_EX1.Enums` — ``LifeRiskID`` (life
  sub-risks), ``LapseShockID`` (lapse up / down / mass), ``LapseScopeID``
  (retail / non-retail) and ``ExtraKeyID`` (extra shock qualifiers).

.. rubric:: Updated Spaces

* :mod:`~annuallife.TradLife_A_EX1.Projection` adds the Solvency II
  output Cells
  :func:`~annuallife.TradLife_A_EX1.Projection.risk_life_sub` (capital
  requirement per life sub-risk),
  :func:`~annuallife.TradLife_A_EX1.Projection.risk_life` (aggregated
  life SCR) and
  :func:`~annuallife.TradLife_A_EX1.Projection.risk_margin` (risk
  margin), and gains the ``InnerProj`` child Space.
* :mod:`~annuallife.TradLife_A_EX1.Assumptions` adds
  :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param` (life
  shock factors),
  :func:`~annuallife.TradLife_A_EX1.Assumptions.life_corr` (life-risk
  correlation coefficient) and
  :func:`~annuallife.TradLife_A_EX1.Assumptions.coc_rate`
  (cost-of-capital rate).
* :mod:`~annuallife.TradLife_A_EX1.InputData` adds
  :func:`~annuallife.TradLife_A_EX1.InputData.life_shock_data` and
  :func:`~annuallife.TradLife_A_EX1.InputData.life_corr_data`, which read
  the ``LifeShocks`` and ``LifeCorr`` named ranges, reads the new
  ``CoCRate`` value from ``ConstParams``, and generalizes
  :func:`~annuallife.TradLife_A_EX1.InputData.get_named_range_as_dict` to
  support named ranges with multi-column (tuple) keys.
* :mod:`~annuallife.TradLife_A_EX1.PolicyAttrs` adds
  :func:`~annuallife.TradLife_A_EX1.PolicyAttrs.segment`, the per-policy
  lapse-risk segment.

The :mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>`,
:mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`,
:mod:`TradLife_A.Economic <annuallife.TradLife_A.Economic>`,
:mod:`TradLife_A.CommTable <annuallife.TradLife_A.CommTable>` and
:mod:`TradLife_A.Utilities <annuallife.TradLife_A.Utilities>` Spaces are unchanged from
:mod:`~annuallife.TradLife_A`; refer to it for them. In particular the
life shocks are applied entirely within
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`, so
:mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>` needs no modification.

.. rubric:: Input workbook

:mod:`~annuallife.TradLife_A_EX1` reads the same *input.xlsx* as
:mod:`~annuallife.TradLife_A`, with three additional inputs: the
``LifeShocks`` and ``LifeCorr`` named ranges and a ``CoCRate`` row in
the ``ConstParams`` range.

Model Structure
---------------

Unlike the rest of this page, which documents only the Spaces that change
from :mod:`~annuallife.TradLife_A`, this section shows the **complete**
space structure of the model, so the new and updated Spaces can be seen
alongside the ones inherited unchanged from
:mod:`~annuallife.TradLife_A`. The *Status* column marks each Space as
new, updated or unchanged; the unchanged Spaces link back to
:mod:`~annuallife.TradLife_A`.

.. list-table::
   :header-rows: 1
   :widths: 24 14 62

   * - Space
     - Status
     - Description
   * - :mod:`~annuallife.TradLife_A_EX1.InputData`
     - Updated
     - Reads *input.xlsx*; adds the ``LifeShocks`` and ``LifeCorr``
       readers and the ``CoCRate`` constant.
   * - :mod:`TradLife_A.Economic <annuallife.TradLife_A.Economic>`
     - Unchanged
     - Scenario-dependent economic (discount) rates; parameter
       ``scen_id``.
   * - :mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>`
     - Unchanged
     - Per-period cashflow projection cells; base of ``Projection`` and
       ``InnerProj``.
   * - :mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`
     - Unchanged
     - Present values of the projected cashflows; base of ``Projection``
       and ``InnerProj``.
   * - :mod:`~annuallife.TradLife_A_EX1.Projection`
     - Updated
     - Per-model-point projection; adds the life SCR and risk-margin
       Cells and the ``InnerProj`` child Space.
   * - :mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`
     - New
     - Inner projection re-run under a single life stress, anchored at
       ``t0``; child Space of ``Projection``.
   * - :mod:`~annuallife.TradLife_A_EX1.Assumptions`
     - Updated
     - Per-policy assumptions; adds the life-shock, correlation and
       cost-of-capital parameters.
   * - :mod:`~annuallife.TradLife_A_EX1.PolicyAttrs`
     - Updated
     - Per-policy attributes; adds the lapse-risk ``segment``.
   * - :mod:`TradLife_A.Utilities <annuallife.TradLife_A.Utilities>`
     - Unchanged
     - Helper cells (``pandas_to_array``, ``map_to_policies``); base of
       ``Assumptions`` and ``PolicyAttrs``.
   * - :mod:`TradLife_A.CommTable <annuallife.TradLife_A.CommTable>`
     - Unchanged
     - Commutation functions and actuarial notations; parameters
       ``Sex``, ``IntRate`` and ``Table``.
   * - :mod:`~annuallife.TradLife_A_EX1.Enums`
     - Updated
     - Enum types; adds the life-risk enums (``LifeRiskID``,
       ``LapseShockID``, ``LapseScopeID``, ``ExtraKeyID``).

Inheritance
^^^^^^^^^^^

As in :mod:`~annuallife.TradLife_A`,
:mod:`~annuallife.TradLife_A_EX1.Projection` inherits from
:mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>` and
:mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`, while
:mod:`~annuallife.TradLife_A_EX1.Assumptions` and
:mod:`~annuallife.TradLife_A_EX1.PolicyAttrs` inherit from
:mod:`TradLife_A.Utilities <annuallife.TradLife_A.Utilities>`. The new
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj` also inherits the
same projection logic from
:mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>` and
:mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`.

.. mermaid::

    %%{init: {"class": {"hideEmptyMembersBox": true}}}%%
    classDiagram
        BaseProj <|-- Projection
        PV <|-- Projection
        BaseProj <|-- InnerProj
        PV <|-- InnerProj
        Utilities <|-- Assumptions
        Utilities <|-- PolicyAttrs

Composition
^^^^^^^^^^^

Besides inheritance, the model nests Spaces as child Spaces. The tree
below is rooted at the :mod:`~annuallife.TradLife_A_EX1` model and
includes the Spaces inherited unchanged from
:mod:`~annuallife.TradLife_A`; the new inner projection
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj` is a child Space
of :mod:`~annuallife.TradLife_A_EX1.Projection`. The enum child Spaces
under :mod:`~annuallife.TradLife_A_EX1.Enums` (e.g. ``LifeRiskID``) and
the ``AsmpID`` enum under
:mod:`~annuallife.TradLife_A_EX1.Assumptions` are omitted from the
diagram for clarity.

.. mermaid::

    %%{init: {"class": {"hideEmptyMembersBox": true}}}%%
    classDiagram
        direction TB
        TradLife_A_EX1 *-- InputData
        TradLife_A_EX1 *-- Economic
        TradLife_A_EX1 *-- BaseProj
        TradLife_A_EX1 *-- PV
        TradLife_A_EX1 *-- Projection
        Projection *-- InnerProj
        TradLife_A_EX1 *-- Assumptions
        TradLife_A_EX1 *-- PolicyAttrs
        TradLife_A_EX1 *-- Utilities
        TradLife_A_EX1 *-- CommTable
        TradLife_A_EX1 *-- Enums

Cross-space references
^^^^^^^^^^^^^^^^^^^^^^

The cross-space References are the same as in
:mod:`~annuallife.TradLife_A`:
:mod:`~annuallife.TradLife_A_EX1.Projection` (and, by inheritance,
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`) resolve ``scen``,
``asmp``, ``pol`` and ``comm_table`` to
:mod:`TradLife_A.Economic <annuallife.TradLife_A.Economic>`,
:mod:`~annuallife.TradLife_A_EX1.Assumptions`,
:mod:`~annuallife.TradLife_A_EX1.PolicyAttrs` and
:mod:`TradLife_A.CommTable <annuallife.TradLife_A.CommTable>`, which in
turn reference :mod:`~annuallife.TradLife_A_EX1.InputData` as
``input_data``. In addition,
:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj` reads the outer
:mod:`~annuallife.TradLife_A_EX1.Projection` through
``_space._parent._parent``, and the outer projection reads results back
from the inner projections.

.. mermaid::

    graph LR
        Projection -- scen --> Economic
        Projection -- asmp --> Assumptions
        Projection -- pol --> PolicyAttrs
        Projection -- comm_table --> CommTable
        Projection -- risk_life --> InnerProj
        InnerProj -. reads outer .-> Projection
        Economic -- input_data --> InputData
        Assumptions -- input_data --> InputData
        PolicyAttrs -- input_data --> InputData
        CommTable -- input_data --> InputData

Basic Usage
-----------

Read and run the model exactly as :mod:`~annuallife.TradLife_A` (see its
:ref:`Basic Usage <tradlife_a-basic-usage>` section), using the
``TradLife_A_EX1`` folder::

    >>> import modelx as mx

    >>> m = mx.read_model("TradLife_A_EX1")

The Solvency II results are obtained from the
:mod:`~annuallife.TradLife_A_EX1.Projection` Space, for example::

    >>> m.Projection[0].risk_life(0)        # aggregated life SCR at t=0

    >>> m.Projection[0].risk_margin(0)      # risk margin at t=0

    >>> m.Projection[0].risk_life_sub(0, m.Enums.LifeRiskID.MORT)

Global References
-----------------

The model-level References (``pd``, ``np``, ``ProductID``, ``SexID`` and
``RateBasisID``) are the same as in :mod:`~annuallife.TradLife_A`.

"""

from modelx.serialize.jsonvalues import *

_name = "TradLife_A_EX1"

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