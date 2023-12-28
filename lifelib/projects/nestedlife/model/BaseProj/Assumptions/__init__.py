"""Assumption input and calculations for individual policies.

This Space holds the outer or inner projection assumptions
for each individual model point.


.. figure:: /images/projects/nestedlife/model/Assumptions/diagram1.png


.. rubric:: Parameters

This Space is a child Space of :mod:`~nestedlife.model.BaseProj`.
Since :mod:`~nestedlife.model.OuterProj` and its
child Space :mod:`~nestedlife.model.OuterProj.InnerProj` both inherit
:mod:`~nestedlife.model.BaseProj`,
Both :mod:`~nestedlife.model.OuterProj` and
:mod:`~nestedlife.model.OuterProj.InnerProj` inherit this Space
as their child Spaces.

Since :mod:`~nestedlife.model.OuterProj` is parameterized with
:attr:`PolicyID` and :attr:`ScenID`, the ``Assumptions`` Space
derived from this Space is also
parameterized as a child space of :mod:`~nestedlife.model.OuterProj`.
For example, ``nestedlife.Projection[1].Assumptions.ExpsMaintSA()``
represents the assumption of maintenance expense per sum assured for Policy 1
for the outer projection.
:mod:`~nestedlife.model.OuterProj.InnerProj` is parameterized with
``t0``, the time at which the inner projection starts,
so its ``Assumptions`` child Space derived this Space is
also parameterized
as a child space of :mod:`~nestedlife.model.OuterProj.InnerProj`.

Attributes:
    PolicyID(:obj:`int`): Policy ID
    ScenID(:obj:`int`, optional): Scenario ID, defaults to 1.

.. rubric:: References

Attributes:
    AssumptionTables: `ExcelRange`_ object holding data read from the
        Excel range *AssumptionTable* in *input.xlsx*.

    MortalityTable: `ExcelRange`_ object holding mortality tables.
        The data is read from *MortalityTables* range in *input.xlsx*.

    prod: Alias for :func:`nestedlife.Projection.Policy.Product`
    polt: Alias for :func:`nestedlife.Projection.Policy.PolicyType`
    gen: Alias for :func:`nestedlife.Projection.Policy.Gen`
    sex: Alias for :func:`nestedlife.Projection.Policy.Sex`
    AsmpLookup: Alias for :func:`nestedlife.Input.AsmpLookup`

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

"""

from modelx.serialize.jsonvalues import *

_formula = None

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


def SurrRateMult(t):
    """Surrender rate multiple (Default: 1)"""
    if t == 0:
        return 1
    else:
        return SurrRateMult(t-1)


# ---------------------------------------------------------------------------
# References

AsmpLookup = ("Interface", ("...", "Input", "AsmpLookup"), "auto")

AssumptionTables = ("IOSpec", 2556815992400, 2556815992400)

MortalityTables = ("IOSpec", 2556818466448, 2556818466448)