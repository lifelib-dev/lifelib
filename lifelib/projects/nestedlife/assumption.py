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

policy_attrs = []

# #--- Mortality ---

def MortTable():
    """Mortality Table"""
    result = asmp.BaseMort.match(prod, polt, gen).value

    if result is not None:
        return MortalityTables(result).MortalityTable
    else:
        raise ValueError('MortTable not found')


def LastAge():
    """Age at which mortality becomes 1"""
    x = 0
    while True:
        if BaseMortRate(x) == 1:
            return x
        x += 1
            

def BaseMortRate(x):
    """Bae mortality rate"""
    return MortTable()(pol.Sex, x)


def MortFactor(y):
    """Mortality factor"""
    table = asmp.MortFactor.match(prod, polt, gen).value

    if table is None:
        raise ValueError('MortFactor not found')

    result = asmp_tbl.cells[table](y)

    if result is None:
        return MortFactor(y - 1)
    else:
        return result

# --- Surrender Rates ---
def SurrRate(y):
    """Surrender Rate"""
    table = asmp.Surrender.match(prod, polt, gen).value

    if table is None:
        raise ValueError('Surrender not found')

    result =  asmp_tbl.cells[table](y)

    if result is None:
        return SurrRate(y - 1)
    else:
        return result

# --- Commissions ---
def CommInitPrem():
    """Initial commission per premium"""
    result = asmp.CommInitPrem.match(prod, polt, gen).value

    if result is not None:
        return result
    else:
        raise ValueError('CommInitPrem not found')


def CommRenPrem():
    """Renewal commission per premium"""
    result = asmp.CommRenPrem.match(prod, polt, gen).value

    if result is not None:
        return  result
    else:
        raise ValueError('CommRenPrem not found')

def CommRenTerm():
    """Renewal commission term"""
    result = asmp.CommRenTerm.match(prod, polt, gen).value

    if result is not None:
        return result
    else:
        raise ValueError('CommRenTerm not found')

# # --- Expenses ---
def ExpsAcqSA():
    """Acquisition expense per sum assured"""
    return asmp.ExpsAcqSA.match(prod, polt, gen).value

def ExpsAcqAnnPrem():
    """Acquisition expense per annualized premium"""
    return asmp.ExpsAcqAnnPrem.match(prod, polt, gen).value

def ExpsAcqPol():
    """Acquisition expense per policy"""
    return asmp.ExpsAcqPol.match(prod, polt, gen).value

def ExpsMaintSA():
    """Maintenance expense per sum assured"""
    return asmp.ExpsMaintSA.match(prod, polt, gen).value

def ExpsMaintAnnPrem():
    """Maintenance expense per annualized premium"""
    return asmp.ExpsMaintPrem.match(prod, polt, gen).value

def ExpsMaintPol():
    """Maintenance expense per policy"""
    return asmp.ExpsMaintPol.match(prod, polt, gen).value

def CnsmpTax():
    """Consumption tax rate"""
    return asmp.CnsmpTax()

def InflRate():
    """Inflation rate"""
    return asmp.InflRate()




    
    












