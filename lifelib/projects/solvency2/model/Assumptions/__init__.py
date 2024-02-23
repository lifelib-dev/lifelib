"""Assumption input and calculations for individual policies.

This Space holds projection assumptions
for each individual model point.

This Space is parameterized with :attr:`PolicyID`,
and each ItemSpace of this Space is referenced in
the Projection Spaces under the ItemSpace of SCR_life
that has the same PolicyID as the ItemSpace of this Space.

For example ``Assumptions[1]`` is referenced in
``SCR_life(1).Projection(Risk)`` as ``asmp``, where Risk is 'base', 'mort',
'longev',... etc.

.. rubric:: Parameters

Attributes:
    PolicyID(:obj:`int`): Policy ID

.. rubric:: References

Attributes:
    AssumptionTables: `ExcelRange`_ object holding data read from the
        Excel range *AssumptionTable* in *input.xlsx*.

    MortalityTable: `ExcelRange`_ object holding mortality tables.
        The data is read from *MortalityTables* range in *input.xlsx*.

    prod: Alias for :func:`~solvency2.model.Policy.Product`
    polt: Alias for :func:`~solvency2.model.Policy.PolicyType`
    gen: Alias for :func:`~solvency2.model.Policy.Gen`
    sex: Alias for :func:`~solvency2.model.Policy.Sex`
    AsmpLookup: Alias for :func:`~solvency2.model.Input.AsmpLookup`

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

"""

from modelx.serialize.jsonvalues import *

_formula = lambda PolicyID: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def BaseMortRate(x):
    """Bae mortality rate"""

    table_id = _space.AsmpLookup.match("BaseMort", prod(), polt(), gen()).value
    return MortalityTables[table_id, sex(), x]


def CnsmpTax():
    """Consumption tax rate"""
    return AsmpLookup("CnsmpTax")


def CommInitPrem():
    """Initial commission per premium"""
    result = _space.AsmpLookup.match("CommInitPrem", prod(), polt(), gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('CommInitPrem not found')


def CommRenPrem():
    """Renewal commission per premium"""
    result = _space.AsmpLookup.match("CommRenPrem", prod(), polt(), gen()).value

    if result is not None:
        return  result
    else:
        raise ValueError('CommRenPrem not found')


def CommRenTerm():
    """Renewal commission term"""
    result = _space.AsmpLookup.match("CommRenTerm", prod(), polt(), gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('CommRenTerm not found')


def ExpsAcqAnnPrem():
    """Acquisition expense per annualized premium"""
    return _space.AsmpLookup.match("ExpsAcqAnnPrem", prod(), polt(), gen()).value


def ExpsAcqPol():
    """Acquisition expense per policy"""
    return _space.AsmpLookup.match("ExpsAcqPol", prod(), polt(), gen()).value


def ExpsAcqSA():
    """Acquisition expense per sum assured"""
    return _space.AsmpLookup.match("ExpsAcqSA", prod(), polt(), gen()).value


def ExpsMaintAnnPrem():
    """Maintenance expense per annualized premium"""
    return _space.AsmpLookup.match("ExpsMaintPrem", prod(), polt(), gen()).value


def ExpsMaintPol():
    """Maintenance expense per policy"""
    return _space.AsmpLookup.match("ExpsMaintPol", prod(), polt(), gen()).value


def ExpsMaintSA():
    """Maintenance expense per sum assured"""
    return _space.AsmpLookup.match("ExpsMaintSA", prod(), polt(), gen()).value


def InflRate():
    """Inflation rate"""
    return AsmpLookup("InflRate")


def LastAge():
    """Age at which mortality becomes 1"""
    x = 0
    while True:
        if BaseMortRate(x) == 1:
            return x
        x += 1


def MortFactor(y):
    """Mortality factor"""
    table = _space.AsmpLookup.match("MortFactor", prod(), polt(), gen()).value

    if table is None:
        raise ValueError('MortFactor not found')

    result = AssumptionTables.get((table, y), None)

    if result is None:
        return MortFactor(y-1)
    else:
        return result


def MortTable():
    """Mortality Table"""
    result = _space.AsmpLookup.match("BaseMort", prod(), polt(), gen()).value

    if result is not None:
        return MortalityTables(result).MortalityTable
    else:
        raise ValueError('MortTable not found')


def SurrRate(y):
    """Surrender Rate"""
    table = _space.AsmpLookup.match("Surrender", prod(), polt(), gen()).value

    if table is None:
        raise ValueError('Surrender not found')

    result =  AssumptionTables.get((table, y), None)

    if result is None:
        return SurrRate(y-1)
    else:
        return result


Product = lambda: PolicyData[PolicyID, 'Product']

PolicyType = lambda: PolicyData[PolicyID, 'PolicyType']

Gen = lambda: PolicyData[PolicyID, 'Gen']

Sex = lambda: PolicyData[PolicyID, 'Sex']

# ---------------------------------------------------------------------------
# References

AsmpLookup = ("Interface", ("..", "Input", "AsmpLookup"), "auto")

AssumptionTables = ("IOSpec", 1401491065920, 1401491065920)

MortalityTables = ("IOSpec", 1401491066256, 1401491066256)

gen = ("Interface", (".", "Gen"), "auto")

polt = ("Interface", (".", "PolicyType"), "auto")

prod = ("Interface", (".", "Product"), "auto")

sex = ("Interface", (".", "Sex"), "auto")

PolicyData = ("IOSpec", 1401484906208, 1401484906208)