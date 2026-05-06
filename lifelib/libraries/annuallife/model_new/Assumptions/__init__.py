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
:attr:`PolicyID` and :attr:`ScenID`, this Space is also
parameterized as a child space of :mod:`~simplelife.model.Projection`.
For example, ``simplelife.Projection[1].Assumptions.ExpsMaintSA()``
represents the expense maintenance per sum assured for Policy 1.

Attributes:
    PolicyID(:obj:`int`): Policy ID
    ScenID(:obj:`int`, optional): Scenario ID, defaults to 1.

.. rubric:: References

Attributes:
    AssumptionTables: `ExcelRange`_ object holding data read from the
        Excel range *AssumptionTable* in *input.xlsx*.

    MortalityTable: `ExcelRange`_ object holding mortality tables.
        The data is read from *MortalityTables* range in *input.xlsx*.

    prod: Alias for :func:`simplelife.Projection.Policy.Product`
    polt: Alias for :func:`simplelife.Projection.Policy.PolicyType`
    gen: Alias for :func:`simplelife.Projection.Policy.Gen`
    sex: Alias for :func:`simplelife.Projection.Policy.Sex`
    AsmpLookup: Alias for :func:`simplelife.Input.AsmpLookup`

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

def BaseMortRate(x):
    """Bae mortality rate"""

    return _space.AsmpLookup

    table_id = _space.AsmpLookup.match("BaseMort", prod(), polt(), gen()).value
    return MortalityTables[table_id, sex(), x]


def CnsmpTax():
    """Consumption tax rate"""
    # return AsmpLookup("CnsmpTax")
    # return pandas_to_array(map_to_policies(Input.Assumption2('CnsmpTax')))
    return Input.ConstParams()['CnsmpTax']


def CommInitPrem():
    """Initial commission per premium"""
    # result = _space.AsmpLookup.match("CommInitPrem", prod(), polt(), gen()).value

    # if result is not None:
    #     return result
    # else:
    #     raise ValueError('CommInitPrem not found')

    return pandas_to_array(map_to_policies(Input.Assumption2('CommInitPrem')))


def CommRenPrem():
    """Renewal commission per premium"""
    # result = _space.AsmpLookup.match("CommRenPrem", prod(), polt(), gen()).value

    # if result is not None:
    #     return  result
    # else:
    #     raise ValueError('CommRenPrem not found')

    return pandas_to_array(map_to_policies(Input.Assumption2('CommRenPrem')))


def CommRenTerm():
    """Renewal commission term"""
    # result = _space.AsmpLookup.match("CommRenTerm", prod(), polt(), gen()).value

    # if result is not None:
    #     return result
    # else:
    #     raise ValueError('CommRenTerm not found')

    return pandas_to_array(map_to_policies(Input.Assumption2('CommRenTerm')))


def ExpsAcqAnnPrem():
    """Acquisition expense per annualized premium"""
    # return _space.AsmpLookup.match("ExpsAcqAnnPrem", prod(), polt(), gen()).value

    return pandas_to_array(map_to_policies(Input.Assumption2('ExpsAcqAnnPrem')))


def ExpsAcqPol():
    """Acquisition expense per policy"""
    # return _space.AsmpLookup.match("ExpsAcqPol", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(Input.Assumption2('ExpsAcqPol')))


def ExpsAcqSA():
    """Acquisition expense per sum assured"""
    # return _space.AsmpLookup.match("ExpsAcqSA", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(Input.Assumption2('ExpsAcqSA')))


def ExpsMaintAnnPrem():
    """Maintenance expense per annualized premium"""
    # return _space.AsmpLookup.match("ExpsMaintPrem", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(Input.Assumption2('ExpsMaintPrem')))


def ExpsMaintPol():
    """Maintenance expense per policy"""
    # return _space.AsmpLookup.match("ExpsMaintPol", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(Input.Assumption2('ExpsMaintPol')))


def ExpsMaintSA():
    """Maintenance expense per sum assured"""
    # return _space.AsmpLookup.match("ExpsMaintSA", prod(), polt(), gen()).value
    return pandas_to_array(map_to_policies(Input.Assumption2('ExpsMaintSA')))


def InflRate():
    """Inflation rate"""
    # return AsmpLookup("InflRate")
    # return pandas_to_array(map_to_policies(Input.Assumption2('InflRate')))
    return Input.ConstParams()['InflRate']


def MortalityTables():
    """Mortality Table"""

    tables = Input.MortalityTables2()
    # return tables.to_numpy() if return_array else tables
    return pandas_to_array(tables)


def MortTableIndex():
    # s = Input.Assumption2('BaseMort')

    # return s.reindex(pd.MultiIndex.from_frame(
    #     Input.PolicyData2()[s.index.names]))
    return map_to_policies(Input.Assumption2('BaseMort'))


def MortArrayIndex():

    columns = Input.MortalityTables2().columns

    # Get the column positions in Input.MortalityTables for each (MortID, Sex) pair
    return columns.get_indexer(
        pd.MultiIndex.from_arrays([MortTableIndex(), Input.PolicyData2()['Sex']])
    )


def AsmpTables():
    return pandas_to_array(Input.AssumptionTables2())


def MortFactorIndex():


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(Input.AssumptionTables2().columns)}

    indexes = Input.Assumption2('MortFactor').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def LapseRateIndex():


    key_to_idx = {getattr(AsmpID, v): i for i, v in enumerate(Input.AssumptionTables2().columns)}

    indexes = Input.Assumption2('Surrender').map(lambda s: getattr(AsmpID, s)).map(key_to_idx)

    return pandas_to_array(map_to_policies(indexes))


def AsmpTableLen():
    return len(AsmpTables())


# ---------------------------------------------------------------------------
# References

AsmpLookup = ("Pickle", 3243921299984)

gen = ("Pickle", 3243927593488)

polt = ("Pickle", 3243947836816)

prod = ("Pickle", 3243947842704)

sex = ("Pickle", 3243910623568)

Input = ("Interface", ("..", "Input"), "auto")

return_array = True