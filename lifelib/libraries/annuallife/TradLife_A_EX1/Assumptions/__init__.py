# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Assumption input and calculations for individual policies.

This Space is :mod:`TradLife_A.Assumptions <annuallife.TradLife_A.Assumptions>` with additional
Cells that supply the Solvency II life-risk parameters. The per-policy
assumption pipeline (``map_to_policies`` then ``pandas_to_array``) and
all the existing assumption Cells are unchanged; see
:mod:`TradLife_A.Assumptions <annuallife.TradLife_A.Assumptions>` for them.

Cells Summary
-------------

New Cells
^^^^^^^^^

:func:`life_shock_param` forwards a life-shock factor from
:func:`~annuallife.TradLife_A_EX1.InputData.life_shock_data`, keyed by the
``(risk, shock, scope, extra_key)`` codes. :func:`life_corr` forwards a
single life-risk correlation coefficient from
:func:`~annuallife.TradLife_A_EX1.InputData.life_corr_data` as a native
:obj:`float`. :func:`coc_rate` forwards the cost-of-capital rate
(``CoCRate``) used by
:func:`~annuallife.TradLife_A_EX1.Projection.risk_margin`.

.. autosummary::

   ~life_shock_param
   ~life_corr
   ~coc_rate

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


def coc_rate():
    """Cost-of-capital rate for the Solvency II risk margin.

    Forwards the ``CoCRate`` scalar from the ``ConstParams`` named range
    (read by :func:`~annuallife.TradLife_A_EX1.InputData.const_params`) to the
    projection, where it is used by
    :func:`~annuallife.TradLife_A_EX1.Projection.risk_margin`. The value is a
    native :obj:`float` (e.g. ``0.06`` for 6%).
    """
    return input_data.const_params()['CoCRate']


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
    :func:`TradLife_A.InputData.policy_data <annuallife.TradLife_A.InputData.policy_data>`.
    """
    return map_to_policies(input_data.assumption('BaseMort'))


def mort_array_index():
    """Per-policy column index into :func:`mortality_tables`.

    Returns a 1-D integer array of column positions in
    :func:`TradLife_A.InputData.mortality_tables <annuallife.TradLife_A.InputData.mortality_tables>` for each
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
    Used by :func:`TradLife_A.BaseProj.mort_factor <annuallife.TradLife_A.BaseProj.mort_factor>` and
    :func:`TradLife_A.BaseProj.lapse_rate <annuallife.TradLife_A.BaseProj.lapse_rate>` together with
    :func:`mort_factor_index` and :func:`lapse_rate_index`.
    """
    return pandas_to_array(input_data.assumption_tables())


def mort_factor_index():
    """Per-policy column index into :func:`asmp_tables` for mortality factors.

    Resolves each policy's ``MortFactor`` assumption (referencing an
    :mod:`TradLife_A.Assumptions.AsmpID <annuallife.TradLife_A.Assumptions.AsmpID>`) to its column
    position in the ``AsmpByDuration`` table.
    """


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_data.assumption_tables().columns)}

    indexes = input_data.assumption('MortFactor').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def lapse_rate_index():
    """Per-policy column index into :func:`asmp_tables` for lapse rates.

    Resolves each policy's ``Surrender`` assumption (referencing an
    :mod:`TradLife_A.Assumptions.AsmpID <annuallife.TradLife_A.Assumptions.AsmpID>`) to its column
    position in the ``AsmpByDuration`` table.
    """


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_data.assumption_tables().columns)}

    indexes = input_data.assumption('Surrender').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def asmp_table_len():
    """Number of rows (durations) in :func:`asmp_tables`."""
    return len(asmp_tables())


def life_shock_param(risk, shock=0, scope=0, extra_key=0):
    """Life shock factor for the given risk / shock / scope / extra key.

    Forwards a single value from
    :func:`~annuallife.TradLife_A_EX1.InputData.life_shock_data`, the
    ``LifeShocks`` input keyed by the ``(risk, shock, scope, extra_key)``
    integer codes. Arguments left at their default ``0`` select the entry
    with no shock / scope / extra qualifier.

    Args:
        risk: A ``LifeRiskID`` code for the life sub-risk.
        shock: A ``LapseShockID`` code (lapse risk only); defaults to 0.
        scope: A ``LapseScopeID`` code; defaults to 0.
        extra_key: An ``ExtraKeyID`` code (e.g. ``LIMIT``, ``INFL``);
            defaults to 0.
    """
    return input_data.life_shock_data()[risk, shock, scope, extra_key]


def life_corr(risk_i, risk_j):
    """Correlation coefficient between two life underwriting sub-risks.

    Forwards a single coefficient from the correlation matrix read by
    :func:`~annuallife.TradLife_A_EX1.InputData.life_corr_data`. The two
    risks are taken as integer parameters and a plain :obj:`float` is
    returned (rather than a :obj:`dict` or :class:`~pandas.DataFrame`) so
    that the consuming :func:`~annuallife.TradLife_A_EX1.Projection.risk_life`
    cell stays on native scalar types, which matters when the projection
    is compiled with Cython.

    Args:
        risk_i: A ``LifeRiskID``
            code for the first sub-risk.
        risk_j: A ``LifeRiskID``
            code for the second sub-risk.
    """
    return float(input_data.life_corr_data().at[risk_i, risk_j])


# ---------------------------------------------------------------------------
# References

input_data = ("Interface", ("..", "InputData"), "auto")

LifeRiskID = ("Interface", ("..", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("..", "Enums", "LapseShockID"), "auto")

LapseScopeID = ("Interface", ("..", "Enums", "LapseScopeID"), "auto")

ExtraKeyID = ("Interface", ("..", "Enums", "ExtraKeyID"), "auto")