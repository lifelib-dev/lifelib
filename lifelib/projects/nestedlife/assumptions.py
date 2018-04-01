"""Source module to create ``Assumptions`` space from.

This module is a source module to create ``Assumptions`` space and its
sub spaces from.
The formulas of the cells in the ``Assumptions`` space are created from the
functions defined in this module.

The ``Assumptions`` space is the base space of the assumption spaces
for individual policies, which are derived from and belong to
the ``Assumptions`` space as its dynamic child spaces.

The assumption spaces for individual policies are parametrized by ``PolicyID``.
For example, to get the assumption space of the policy whose ID is 171::

    >> asmp = model.Assumptions(171)

The cells in an assumption space for each individual policy retrieve
input data, calculate and hold values of assumptions specific to that policy,
so various spaces in :mod:`Input<simplelife.build_input>` must be accessible
from the ``Assumptions`` space.

.. rubric:: Project Templates

This module is included in the following project templates.

* :mod:`simplelife`
* :mod:`nestedlife`

.. rubric:: Referred Spaces

The ``Assumptions`` space and its sub spaces depend of the following spaces.
See references sections below for aliases to those spaces and their members
that are referenced in the ``Assumptions`` spaces.

* :mod:`Policy<simplelife.policy>` its sub spaces
* ``LifeTable`` in :mod:`Input<simplelife.build_input>`
* ``MortalityTables`` in :mod:`Input<simplelife.build_input>`
* ``Assumptions`` in :mod:`Input<simplelife.build_input>`

.. rubric:: Space Parameters

Attributes:
    PolicyID: Policy ID

.. rubric:: References in Base

Attributes:
    asmp_tbl: ``AssumptionTables`` space in :mod:`Input<simplelife.build_input>` space
    asmp: ``Assumptions`` space in :mod:`Input<simplelife.build_input>` space
    MortalityTables: ``MortalityTables`` space in :mod:`Input<simplelife.build_input>` space

.. rubric:: References in Sub

Attributes:
    pol: Alias to :mod:`Policy[PolicyID]<simplelife.policy>`
    prd: Alias to :attr:`Policy[PolicyID].Product<simplelife.policy.Product>`
    polt: Alias to :attr:`Policy[PolicyID].PolicyType<simplelife.policy.PolicyType>`
    gen: Alias to :attr:`Policy[PolicyID].Gen<simplelife.policy.Gen>`



"""

policy_attrs = []

# #--- Mortality ---

def MortTable():
    """Mortality Table"""
    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.BaseMort.match(prd, polt, gen).value

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
    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    table = asmp.MortFactor.match(prd, polt, gen).value

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
    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    table = asmp.Surrender.match(prd, polt, gen).value

    if table is None:
        raise ValueError('Surrender not found')

    result =  asmp_tbl.cells[table](y)

    if result is None:
        return SurrRate(y - 1)
    else:
        return result

# --- Commissions ---
def CmsnInitPrem():
    """Initial commission per premium"""

    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.CmsnInitPrem.match(prd, polt, gen).value

    if result is not None:
        return result
    else:
        raise ValueError('CmsnInitPrem not found')


def CmsnRenPrem():
    """Renewal commission per premium"""

    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.CmsnRenPrem.match(prd, polt, gen).value

    if result is not None:
        return  result
    else:
        raise ValueError('CmsnRenPrem not found')

def CmsnRenTerm():
    """Renewal commission term"""

    prd, polt, gen = pol.Product, pol.PolicyType, pol.Gen
    result = asmp.CmsnRenTerm.match(prd, polt, gen).value

    if result is not None:
        return result
    else:
        raise ValueError('CmsnRenTerm not found')

# # --- Expenses ---
def ExpsAcqSA():
    """Acquisition expense per sum assured"""
    return asmp.ExpsAcqSA.match(prd, polt, gen).value

def ExpsAcqAP():
    """Acquisition expense per annualized premium"""
    return asmp.ExpsAcqAP.match(prd, polt, gen).value

def ExpsAcqPol():
    """Acquisition expense per policy"""
    return asmp.ExpsAcqPol.match(prd, polt, gen).value

def ExpsMaintSA():
    """Maintenance expense per sum assured"""
    return asmp.ExpsAcqSA.match(prd, polt, gen).value

def ExpsMaintAP():
    """Maintenance expense per annualized premium"""
    return asmp.ExpsMaintGP.match(prd, polt, gen).value

def ExpsMaintPol():
    """Maintenance expense per policy"""
    return asmp.ExpsMaintPol.match(prd, polt, gen).value

def CnsmpTax():
    """Consumption tax rate"""
    return asmp.CnsmpTax()

def InflRate():
    """Inflation rate"""
    return asmp.InflRate()




    
    












