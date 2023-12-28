"""Policy attributes and policy values

This Space is a child Space of :mod:`~nestedlife.model.OuterProj`.
A child Space derived from this Space is created under each
:mod:`~nestedlife.model.OuterProj` ItemSpace,
such as ``nestedlife.OuterProj[1].Policy``,
which holds policy attributes and policy values for Policy 1.
The Space is used by :mod:`~nestedlife.model.BaseProj.Assumptions`
and :mod:`~nestedlife.model.OuterProj.InnerProj`.

Some Cells in this Space, such as :func:`Product` and :func:`IssueAge`,
are for retrieving attributes for the selected policy from :attr:`PolicyData`.
Some other Cells, such as :func:`GrossPremRate` are for
calculating policy values for the policy from the attributes and
product specs looked up through :attr:`SpecLookup`.


.. figure:: /images/projects/nestedlife/model/Policy/diagram1.png


.. rubric:: Parameters

Since :mod:`~nestedlife.model.OuterProj` is parameterized with
:attr:`PolicyID` and :attr:`ScenID`, this Space is also
parameterized as a child space of :mod:`~nestedlife.model.OuterProj`.
For example, ``nestedlife.Projection[1].Policy.GrossPremRate()``
represents the gross premium rate for Policy 1.

Attributes:
    PolicyID(:obj:`int`): Policy ID
    ScenID(:obj:`int`, optional): Scenario ID, defaults to 1.


.. rubric:: References

Attributes:
    LifeTable: :mod:`~nestedlife.model.LifeTable` Space
    PolicyData: `ExcelRange`_ object holding data read from the
        Excel range *PolicyData* in *input.xlsx*.
    SpecLookup: :func:`~nestedlife.model.Input.SpecLookup`
    PremTerm: Alias for :func:`PolicyTerm`

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

def AnnPremRate():
    """Annualized Premium Rate per Sum Assured"""
    return GrossPremRate() * (1/10 if PremFreq() == 0 else PremFreq())


def CashValueRate(t):
    """Cash Value Rate per Sum Assured"""
    return max(ReserveNLP_Rate('PREM', t) - SurrCharge(t), 0)


def GrossPremRate():
    """Gross Premium Rate per Sum Assured per payment"""

    alpha = LoadAcqSA()
    beta = LoadMaintPrem()
    gamma = LoadMaintSA()
    gamma2 = LoadMaintSA2()
    delta = LoadMaintPremWaiverPrem()

    x, n, m = IssueAge(), PolicyTerm(), PremTerm()

    comf = LifeTable[Sex(), IntRate('PREM'), TableID('PREM')]

    if Product() == 'TERM' or Product() == 'WL':
        return (comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, PremFreq())
                + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / PremFreq() / comf.AnnDuenx(x, m, PremFreq())

    elif Product() == 'ENDW':
        return (comf.Exn(x, n) + comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, PremFreq())
                + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / PremFreq() / comf.AnnDuenx(x, m, PremFreq())
    else:
        raise ValueError('invalid product')


def GrossPremTable():
    """Gross premium table"""
    return None


def InitSurrCharge():
    """Initial Surrender Charge Rate"""

    param1 = _space.SpecLookup.match("SurrChargeParam1", Product(), PolicyType(), Gen()).value
    param2 = _space.SpecLookup.match("SurrChargeParam2", Product(), PolicyType(), Gen()).value

    if param1 is None or param2 is None:
        raise ValueError('SurrChargeParam not found')

    return param1 + param2 * min(PolicyTerm() / 10, 1)


def IntRate(RateBasis):
    """Interest Rate"""

    if RateBasis == 'PREM':
        basis = 'IntRatePrem'
    elif RateBasis == 'VAL':
        basis = 'IntRateVal'
    else:
        raise ValueError('invalid RateBasis')

    result = _space.SpecLookup.match(basis, Product(), PolicyType(), Gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('invalid RateBais')


def LoadAcqSA():
    """Acquisition Loading per Sum Assured"""
    param1 = SpecLookup("LoadAcqSAParam1", Product())
    param2 = SpecLookup("LoadAcqSAParam2", Product())

    return param1 + param2 * min(PolicyTerm() / 10, 1)


def LoadMaintPrem():
    """Maintenance Loading per Gross Premium"""

    if SpecLookup("LoadMaintPremParam1", Product()) is not None:
        return SpecLookup("LoadMaintPremParam1", Product())

    elif SpecLookup("LoadMaintPremParam2", Product()) is not None:
        param = SpecLookup("LoadMaintPremParam2", Product())
        return (param + min(10, PolicyTerm())) / 100

    else:
        raise ValueError('LoadMaintPrem parameters not found')


def LoadMaintPremWaiverPrem():
    """Maintenance Loading per Gross Premium for Premium Waiver"""

    if PremTerm() < 5:
        return 0.0005
    elif PremTerm() < 10:
        return 0.001
    else:
        return 0.002


def LoadMaintSA():
    """Maintenance Loading per Sum Assured during Premium Payment"""

    result = _space.SpecLookup.match("LoadMaintSA", Product(), PolicyType(), Gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('lookup failed')


def LoadMaintSA2():
    """Maintenance Loading per Sum Assured after Premium Payment"""

    result = _space.SpecLookup.match("LoadMaintSA2", Product(), PolicyType(), Gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('lookup failed')


def NetPremRate(basis):
    """Net Premium Rate"""

    gamma2 = LoadMaintSA2()
    comf = LifeTable[Sex(), IntRate(basis), TableID(basis)]

    x, n, m = IssueAge(), PolicyTerm(), PremTerm()

    if Product() == 'TERM' or Product() == 'WL':
        return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

    elif Product() == 'ENDW':
        return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

    else:
        raise ValueError('invalid product')


def ReserveNLP_Rate(basis, t):
    """Net level premium reserve rate"""

    gamma2 = LoadMaintSA2()

    lt = LifeTable[Sex(), IntRate(basis), TableID(basis)]

    x, n, m = IssueAge(), PolicyTerm(), PremTerm()

    if t <= m:
        return lt.Axn(x+t, n-t) + gamma2 * lt.AnnDuenx(x+t, n-m, 1, m-t) \
                - NetPremRate(basis) * lt.AnnDuenx(x+t, m-t)
    else:
        return lt.Axn(x+t, n-t) + gamma2 * lt.AnnDuenx(x+t, n-m, 1, m-t)


def ReserveRate():
    """Valuation Reserve Rate per Sum Assured"""
    return None


def SurrCharge(t):
    """Surrender Charge Rate per Sum Assured"""
    m = PremTerm()
    return InitSurrCharge() * max((min(m, 10) - t) / min(m, 10), 0)


def TableID(RateBasis):
    """Mortality Table ID"""

    if RateBasis == 'PREM':
        basis = "MortTablePrem"
    elif RateBasis == 'VAL':
        basis = "MortTableVal"
    else:
        raise ValueError('invalid RateBasis')

    result = _space.SpecLookup.match(basis, Product(), PolicyType(), Gen()).value

    if result is not None:
        return result
    else:
        raise ValueError('invalid RateBais')


def UernPremRate():
    """Unearned Premium Rate"""
    return None


Product = lambda: PolicyData[PolicyID, 'Product']

PolicyType = lambda: PolicyData[PolicyID, 'PolicyType']

Gen = lambda: PolicyData[PolicyID, 'Gen']

Channel = lambda: PolicyData[PolicyID, 'Channel']

Sex = lambda: PolicyData[PolicyID, 'Sex']

Duration = lambda: PolicyData[PolicyID, 'Duration']

IssueAge = lambda: PolicyData[PolicyID, 'IssueAge']

PremFreq = lambda: PolicyData[PolicyID, 'PremFreq']

PolicyTerm = lambda: PolicyData[PolicyID, 'PolicyTerm']

PolicyCount = lambda: PolicyData[PolicyID, 'PolicyCount']

SumAssured = lambda: PolicyData[PolicyID, 'SumAssured']

# ---------------------------------------------------------------------------
# References

LifeTable = ("Interface", ("...", "LifeTable"), "auto")

PolicyData = ("IOSpec", 2556818224720, 2556818224720)

PremTerm = ("Interface", (".", "PolicyTerm"), "auto")

SpecLookup = ("Interface", ("...", "Input", "SpecLookup"), "auto")