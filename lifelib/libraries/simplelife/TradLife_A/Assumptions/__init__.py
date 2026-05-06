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
    asmp_lookup: Alias for :func:`simplelife.input_.asmp_lookup`

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
    # return asmp_lookup("CnsmpTax")
    # return pandas_to_array(map_to_policies(input_.assumption('CnsmpTax')))
    return input_.const_params()['CnsmpTax']


def comm_init_prem():
    """Initial commission per premium"""
    # result = _space.asmp_lookup.match("CommInitPrem", prod(), polt(), gen()).value

    # if result is not None:
    #     return result
    # else:
    #     raise ValueError('comm_init_prem not found')

    return pandas_to_array(map_to_policies(input_.assumption('CommInitPrem')))


def comm_ren_prem():
    """Renewal commission per premium"""
    # result = _space.asmp_lookup.match("CommRenPrem", prod(), polt(), gen()).value

    # if result is not None:
    #     return  result
    # else:
    #     raise ValueError('comm_ren_prem not found')

    return pandas_to_array(map_to_policies(input_.assumption('CommRenPrem')))


def comm_ren_term():
    """Renewal commission term"""
    # result = _space.asmp_lookup.match("CommRenTerm", prod(), polt(), gen()).value

    # if result is not None:
    #     return result
    # else:
    #     raise ValueError('comm_ren_term not found')

    return pandas_to_array(map_to_policies(input_.assumption('CommRenTerm')))


def exps_acq_ann_prem():
    """Acquisition expense per annualized premium"""
    # return _space.asmp_lookup.match("ExpsAcqAnnPrem", prod(), polt(), gen()).value

    return pandas_to_array(map_to_policies(input_.assumption('ExpsAcqAnnPrem')))


def exps_acq_pol():
    """Acquisition expense per policy"""
    # return _space.asmp_lookup.match("ExpsAcqPol", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(input_.assumption('ExpsAcqPol')))


def exps_acq_sa():
    """Acquisition expense per sum assured"""
    # return _space.asmp_lookup.match("ExpsAcqSA", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(input_.assumption('ExpsAcqSA')))


def exps_maint_ann_prem():
    """Maintenance expense per annualized premium"""
    # return _space.asmp_lookup.match("ExpsMaintPrem", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(input_.assumption('ExpsMaintPrem')))


def exps_maint_pol():
    """Maintenance expense per policy"""
    # return _space.asmp_lookup.match("ExpsMaintPol", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(input_.assumption('ExpsMaintPol')))


def exps_maint_sa():
    """Maintenance expense per sum assured"""
    # return _space.asmp_lookup.match("ExpsMaintSA", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(input_.assumption('ExpsMaintSA')))


def inflation_rate():
    """Inflation rate"""
    # return asmp_lookup("InflRate")
    # return pandas_to_array(map_to_policies(input_.assumption('InflRate')))
    return input_.const_params()['InflRate']


def mortality_tables():
    """Mortality Table"""

    tables = input_.mortality_tables()
    # return tables.to_numpy() if return_array else tables
    return pandas_to_array(tables)


def mort_table_index():
    # s = input_.assumption('BaseMort')

    # return s.reindex(pd.MultiIndex.from_frame(
    #     input_.policy_data()[s.index.names]))
    return map_to_policies(input_.assumption('BaseMort'))


def mort_array_index():

    columns = input_.mortality_tables().columns

    # Get the column positions in input_.mortality_tables for each (MortID, sex) pair
    return columns.get_indexer(
        pd.MultiIndex.from_arrays([mort_table_index(), input_.policy_data()['Sex']])
    )


def asmp_tables():
    return pandas_to_array(input_.assumption_tables())


def mort_factor_index():


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_.assumption_tables().columns)}

    indexes = input_.assumption('MortFactor').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def lapse_rate_index():


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(input_.assumption_tables().columns)}

    indexes = input_.assumption('Surrender').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def asmp_table_len():
    return len(asmp_tables())


# ---------------------------------------------------------------------------
# References

asmp_lookup = ("Pickle", 3243921299984)

gen = ("Pickle", 3243927593488)

polt = ("Pickle", 3243947836816)

prod = ("Pickle", 3243947842704)

sex = ("Pickle", 3243910623568)

input_ = ("Interface", ("..", "Input"), "auto")

return_array = True