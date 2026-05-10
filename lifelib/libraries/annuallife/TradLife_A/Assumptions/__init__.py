# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Assumption input and calculations for individual policies.

This Space is a child Space of :mod:`~simplelife.model.Projection`,
and it holds assumption parameters and rates used
by the :mod:`~simplelife.model.Projection` Space.

.. figure:: /images/projects/simplelife/model/Assumptions/diagram1.png

.. rubric:: Parameters

Since :mod:`~simplelife.model.Projection` is parameterized with
:attr:`idx` and :attr:`scen_id`, this Space is also
parameterized as a child space of :mod:`~simplelife.model.Projection`.
For example, ``simplelife.Projection[1].Assumptions.exps_maint_sa()``
represents the expense maintenance per sum assured for Policy 1.

Attributes:
    idx(:obj:`int`): Policy ID
    scen_id(:obj:`int`, optional): Scenario ID, defaults to 1.

.. rubric:: References

Attributes:
    AssumptionTables: `ExcelRange`_ object holding data read from the
        Excel range *AssumptionTable* in *input.xlsx*.

    MortalityTable: `ExcelRange`_ object holding mortality tables.
        The data is read from *mortality_tables* range in *input.xlsx*.

    prod: Alias for :func:`simplelife.Projection.Policy.product`
    polt: Alias for :func:`simplelife.Projection.Policy.policy_type`
    gen: Alias for :func:`simplelife.Projection.Policy.gen`
    sex: Alias for :func:`simplelife.Projection.Policy.sex`
    asmp_lookup: Alias for :func:`simplelife.input_data.asmp_lookup`

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

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

def mort_rate(x):
    """Bae mortality rate"""

    return _space.asmp_lookup

    table_id = _space.asmp_lookup.match("BaseMort", prod(), polt(), gen()).value
    return mortality_tables[table_id, sex(), x]


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
    """Mortality Table"""

    tables = input_data.mortality_tables()
    # return tables.to_numpy() if return_array else tables
    return pandas_to_array(tables)


def mort_table_index():
    # s = input_data.assumption('BaseMort')

    # return s.reindex(pd.MultiIndex.from_frame(
    #     input_data.policy_data()[s.index.names]))
    return map_to_policies(input_data.assumption('BaseMort'))


def mort_array_index():

    columns = input_data.mortality_tables().columns

    # Get the column positions in input_data.mortality_tables for each (MortID, sex) pair
    return columns.get_indexer(
        pd.MultiIndex.from_arrays([mort_table_index(), input_data.policy_data()['Sex']])
    )


def last_mort_age():
    """Last mortality age (first age where mortality reaches 1) per policy."""

    last_ages = input_data.mort_table_last_ages()
    keys = pd.MultiIndex.from_arrays(
        [mort_table_index(), input_data.policy_data()['Sex']]
    )
    result = pd.Series(last_ages.reindex(keys).values,
                       index=input_data.policy_data().index)
    return pandas_to_array(result)


def asmp_tables():
    return pandas_to_array(input_data.assumption_tables())


def mort_factor_index():


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_data.assumption_tables().columns)}

    indexes = input_data.assumption('MortFactor').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def lapse_rate_index():


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_data.assumption_tables().columns)}

    indexes = input_data.assumption('Surrender').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def asmp_table_len():
    return len(asmp_tables())


# ---------------------------------------------------------------------------
# References

input_data = ("Interface", ("..", "InputData"), "auto")

return_array = True