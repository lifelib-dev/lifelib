"""Projection Assumptions


This Space associates projection assumptions to model points,
by looking up paramters in a table stored as an `ExcelRange`_ object
associated to a Reference named :attr:`Assumption`.

.. _PandasData:
   https://docs.modelx.io/en/latest/reference/dataclient.html#pandasdata

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange


.. rubric:: References

Attributes:
    Assumption: `ExcelRange`_ object for associating
        assumption identifiers to model point keys
    AssumptionTables: `ExcelRange`_ object holding assumption tables
        such as surrender rates and mortality factors
    PolicyData: `PandasData`_ object holding model point data as a pandas
        DataFrame read from the model point file
    TableLastAge: Reference to :func:`fastlife.model.Input.TableLastAge`
    prod: Reference to :func:`fastlife.Projection.Policy.Product`
    polt: Reference to :func:`fastlife.Projection.Policy.PolicyType`
    gen: Reference to :func:`fastlife.Projection.Policy.Gen`
    sex: Reference to :func:`fastlife.Projection.Policy.Sex`

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
        result = _space.AsmpLookup.match("CommInitPrem", key1, key2, key2).value

        if result is not None:
            return result
        else:
            raise ValueError('CommInitPrem not found')

    return PolicyData().apply(get_table_id, axis=1)


def CommRenPrem():
    """Renewal commission per premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        result = _space.AsmpLookup.match("CommRenPrem", key1, key2, key2).value

        if result is not None:
            return result
        else:
            raise ValueError('CommRenPrem not found')

    return PolicyData().apply(get_table_id, axis=1)


def CommRenTerm():
    """Renewal commission term"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        result = _space.AsmpLookup.match("CommRenTerm", key1, key2, key2).value

        if result is not None:
            return result
        else:
            raise ValueError('CommRenTerm not found')

    return PolicyData().apply(get_table_id, axis=1)


def ExpsAcqAnnPrem():
    """Acquisition expense per annualized premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("ExpsAcqAnnPrem", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsAcqPol():
    """Acquisition expense per policy"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("ExpsAcqPol", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsAcqSA():
    """Acquisition expense per sum assured"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("ExpsAcqSA", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsMaintAnnPrem():
    """Maintenance expense per annualized premium"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("ExpsMaintPrem", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsMaintPol():
    """Maintenance expense per policy"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("ExpsMaintPol", key1, key2, key2).value

    return PolicyData().apply(get_table_id, axis=1)


def ExpsMaintSA():
    """Maintenance expense per sum assured"""


    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("ExpsMaintSA", key1, key2, key2).value

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

    fac = MortFactorID().apply(lambda facid: AssumptionTables.get((facid, y), np.nan))

    if y == 0 or not fac.isnull().any():
        return fac
    else:
        return fac.mask(fac.isnull(), MortFactor(y-1))


def SurrRate(y):
    """Surrender Rate"""

    fac = SurrRateID().apply(lambda surrid: AssumptionTables.get((surrid, y), np.nan))

    if y == 0 or not fac.isnull().any():
        return fac
    else:
        return fac.mask(fac.isnull(), SurrRate(y-1))


def MortTableID():
    """Mortality Table"""

    def get_table_id(pol):
        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        return _space.AsmpLookup.match("BaseMort", key1, key2, key2).value

    result = PolicyData().apply(get_table_id, axis=1)
    result.name = 'MortTableID'

    return result


def MortFactorID():
    """Mortality factor"""

    def get_factor(pol):

        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        table = _space.AsmpLookup.match("MortFactor", key1, key2, key2).value

        if table is None:
            raise ValueError('MortFactor not found')

        return table

    return PolicyData().apply(lambda pol: get_factor(pol), axis=1)


def SurrRateID():

    def get_factor(pol):

        key1, key2, key3 = pol['Product'], pol['PolicyType'], pol['Gen']
        table = _space.AsmpLookup.match("Surrender", key1, key2, key2).value

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