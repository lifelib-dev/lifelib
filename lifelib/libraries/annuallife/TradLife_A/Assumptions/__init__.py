# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Assumption input and calculations for individual policies.

This Space holds assumption parameters and rates used by
:mod:`~annuallife.TradLife_A.Projection` and its base spaces.

The main role of this Space is to associate assumption data sourced
from :mod:`~annuallife.TradLife_A.InputData` with the model points
held in
:func:`~annuallife.TradLife_A.InputData.policy_data`, and to expose
the resulting per-policy values as 1-D :mod:`numpy` arrays whose
layout matches the rows of ``policy_data``. Callers therefore index
into them with the integer policy index ``idx``. A few cells, such
as :func:`asmp_tables` and :func:`mortality_tables`, return tables
shared across all policies.

The association is carried out by chaining two helper cells inherited
from the :mod:`~annuallife.TradLife_A.Utilities` base Space:

* :func:`~annuallife.TradLife_A.Utilities.map_to_policies` reindexes
  an assumption ``Series`` keyed by lookup columns (e.g. ``Product``,
  ``PolType``, ``Gen``) onto the rows of ``policy_data``, so the
  result has one entry per policy.
* :func:`~annuallife.TradLife_A.Utilities.pandas_to_array` then
  converts that ``Series`` (or a ``DataFrame``, for table-returning
  cells) into a NumPy array when
  :attr:`~annuallife.TradLife_A.Utilities.return_array` is ``True``
  (the default). When ``return_array`` is ``False`` the pandas
  object is passed through unchanged, which is convenient for
  inspection and debugging.

A typical per-policy Cells in this Space therefore implements the
following pipeline:

.. mermaid::

    graph LR
        A["input_data.assumption(key)<br/>pandas Series keyed by<br/>(Product, PolType, Gen)"]
        --> B["map_to_policies<br/>reindex onto<br/>policy_data rows"]
        B --> C["pandas_to_array<br/>convert when<br/>return_array=True"]
        C --> D["1-D NumPy array<br/>indexed by policy idx"]

For example, :func:`comm_init_prem` is implemented as
``pandas_to_array(map_to_policies(input_data.assumption('CommInitPrem')))``,
and most other per-policy cells in this Space follow the same
pattern.

The three steps can also be executed individually on a console,
which is useful for inspecting the intermediate pandas objects::

    >>> asmp = m.Assumptions

    >>> # Step 1: raw assumption Series keyed by lookup columns
    >>> s = asmp.input_data.assumption('CommInitPrem')
    >>> s
    Product
    TERM    0.2
    WL      0.5
    ENDW    0.5
    Name: CommInitPrem, dtype: float64

    >>> # Step 2: reindex onto the rows of policy_data
    >>> mapped = asmp.map_to_policies(s)
    >>> mapped.head()
    Policy
    1    0.2
    2    0.2
    3    0.2
    4    0.2
    5    0.2
    Name: CommInitPrem, dtype: float64
    >>> len(mapped)
    300

    >>> # Step 3: convert to a 1-D NumPy array (return_array is True)
    >>> asmp.pandas_to_array(mapped)
    array([0.2, 0.2, 0.2, ..., 0.5, 0.5, 0.5])

Composing the three calls is exactly what :func:`comm_init_prem`
returns.

Parameters and References
-------------------------

Attributes:
    input_data: Alias for :mod:`~annuallife.TradLife_A.InputData`.
        Per-policy assumptions are read from the ``AssumptionTable``
        range in *input.xlsx* via
        :func:`~annuallife.TradLife_A.InputData.assumption`,
        and mortality / lapse tables from
        :func:`~annuallife.TradLife_A.InputData.assumption_tables` and
        :func:`~annuallife.TradLife_A.InputData.mortality_tables`.

.. rubric:: Inherited helpers

Inherited from :mod:`~annuallife.TradLife_A.Utilities`:

* :func:`~annuallife.TradLife_A.Utilities.pandas_to_array`
* :func:`~annuallife.TradLife_A.Utilities.map_to_policies`
* :attr:`~annuallife.TradLife_A.Utilities.return_array`

.. rubric:: Child spaces

* :mod:`~annuallife.TradLife_A.Assumptions.AsmpID`: Enum-style codes
  identifying entries in the ``AsmpByDuration`` table.


Cells Summary
-------------

Commission Assumptions
^^^^^^^^^^^^^^^^^^^^^^

Per-policy initial and renewal commission rates and the renewal
commission term.

.. autosummary::

   ~comm_init_prem
   ~comm_ren_prem
   ~comm_ren_term


Expense Assumptions
^^^^^^^^^^^^^^^^^^^

Per-policy acquisition and maintenance expense assumptions, expressed
per annualized premium, per policy and per sum assured.

.. autosummary::

   ~exps_acq_ann_prem
   ~exps_acq_pol
   ~exps_acq_sa
   ~exps_maint_ann_prem
   ~exps_maint_pol
   ~exps_maint_sa


Tax and Inflation Assumptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The consumption tax rate and the expense inflation rate.

.. autosummary::

   ~cnsmp_tax
   ~inflation_rate


Mortality
^^^^^^^^^

The mortality-table block and the per-policy indices that select each
policy's base mortality rates and its last mortality age.

.. autosummary::

   ~mortality_tables
   ~mort_table_index
   ~mort_array_index
   ~last_mort_age


Mortality Factor and Lapse
^^^^^^^^^^^^^^^^^^^^^^^^^^

The assumption-by-duration table and the per-policy indices that
select mortality factors and lapse rates, together with its row count.

.. autosummary::

   ~asmp_tables
   ~mort_factor_index
   ~lapse_rate_index
   ~asmp_table_len

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = [
    ".Utilities"
]

_allow_none = None

_spaces = [
    "AsmpID"
]

# ---------------------------------------------------------------------------
# Cells

def cnsmp_tax():
    """Consumption tax rate"""
    return input_data.const_params()['CnsmpTax']


def comm_init_prem():
    """Initial commission per premium"""
    return pandas_to_array(map_to_policies(input_data.assumption('CommInitPrem')))


def comm_ren_prem():
    """Renewal commission per premium"""
    return pandas_to_array(map_to_policies(input_data.assumption('CommRenPrem')))


def comm_ren_term():
    """Renewal commission term"""
    return pandas_to_array(map_to_policies(input_data.assumption('CommRenTerm')))


def exps_acq_ann_prem():
    """Acquisition expense per annualized premium"""
    return pandas_to_array(map_to_policies(input_data.assumption('ExpsAcqAnnPrem')))


def exps_acq_pol():
    """Acquisition expense per policy"""
    return pandas_to_array(map_to_policies(input_data.assumption('ExpsAcqPol')))


def exps_acq_sa():
    """Acquisition expense per sum assured"""
    return pandas_to_array(map_to_policies(input_data.assumption('ExpsAcqSA')))


def exps_maint_ann_prem():
    """Maintenance expense per annualized premium"""
    return pandas_to_array(map_to_policies(input_data.assumption('ExpsMaintPrem')))


def exps_maint_pol():
    """Maintenance expense per policy"""
    return pandas_to_array(map_to_policies(input_data.assumption('ExpsMaintPol')))


def exps_maint_sa():
    """Maintenance expense per sum assured"""
    return pandas_to_array(map_to_policies(input_data.assumption('ExpsMaintSA')))


def inflation_rate():
    """Inflation rate"""
    return input_data.const_params()['InflRate']


def mortality_tables():
    """Mortality tables read from *input.xlsx*.

    Returns the full mortality-table block from the ``MortalityTables``
    range as a 2-D NumPy array (when ``return_array`` is ``True``),
    where rows are indexed by age and columns by ``(MortTable, Sex)``.
    """

    tables = input_data.mortality_tables()
    return pandas_to_array(tables)


def mort_table_index():
    """Per-policy mortality table identifier.

    Maps the ``BaseMort`` assumption keyed by the model point lookup
    (product, policy type, gen) to each row of
    :func:`~annuallife.TradLife_A.InputData.policy_data`.
    """
    return map_to_policies(input_data.assumption('BaseMort'))


def mort_array_index():
    """Per-policy column index into :func:`mortality_tables`.

    Returns a 1-D integer array of column positions in
    :func:`~annuallife.TradLife_A.InputData.mortality_tables` for each
    policy's ``(mort_table_index, sex)`` pair.
    """

    columns = input_data.mortality_tables().columns

    # Get the column positions in input_data.mortality_tables for each (MortID, sex) pair
    return columns.get_indexer(
        pd.MultiIndex.from_arrays([mort_table_index(), input_data.policy_data()['Sex']])
    )


def last_mort_age():
    """Last mortality age per policy (first age where mortality reaches 1)."""

    last_ages = input_data.mort_table_last_ages()
    keys = pd.MultiIndex.from_arrays(
        [mort_table_index(), input_data.policy_data()['Sex']]
    )
    result = pd.Series(last_ages.reindex(keys).values,
                       index=input_data.policy_data().index)
    return pandas_to_array(result)


def asmp_tables():
    """Assumption tables by duration.

    Returns the ``AsmpByDuration`` range from *input.xlsx* as a 2-D
    NumPy array indexed by duration (rows) and assumption ID (columns).
    Used by :func:`~annuallife.TradLife_A.BaseProj.mort_factor` and
    :func:`~annuallife.TradLife_A.BaseProj.lapse_rate` together with
    :func:`mort_factor_index` and :func:`lapse_rate_index`.
    """
    return pandas_to_array(input_data.assumption_tables())


def mort_factor_index():
    """Per-policy column index into :func:`asmp_tables` for mortality factors.

    Resolves each policy's ``MortFactor`` assumption (referencing an
    :mod:`~annuallife.TradLife_A.Assumptions.AsmpID`) to its column
    position in the ``AsmpByDuration`` table.
    """


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_data.assumption_tables().columns)}

    indexes = input_data.assumption('MortFactor').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def lapse_rate_index():
    """Per-policy column index into :func:`asmp_tables` for lapse rates.

    Resolves each policy's ``Surrender`` assumption (referencing an
    :mod:`~annuallife.TradLife_A.Assumptions.AsmpID`) to its column
    position in the ``AsmpByDuration`` table.
    """


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_data.assumption_tables().columns)}

    indexes = input_data.assumption('Surrender').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def asmp_table_len():
    """Number of rows (durations) in :func:`asmp_tables`."""
    return len(asmp_tables())


# ---------------------------------------------------------------------------
# References

input_data = ("Interface", ("..", "InputData"), "auto")