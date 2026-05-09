# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Policy attributes and policy values

This Space is a child Space of :mod:`~simplelife.model.Projection`,
and it holds policy attributes and policy values used
by :mod:`~simplelife.model.Projection`
and by :mod:`~simplelife.model.Projection.Assumptions`, another child Space
of :mod:`~simplelife.model.Projection`.

Some Cells in this Space, such as :func:`Product` and :func:`IssueAge`,
are for retrieving attributes for the selected policy from :attr:`PolicyData`.
Some other Cells, such as :func:`GrossPremRate` are for
calculating policy values for the policy from the attributes and
product specs looked up through :attr:`SpecLookup`.


.. figure:: /images/projects/simplelife/model/Policy/diagram1.png


.. rubric:: Parameters

Since :mod:`~simplelife.model.Projection` is parameterized with
:attr:`PolicyID` and :attr:`ScenID`, this Space is also
parameterized as a child space of :mod:`~simplelife.model.Projection`.
For example, ``simplelife.Projection[1].Policy.GrossPremRate()``
represents the gross premium rate for Policy 1.

Attributes:
    PolicyID(:obj:`int`): Policy ID
    ScenID(:obj:`int`, optional): Scenario ID, defaults to 1.


.. rubric:: References

Attributes:
    LifeTable: :mod:`~simplelife.model.LifeTable` Space
    PolicyData: `ExcelRange`_ object holding data read from the
        Excel range *PolicyData* in *input.xlsx*.
    SpecLookup: :func:`~simplelife.model.Input.SpecLookup`
    PremTerm: Alias for :func:`PolicyTerm`

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = [
    ".Utilities"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def GrossPremTable():
    """Gross premium table"""
    return None


def InitSurrCharge():
    """Initial Surrender Charge Rate"""

    # param1 = _space.SpecLookup.match("SurrChargeParam1", Product(), PolicyType(), Gen()).value
    # param2 = _space.SpecLookup.match("SurrChargeParam2", Product(), PolicyType(), Gen()).value

    # if param1 is None or param2 is None:
    #     raise ValueError('SurrChargeParam not found')

    param1 = SurrChargeParam1()
    param2 = SurrChargeParam2()

    return param1 + param2 * np.minimum(PolicyTerm() / 10, 1)


def IntRate(basis):
    """Interest Rate"""

    col = {
        RateBasisID.PREM: 'IntRatePrem',
        RateBasisID.VAL: 'IntRateVal'}.get(basis, None)

    return pandas_to_array(
        map_to_policies(Input.ProductSpec2(col)))


def LoadAcqSA():
    """Acquisition Loading per Sum Assured"""
    param1 = LoadAcqSAParam1()
    param2 = LoadAcqSAParam2()

    return param1 + param2 * np.minimum(PolicyTerm() / 10, 1)


def LoadMaintPrem():
    """Maintenance Loading per Gross Premium"""

    param1 = LoadMaintPremParam1()
    param2 = LoadMaintPremParam2()

    return np.where(np.isnan(param1), (param2 + np.minimum(10, PolicyTerm())) / 100, param1)


def LoadMaintPremWaiverPrem():
    """Maintenance Loading per Gross Premium for Premium Waiver"""

    # if PremTerm() < 5:
    #     return 0.0005
    # elif PremTerm() < 10:
    #     return 0.001
    # else:
    #     return 0.002

    table = Input.PremWaiverCost2()

    bins = [-np.inf] + list(table.keys())[:-1] + [np.inf]
    vals = list(table.values())

    return pandas_to_array(pd.cut(
         Input.PolicyData2()['PolicyTerm'],
         bins=bins,
         labels=vals,
         right=False,        # left-closed: [x, y)
     )) #.astype(float)


def LoadMaintSA():
    """Maintenance Loading per Sum Assured during Premium Payment"""

    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('LoadMaintSA')))


def LoadMaintSA2():
    """Maintenance Loading per Sum Assured during Premium Payment"""

    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('LoadMaintSA2')))


def ReserveRate():
    """Valuation Reserve Rate per Sum Assured"""
    return None


def TableID(basis):
    """Mortality Table ID"""

    # if RateBasis == 'PREM':
    #     basis = "MortTablePrem"
    # elif RateBasis == 'VAL':
    #     basis = "MortTableVal"
    # else:
    #     raise ValueError('invalid RateBasis')

    # result = _space.SpecLookup.match(basis, Product(), PolicyType(), Gen()).value

    # if result is not None:
    #     return result
    # else:
    #     raise ValueError('invalid RateBais')

    col = {
        RateBasisID.PREM: 'MortTablePrem',
        RateBasisID.VAL: 'MortTableVal'}.get(basis, None)

    return pandas_to_array(
        map_to_policies(Input.ProductSpec2(col)))


def UernPremRate():
    """Unearned Premium Rate"""
    return None


def Product():
    # return getattr(ProductID, 'TERM')

    # prod_str_to_int = {
    #     'TERM': ProductID.TERM,
    #     'WL': ProductID.WL,
    #     'ENDW': ProductID.ENDW
    #     }
    return pandas_to_array(Input.PolicyData2()['Product'].map(lambda s: getattr(ProductID, s)))


def PolicyType():
    return pandas_to_array(Input.PolicyData2()['PolType'])


Gen = lambda: PolicyData[PolicyID, 'Gen']

Channel = lambda: PolicyData[PolicyID, 'Channel']

def Sex():

    return pandas_to_array(Input.PolicyData2()['Sex'].map(lambda s: getattr(SexID, s)))


Duration = lambda: PolicyData[PolicyID, 'Duration']

def IssueAge():

    return pandas_to_array(Input.PolicyData2()['IssueAge'])


def PremFreq(): 
   return pandas_to_array(Input.PolicyData2()['PremFreq'])


def PolicyTerm():

    return pandas_to_array(Input.PolicyData2()['PolicyTerm'])


def PolicyCount():
    return pandas_to_array(Input.PolicyData2()['PolicyCount'])


def SumAssured():
    return pandas_to_array(Input.PolicyData2()['SumAssured'])


def LoadAcqSAParam1():
    # return Input.ProductSpec2('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('LoadAcqSAParam1')))


def LoadAcqSAParam2():
    # return Input.ProductSpec2('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('LoadAcqSAParam2')))


def LoadMaintPremParam1():
    # return Input.ProductSpec2('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('LoadMaintPremParam1')))


def LoadMaintPremParam2():
    # return Input.ProductSpec2('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('LoadMaintPremParam2')))


def SurrChargeParam1():
    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('SurrChargeParam1')))


def SurrChargeParam2():
    return pandas_to_array(
        map_to_policies(Input.ProductSpec2('SurrChargeParam2')))


# ---------------------------------------------------------------------------
# References

LifeTable = ("Interface", ("..", "CommTable"), "auto")

Input = ("Interface", ("..", "Input"), "auto")

PremTerm = ("Interface", (".", "PolicyTerm"), "auto")

return_array = True