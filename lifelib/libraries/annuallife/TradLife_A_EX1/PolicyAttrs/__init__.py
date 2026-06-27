# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Policy attributes and policy values.

This Space is :mod:`TradLife_A.PolicyAttrs <annuallife.TradLife_A.PolicyAttrs>` with one addition
for the Solvency II lapse stress; all other Cells are unchanged, see
:mod:`TradLife_A.PolicyAttrs <annuallife.TradLife_A.PolicyAttrs>`.

Cells Summary
-------------

New Cells
^^^^^^^^^

:func:`segment` returns the per-policy lapse-risk segment as a
``LapseScopeID`` code (currently ``RETAIL`` for every policy). It selects
the mass-lapse factor applied by
:func:`~annuallife.TradLife_A_EX1.Projection.InnerProj.pols_lapse_mass`.

.. autosummary::

   ~segment

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
    """Per-policy product type as a :mod:`TradLife_A.Enums.ProductID <annuallife.TradLife_A.Enums.ProductID>` code."""
    return pandas_to_array(input_data.policy_data()['Product'].map(lambda s: getattr(ProductID, s)))


def policy_type():
    """Per-policy policy type from the ``PolType`` column of :func:`TradLife_A.InputData.policy_data <annuallife.TradLife_A.InputData.policy_data>`."""
    return pandas_to_array(input_data.policy_data()['PolType'])


def gen():
    """Per-policy generation (cohort) identifier."""
    return PolicyData[idx, 'Gen']


def channel():
    """Per-policy distribution channel."""
    return PolicyData[idx, 'Channel']


def sex():
    """Per-policy sex as a :mod:`TradLife_A.Enums.SexID <annuallife.TradLife_A.Enums.SexID>` code."""
    return pandas_to_array(input_data.policy_data()['Sex'].map(lambda s: getattr(SexID, s)))


def duration():
    """Per-policy elapsed policy duration in years."""
    return PolicyData[idx, 'Duration']


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


def segment():
    """Per-policy lapse-risk segment as a ``LapseScopeID`` code.

    Returns a 1-D array, one entry per policy, giving the lapse-risk
    segment that selects the mass-lapse factor applied by
    :func:`~annuallife.TradLife_A_EX1.Projection.InnerProj.pols_lapse_mass`.
    Every policy is currently assigned ``LapseScopeID.RETAIL``.
    """
    return pandas_to_array(pd.Series(LapseScopeID.RETAIL, index=input_data.policy_data().index))


# ---------------------------------------------------------------------------
# References

input_data = ("Interface", ("..", "InputData"), "auto")

prem_term = ("Interface", (".", "policy_term"), "auto")

LapseScopeID = ("Interface", ("..", "Enums", "LapseScopeID"), "auto")