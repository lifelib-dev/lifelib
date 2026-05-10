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

Some Cells in this Space, such as :func:`product` and :func:`issue_age`,
are for retrieving attributes for the selected policy from :attr:`PolicyData`.
Some other Cells, such as :func:`GrossPremRate` are for
calculating policy values for the policy from the attributes and
product specs looked up through :attr:`SpecLookup`.


.. figure:: /images/projects/simplelife/model/Policy/diagram1.png


.. rubric:: Parameters

Since :mod:`~simplelife.model.Projection` is parameterized with
:attr:`idx` and :attr:`scen_id`, this Space is also
parameterized as a child space of :mod:`~simplelife.model.Projection`.
For example, ``simplelife.Projection[1].Policy.GrossPremRate()``
represents the gross premium rate for Policy 1.

Attributes:
    idx(:obj:`int`): Policy ID
    scen_id(:obj:`int`, optional): Scenario ID, defaults to 1.


.. rubric:: References

Attributes:
    life_table: :mod:`~simplelife.model.life_table` Space
    PolicyData: `ExcelRange`_ object holding data read from the
        Excel range *PolicyData* in *input.xlsx*.
    SpecLookup: :func:`~simplelife.model.input_data.SpecLookup`
    prem_term: Alias for :func:`policy_term`

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

def gross_prem_table():
    """Gross premium table"""
    return None


def init_surr_charge():
    """Initial Surrender Charge Rate"""

    param1 = surr_charge_param1()
    param2 = surr_charge_param2()

    return param1 + param2 * np.minimum(policy_term() / 10, 1)


def int_rate(basis):
    """Interest Rate"""

    col = {
        RateBasisID.PREM: 'IntRatePrem',
        RateBasisID.VAL: 'IntRateVal'}.get(basis, None)

    return pandas_to_array(
        map_to_policies(input_data.product_spec(col)))


def load_acq_sa():
    """Acquisition Loading per Sum Assured"""
    param1 = load_acq_sa_param1()
    param2 = load_acq_sa_param2()

    return param1 + param2 * np.minimum(policy_term() / 10, 1)


def load_maint_prem():
    """Maintenance Loading per Gross Premium"""

    param1 = load_maint_prem_param1()
    param2 = load_maint_prem_param2()

    return np.where(np.isnan(param1), (param2 + np.minimum(10, policy_term())) / 100, param1)


def load_maint_prem_waiver_prem():
    """Maintenance Loading per Gross Premium for Premium Waiver"""

    table = input_data.prem_waiver_cost()

    bins = [-np.inf] + list(table.keys())[:-1] + [np.inf]
    vals = list(table.values())

    return pandas_to_array(pd.cut(
         input_data.policy_data()['PolicyTerm'],
         bins=bins,
         labels=vals,
         right=False,        # left-closed: [x, y)
     )) #.astype(float)


def load_maint_sa():
    """Maintenance Loading per Sum Assured during Premium Payment"""

    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadMaintSA')))


def load_maint_sa2():
    """Maintenance Loading per Sum Assured during Premium Payment"""

    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadMaintSA2')))


def reserve_rate():
    """Valuation Reserve Rate per Sum Assured"""
    return None


def table_id(basis):
    """Mortality Table ID"""

    col = {
        RateBasisID.PREM: 'MortTablePrem',
        RateBasisID.VAL: 'MortTableVal'}.get(basis, None)

    return pandas_to_array(
        map_to_policies(input_data.product_spec(col)))


def uern_prem_rate():
    """Unearned Premium Rate"""
    return None


def product():
    # return getattr(ProductID, 'TERM')

    # prod_str_to_int = {
    #     'TERM': ProductID.TERM,
    #     'WL': ProductID.WL,
    #     'ENDW': ProductID.ENDW
    #     }
    return pandas_to_array(input_data.policy_data()['Product'].map(lambda s: getattr(ProductID, s)))


def policy_type():
    return pandas_to_array(input_data.policy_data()['PolType'])


gen = lambda: PolicyData[idx, 'Gen']

channel = lambda: PolicyData[idx, 'Channel']

def sex():

    return pandas_to_array(input_data.policy_data()['Sex'].map(lambda s: getattr(SexID, s)))


duration = lambda: PolicyData[idx, 'Duration']

def issue_age():

    return pandas_to_array(input_data.policy_data()['IssueAge'])


def prem_freq(): 
   return pandas_to_array(input_data.policy_data()['PremFreq'])


def policy_term():

    return pandas_to_array(input_data.policy_data()['PolicyTerm'])


def policy_count():
    return pandas_to_array(input_data.policy_data()['PolicyCount'])


def sum_assured():
    return pandas_to_array(input_data.policy_data()['SumAssured'])


def load_acq_sa_param1():
    # return input_data.product_spec('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadAcqSAParam1')))


def load_acq_sa_param2():
    # return input_data.product_spec('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadAcqSAParam2')))


def load_maint_prem_param1():
    # return input_data.product_spec('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadMaintPremParam1')))


def load_maint_prem_param2():
    # return input_data.product_spec('LoadAcqSAParam2')
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadMaintPremParam2')))


def surr_charge_param1():
    return pandas_to_array(
        map_to_policies(input_data.product_spec('SurrChargeParam1')))


def surr_charge_param2():
    return pandas_to_array(
        map_to_policies(input_data.product_spec('SurrChargeParam2')))


# ---------------------------------------------------------------------------
# References

life_table = ("Interface", ("..", "CommTable"), "auto")

input_data = ("Interface", ("..", "InputData"), "auto")

prem_term = ("Interface", (".", "policy_term"), "auto")

return_array = True