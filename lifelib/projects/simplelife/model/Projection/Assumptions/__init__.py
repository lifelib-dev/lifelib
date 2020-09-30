"""Source module to create ``Assumption`` space from.

This module is a source module to create ``Assumption`` space and its
sub spaces from.
The formulas of the cells in the ``Assumption`` space are created from the
functions defined in this module.

The ``Assumption`` space is the base space of the assumption spaces
for individual policies, which are derived from and belong to
the ``Assumption`` space as its dynamic child spaces.

The assumption spaces for individual policies are parametrized by ``PolicyID``.
For example, to get the assumption space of the policy whose ID is 171::

    >> asmp = model.Assumption(171)

The cells in an assumption space for each individual policy retrieve
input data, calculate and hold values of assumptions specific to that policy,
so various spaces in :mod:`Input<simplelife.build_input>` must be accessible
from the ``Assumption`` space.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

.. rubric:: Referred Spaces

The ``Assumption`` space and its sub spaces depend of the following spaces.
See references sections below for aliases to those spaces and their members
that are referenced in the ``Assumption`` spaces.

* :mod:`Policy<simplelife.policy>` its sub spaces
* ``LifeTable`` in :mod:`Input<simplelife.build_input>`
* ``MortalityTables`` in :mod:`Input<simplelife.build_input>`
* ``Assumption`` in :mod:`Input<simplelife.build_input>`

.. rubric:: Space Parameters

Attributes:
    PolicyID: Policy ID

.. rubric:: References in Base

Attributes:
    asmp_tbl: ``AssumptionTables`` space in :mod:`Input<simplelife.build_input>` space
    asmp: ``Assumption`` space in :mod:`Input<simplelife.build_input>` space
    MortalityTables: ``MortalityTables`` space in :mod:`Input<simplelife.build_input>` space

.. rubric:: References in Sub

Attributes:
    pol: Alias to :mod:`Policy[PolicyID]<simplelife.policy>`
    prod: Alias to :attr:`Policy[PolicyID].Product<simplelife.policy.Product>`
    polt: Alias to :attr:`Policy[PolicyID].PolicyType<simplelife.policy.PolicyType>`
    gen: Alias to :attr:`Policy[PolicyID].Gen<simplelife.policy.Gen>`


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

    table_id = AsmpLookup.match("BaseMort", prod(), polt(), gen()).value
    return MortalityTables[table_id, sex(), x]


def CnsmpTax():
    """Consumption tax rate"""
    return AsmpLookup("CnsmpTax")


def CommInitPrem():
    """Initial commission per premium"""
    result = AsmpLookup.match("CommInitPrem", prod(), polt(), gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('CommInitPrem not found')


def CommRenPrem():
    """Renewal commission per premium"""
    result = AsmpLookup.match("CommRenPrem", prod(), polt(), gen()).value

    if result is not None:
        return  result
    else:
        raise ValueError('CommRenPrem not found')


def CommRenTerm():
    """Renewal commission term"""
    result = AsmpLookup.match("CommRenTerm", prod(), polt(), gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('CommRenTerm not found')


def ExpsAcqAnnPrem():
    """Acquisition expense per annualized premium"""
    return AsmpLookup.match("ExpsAcqAnnPrem", prod(), polt(), gen()).value


def ExpsAcqPol():
    """Acquisition expense per policy"""
    return AsmpLookup.match("ExpsAcqPol", prod(), polt(), gen()).value


def ExpsAcqSA():
    """Acquisition expense per sum assured"""
    return AsmpLookup.match("ExpsAcqSA", prod(), polt(), gen()).value


def ExpsMaintAnnPrem():
    """Maintenance expense per annualized premium"""
    return AsmpLookup.match("ExpsMaintPrem", prod(), polt(), gen()).value


def ExpsMaintPol():
    """Maintenance expense per policy"""
    return AsmpLookup.match("ExpsMaintPol", prod(), polt(), gen()).value


def ExpsMaintSA():
    """Maintenance expense per sum assured"""
    return AsmpLookup.match("ExpsMaintSA", prod(), polt(), gen()).value


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
    table = AsmpLookup.match("MortFactor", prod(), polt(), gen()).value

    if table is None:
        raise ValueError('MortFactor not found')

    result = AssumptionTables.get((table, y), None)

    if result is None:
        return MortFactor(y-1)
    else:
        return result


def MortTable():
    """Mortality Table"""
    result = AsmpLookup.match("BaseMort", prod(), polt(), gen()).value

    if result is not None:
        return MortalityTables(result).MortalityTable
    else:
        raise ValueError('MortTable not found')


def SurrRate(y):
    """Surrender Rate"""
    table = AsmpLookup.match("Surrender", prod(), polt(), gen()).value

    if table is None:
        raise ValueError('Surrender not found')

    result =  AssumptionTables.get((table, y), None)

    if result is None:
        return SurrRate(y-1)
    else:
        return result


# ---------------------------------------------------------------------------
# References

AsmpLookup = ("Interface", ("...", "Input", "AsmpLookup"), "auto")

AssumptionTables = ("Pickle", 1889862980512)

MortalityTables = ("Pickle", 1889853839344)

gen = ("Interface", ("..", "Policy", "Gen"), "auto")

polt = ("Interface", ("..", "Policy", "PolicyType"), "auto")

prod = ("Interface", ("..", "Policy", "Product"), "auto")

sex = ("Interface", ("..", "Policy", "Sex"), "auto")