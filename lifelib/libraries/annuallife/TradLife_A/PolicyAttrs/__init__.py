# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Policy attributes and policy values.

This Space holds policy attributes and policy-level values used by
:mod:`~annuallife.TradLife_A.Projection` and its base spaces.

Some Cells in this Space, such as :func:`product` and :func:`issue_age`,
retrieve attributes for the model points from
:func:`~annuallife.TradLife_A.InputData.policy_data`. Other Cells,
such as those used by
:func:`~annuallife.TradLife_A.BaseProj.gross_prem_rate`, derive
policy-level values from product specs looked up through
:func:`~annuallife.TradLife_A.InputData.product_spec`.

Most cells return per-policy NumPy arrays whose layout matches the rows
of :func:`~annuallife.TradLife_A.InputData.policy_data`, so callers
index into them with the integer policy index ``idx``.

.. rubric:: References

Attributes:
    input_data: Alias for :mod:`~annuallife.TradLife_A.InputData`.
        Per-policy attributes are read from the ``PolicyData`` range
        in *input.xlsx* via
        :func:`~annuallife.TradLife_A.InputData.policy_data`,
        and product specs from
        :func:`~annuallife.TradLife_A.InputData.product_spec`.
    prem_term: Alias for :func:`policy_term`.
    return_array(:obj:`bool`): When ``True`` (the default), helper
        functions inherited from
        :mod:`~annuallife.TradLife_A.Utilities` return NumPy arrays
        instead of pandas objects.

.. rubric:: Inherited helpers

Inherited from :mod:`~annuallife.TradLife_A.Utilities`:

* :func:`~annuallife.TradLife_A.Utilities.pandas_to_array`
* :func:`~annuallife.TradLife_A.Utilities.map_to_policies`

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
     ))


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
    """Per-policy product type as a :mod:`~annuallife.TradLife_A.Enums.ProductID` code."""
    return pandas_to_array(input_data.policy_data()['Product'].map(lambda s: getattr(ProductID, s)))


def policy_type():
    """Per-policy policy type from the ``PolType`` column of :func:`~annuallife.TradLife_A.InputData.policy_data`."""
    return pandas_to_array(input_data.policy_data()['PolType'])


gen = lambda: PolicyData[idx, 'Gen']

channel = lambda: PolicyData[idx, 'Channel']

def sex():
    """Per-policy sex as a :mod:`~annuallife.TradLife_A.Enums.SexID` code."""
    return pandas_to_array(input_data.policy_data()['Sex'].map(lambda s: getattr(SexID, s)))


duration = lambda: PolicyData[idx, 'Duration']

def issue_age():
    """Per-policy issue age in years."""
    return pandas_to_array(input_data.policy_data()['IssueAge'])


def prem_freq():
   """Per-policy premium payment frequency (number of payments per year)."""
   return pandas_to_array(input_data.policy_data()['PremFreq'])


def policy_term():
    """Per-policy policy term in years."""
    return pandas_to_array(input_data.policy_data()['PolicyTerm'])


def policy_count():
    """Per-policy number of policies in the model point."""
    return pandas_to_array(input_data.policy_data()['PolicyCount'])


def sum_assured():
    """Per-policy sum assured."""
    return pandas_to_array(input_data.policy_data()['SumAssured'])


def load_acq_sa_param1():
    """Per-policy ``LoadAcqSAParam1`` parameter from ``ProductSpecTable``."""
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadAcqSAParam1')))


def load_acq_sa_param2():
    """Per-policy ``LoadAcqSAParam2`` parameter from ``ProductSpecTable``."""
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadAcqSAParam2')))


def load_maint_prem_param1():
    """Per-policy ``LoadMaintPremParam1`` parameter from ``ProductSpecTable``."""
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadMaintPremParam1')))


def load_maint_prem_param2():
    """Per-policy ``LoadMaintPremParam2`` parameter from ``ProductSpecTable``."""
    return pandas_to_array(
        map_to_policies(input_data.product_spec('LoadMaintPremParam2')))


def surr_charge_param1():
    """Per-policy ``SurrChargeParam1`` parameter from ``ProductSpecTable``."""
    return pandas_to_array(
        map_to_policies(input_data.product_spec('SurrChargeParam1')))


def surr_charge_param2():
    """Per-policy ``SurrChargeParam2`` parameter from ``ProductSpecTable``."""
    return pandas_to_array(
        map_to_policies(input_data.product_spec('SurrChargeParam2')))


# ---------------------------------------------------------------------------
# References

input_data = ("Interface", ("..", "InputData"), "auto")

prem_term = ("Interface", (".", "policy_term"), "auto")

return_array = True