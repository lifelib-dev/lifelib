"""Policy data and attributes

This Space contains policy data and Cells associated with
policy attributes and policy values.

.. rubric:: References

Attributes:
    PolicyData: `PandasData`_ object holding model point data as a pandas
        DataFrame read from the model point file.
    ProductSpec: `ExcelRange`_ object which is a dict like object for associating
        product spec parameters to model point keys.
    LifeTable: Alias for :mod:`~fastlife.model.LifeTable`
    PremTerm: Alias for :func:`PolicyTerm`


.. _PandasData:
   https://docs.modelx.io/en/latest/reference/dataclient.html#pandasdata

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = True

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AnnPremRate():
    """Annualized Premium Rate per Sum Assured"""
    return GrossPremRate() * PremFreq().mask(PremFreq() == 0, other=1/10)


def CashValueRate(t):
    """Cash Value Rate per Sum Assured"""
    return np.maximum(ReserveNLP_Rate('PREM', t) - SurrCharge(t), 0)


def GrossPremRate():
    """Gross Premium Rate per Sum Assured per payment"""

    def get_value(pol):

        prod = pol['Product']
        alpha = pol['LoadAcqSA']
        beta = pol['LoadMaintPrem']
        delta = pol['LoadMaintPrem2']
        gamma = pol['LoadMaintSA']
        gamma2 = pol['LoadMaintSA2']
        freq = pol['PremFreq']

        x, n, m = pol['IssueAge'], pol['PolicyTerm'], pol['PolicyTerm']

        comf = LifeTable[pol['Sex'], pol['IntRate_PREM'], pol['TableID_PREM']]

        if prod == 'TERM' or prod == 'WL':
            return (comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, freq)
                    + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / freq / comf.AnnDuenx(x, m, freq)

        elif prod == 'ENDW':
            return (comf.Exn(x, n) + comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, freq)
                    + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / freq / comf.AnnDuenx(x, m, freq)
        else:
            raise ValueError('invalid product')


    result = PolicyDataExt1().apply(get_value, axis=1)
    result.name = 'GrossPremRate'

    return result


def GrossPremTable():
    """Gross premium table"""
    return None


def InitSurrCharge():
    """Initial Surrender Charge Rate"""

    def get_value(pol):

        prod, polt, gen = pol['Product'], pol['PolicyType'], pol['Gen']
        term = pol['PolicyTerm']

        param1 = _space.SpecLookup.match("SurrChargeParam1", prod, polt, gen).value
        param2 = _space.SpecLookup.match("SurrChargeParam2", prod, polt, gen).value

        if param1 is None or param2 is None:
            raise ValueError('SurrChargeParam not found')

        return param1 + param2 * min(term / 10, 1)


    result = PolicyData().apply(get_value, axis=1)
    result.name = 'InitSurrCharge'

    return result


def IntRate(RateBasis):
    """Interest Rate"""

    if RateBasis == 'PREM':
        basis = 'IntRatePrem'
    elif RateBasis == 'VAL':
        basis = 'IntRateVal'
    else:
        raise ValueError('invalid RateBasis')


    def get_value(pol):

        result = _space.SpecLookup.match(basis,
                                  pol["Product"], 
                                  pol["PolicyType"],
                                  pol["Gen"]).value

        if result is not None:
            return result
        else:
            raise ValueError('lookup failed')


    result = PolicyData().apply(get_value, axis=1)
    result.name = 'IntRate_' + RateBasis
    return result


def LoadAcqSA():
    """Acquisition Loading per Sum Assured"""
    param1 = Product().apply(lambda prod: SpecLookup("LoadAcqSAParam1", prod))
    param2 = Product().apply(lambda prod: SpecLookup("LoadAcqSAParam2", prod))

    result = param1 + param2 * np.minimum(PolicyTerm() / 10, 1)

    result.name = 'LoadAcqSA'
    return result


def LoadMaintPrem():
    """Maintenance Loading per Gross Premium"""

    def get_value(pol):

        if SpecLookup("LoadMaintPremParam1", pol["Product"]) is not None:
            return SpecLookup("LoadMaintPremParam1", pol["Product"])

        elif SpecLookup("LoadMaintPremParam2", pol["Product"]) is not None:
            param = SpecLookup("LoadMaintPremParam2", pol["Product"])
            return (param + min(10, pol["PolicyTerm"])) / 100

        else:
            raise ValueError('LoadMaintPrem parameters not found')


    result = PolicyData().apply(get_value, axis=1)
    result.name = 'LoadMaintPrem'

    return result


def LoadMaintSA():
    """Maintenance Loading per Sum Assured during Premium Payment"""

    def get_value(pol):

        result = _space.SpecLookup.match("LoadMaintSA",
                                  pol["Product"], 
                                  pol["PolicyType"],
                                  pol["Gen"]).value

        if result is not None:
            return result
        else:
            raise ValueError('lookup failed')


    result = PolicyData().apply(get_value, axis=1)
    result.name = 'LoadMaintSA'
    return result


def LoadMaintSA2():
    """Maintenance Loading per Sum Assured after Premium Payment"""

    def get_value(pol):

        result = _space.SpecLookup.match("LoadMaintSA2",
                                  pol["Product"], 
                                  pol["PolicyType"],
                                  pol["Gen"]).value

        if result is not None:
            return result
        else:
            raise ValueError('lookup failed')


    result = PolicyData().apply(get_value, axis=1)
    result.name = 'LoadMaintSA2'
    return result


def NetPremRate(basis):
    """Net Premium Rate"""

    def get_value(pol):

        prod = pol['Product']
        gamma2 = pol['LoadMaintSA2']

        x, n, m = pol['IssueAge'], pol['PolicyTerm'], pol['PolicyTerm']

        comf = LifeTable[pol['Sex'], pol['IntRate_' + basis], pol['TableID_' + basis]]

        if prod == 'TERM' or prod == 'WL':
            return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

        elif prod == 'ENDW':
            return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

        else:
            raise ValueError('invalid product')


    result = PolicyDataExt1().apply(get_value, axis=1)
    result.name = 'NetPremRate_' + basis

    return result


def ReserveNLP_Rate(basis, t):
    """Net level premium reserve rate"""

    def get_value(pol):

        prod = pol['Product']
        gamma2 = pol['LoadMaintSA2']
        netp = pol['NetPremRate_' + basis]

        x, n, m = pol['IssueAge'], pol['PolicyTerm'], pol['PolicyTerm']

        lt = LifeTable[pol['Sex'], pol['IntRate_' + basis], pol['TableID_' + basis]]

        if t <= m:
            return lt.Axn(x+t, n-t) + (gamma2 * lt.AnnDuenx(x+t, n-m, 1, m-t)
                    - netp * lt.AnnDuenx(x+t, m-t))
        elif t <=n:
            return lt.Axn(x+t, n-t) + gamma2 * lt.AnnDuenx(x+t, n-m, 1, m-t)
        else:
            return 0


    result = PolicyDataExt2().apply(get_value, axis=1)
    result.name = 'ReserveNLP_Rate'

    return result


def ReserveRate():
    """Valuation Reserve Rate per Sum Assured"""
    return None


def SurrCharge(t):
    """Surrender Charge Rate per Sum Assured"""
    m = PremTerm()
    return InitSurrCharge() * np.maximum((np.minimum(m, 10) - t) / np.minimum(m, 10), 0)


def TableID(RateBasis):
    """Mortality Table ID"""

    if RateBasis == 'PREM':
        basis = "MortTablePrem"
    elif RateBasis == 'VAL':
        basis = "MortTableVal"
    else:
        raise ValueError('invalid RateBasis')


    def get_value(pol):

        result = _space.SpecLookup.match(basis,
                                  pol["Product"], 
                                  pol["PolicyType"],
                                  pol["Gen"]).value

        if result is not None:
            return result
        else:
            raise ValueError('lookup failed')


    result = PolicyData().apply(get_value, axis=1)
    result.name = 'TableID_' + RateBasis
    return result


def UernPremRate():
    """Unearned Premium Rate"""
    return None


Product = lambda: PolicyData()['Product']

PolicyType = lambda: PolicyData()['PolicyType']

Gen = lambda: PolicyData()['Gen']

Channel = lambda: PolicyData()['Channel']

Sex = lambda: PolicyData()['Sex']

Duration = lambda: PolicyData()['Duration']

IssueAge = lambda: PolicyData()['IssueAge']

PremFreq = lambda: PolicyData()['PremFreq']

PolicyTerm = lambda: PolicyData()['PolicyTerm']

PolicyCount = lambda: PolicyData()['PolicyCount']

SumAssured = lambda: PolicyData()['SumAssured']

def LoadMaintPrem2():
    """Maintenance Loading per Gross Premium for Premium Waiver"""

    result = pd.Series(0.002, index=PolicyData().index)

    result[PremTerm() < 10] = 0.001
    result[PremTerm() < 5] = 0.0005

    result.name = 'LoadMaintPrem2'

    return result


def PolicyDataExt1():
    """Extended Poicy Data"""

    data = pd.concat([PolicyData(), 
                      LoadAcqSA(),
                      LoadMaintPrem(),
                      LoadMaintPrem2(),
                      LoadMaintSA(),
                      LoadMaintSA2(),
                      IntRate('PREM'),
                      TableID('PREM')], axis=1)

    return data


def PolicyDataExt2():
    """Extended Poicy Data"""

    data = pd.concat([PolicyDataExt1(),
                      NetPremRate('PREM')], axis=1)

    return data


def SpecLookup(spec, prod=None, polt=None, gen=None):
    """Look up product specs"""
    return ProductSpec.get((spec, prod, polt, gen), None)


# ---------------------------------------------------------------------------
# References

LifeTable = ("Interface", ("...", "LifeTable"), "auto")

PremTerm = ("Interface", (".", "PolicyTerm"), "auto")

ProductSpec = ("Pickle", 3020542092744)

PolicyData = ("Pickle", 3020548337160)