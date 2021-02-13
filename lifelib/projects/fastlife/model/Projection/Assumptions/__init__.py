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

_allow_none = True

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def CnsmpTax():
    """Consumption tax rate"""
    return AsmpLookup("CnsmpTax")


def CommInitPrem():
    """Initial commission per premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        result = AsmpLookup.match("CommInitPrem", key1, key2, key2).value

        if result is not None:
            return result
        else:
            raise ValueError('CommInitPrem not found')

    return PolicyData().apply(get_table_id, axis=1)


def CommRenPrem():
    """Renewal commission per premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        result = AsmpLookup.match("CommRenPrem", key1, key2, key2).value

        if result is not None:
            return result
        else:
            raise ValueError('CommRenPrem not found')

    return PolicyData().apply(get_table_id, axis=1)


def CommRenTerm():
    """Renewal commission term"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        result = AsmpLookup.match("CommRenTerm", key1, key2, key2).value

        if result is not None:
            return result
        else:
            raise ValueError('CommRenTerm not found')

    return PolicyData().apply(get_table_id, axis=1)


def ExpsAcqAnnPrem():
    """Acquisition expense per annualized premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("ExpsAcqAnnPrem", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsAcqPol():
    """Acquisition expense per policy"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("ExpsAcqPol", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsAcqSA():
    """Acquisition expense per sum assured"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("ExpsAcqSA", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsMaintAnnPrem():
    """Maintenance expense per annualized premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("ExpsMaintPrem", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsMaintPol():
    """Maintenance expense per policy"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("ExpsMaintPol", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsMaintSA():
    """Maintenance expense per sum assured"""


    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("ExpsMaintSA", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def InflRate():
    """Inflation rate"""
    return AsmpLookup("InflRate")


def LastAge():
    """Age at which mortality becomes 1"""

    keys = pd.concat([MortTableID(), sex()], axis=1)

    result = keys.join(TableLastAge(), on=['MortTableID', 'Sex'])['TableLastAge']

    result.name = 'LastAge'

    return result


def MortFactor(y):
    """Mortality factor"""

    fac = MortFactorID().apply(lambda facid: AssumptionTables.get((facid, y), np.NaN))

    if y == 0 or not fac.isnull().any():
        return fac
    else:
        return fac.mask(fac.isnull(), MortFactor(y-1))


def SurrRate(y):
    """Surrender Rate"""

    fac = SurrRateID().apply(lambda surrid: AssumptionTables.get((surrid, y), np.NaN))

    if y == 0 or not fac.isnull().any():
        return fac
    else:
        return fac.mask(fac.isnull(), SurrRate(y-1))


def MortTableID():
    """Mortality Table"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return AsmpLookup.match("BaseMort", key1, key2, key2).value

    result = PolicyData().apply(get_table_id, axis=1)
    result.name = 'MortTableID'

    return result


def MortFactorID():
    """Mortality factor"""

    def get_factor(pol):

        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        table = AsmpLookup.match("MortFactor", key1, key2, key2).value

        if table is None:
            raise ValueError('MortFactor not found')

        return table

    return PolicyData().apply(lambda pol: get_factor(pol), axis=1)


def SurrRateID():

    def get_factor(pol):

        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        table = AsmpLookup.match("Surrender", key1, key2, key2).value

        if table is None:
            raise ValueError('Surrender not found')

        return table

    return PolicyData().apply(lambda pol: get_factor(pol), axis=1)


def AsmpLookup(asmp, prod=None, polt=None, gen=None):
    """Look up assumptions"""
    return Assumption.get((asmp, prod, polt, gen), None)


# ---------------------------------------------------------------------------
# References

Assumption = ("Pickle", 3020548391688)

AssumptionTables = ("Pickle", 3020548383112)

PolicyData = ("Pickle", 3020548337160)

TableLastAge = ("Interface", ("...", "Input", "TableLastAge"), "auto")

gen = ("Interface", ("..", "Policy", "Gen"), "auto")

polt = ("Interface", ("..", "Policy", "PolicyType"), "auto")

prod = ("Interface", ("..", "Policy", "Product"), "auto")

sex = ("Interface", ("..", "Policy", "Sex"), "auto")

MortalityTables = ("Pickle", 3020541952136)