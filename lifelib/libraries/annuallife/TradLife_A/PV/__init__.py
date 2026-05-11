# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Present Value mix-in Space

This Space serves as a base Space for
:mod:`~annuallife.TradLife_A.Projection`,
and it contains Cells that take the present value of projected
cashflows produced by :mod:`~annuallife.TradLife_A.BaseProj`.

Each present-value cell is defined recursively in ``t``: the recursion
terminates at ``t > proj_len()`` by returning ``0``, where
:func:`~annuallife.TradLife_A.BaseProj.proj_len` is the projection
length for the selected policy. Discounting uses the
:func:`~annuallife.TradLife_A.BaseProj.disc_rate_mth` cell that resolves
to :func:`~annuallife.TradLife_A.Economic.disc_rate_mth` for the
selected scenario.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def interest_net_cf(t):
    """Interest accreted on pv of net cashflows"""
    if t > proj_len():
        return 0
    else:
        return (pv_net_cf(t)
                - premiums(t)
                + expenses(t)) * disc_rate_mth(t)


def pv_claims_death(t):
    """Present value of death benefits"""
    if t > proj_len():
        return 0
    else:
        return (-claims_death(t) + pv_claims_death(t+1)) / (1 + disc_rate_mth(t))


def pv_claims_mat(t):
    """Present value of maturity benefits"""
    if t > proj_len():
        return 0
    else:
        return (-claims_mat(t) + pv_claims_mat(t+1)) / (1 + disc_rate_mth(t))


def pv_claims_surr(t):
    """Present value of surrender benefits"""
    if t > proj_len():
        return 0
    else:
        return (-claims_surr(t) + pv_claims_surr(t+1)) / (1 + disc_rate_mth(t))


def pv_claims(t):
    """Present value of total benefits"""
    if t > proj_len():
        return 0
    else:
        return (-claims(t) + pv_claims(t+1)) / (1 + disc_rate_mth(t))


def pv_check(t):
    """Difference between :func:`pv_net_cf` and :func:`pv_net_cf_for_check`.

    Used as a numerical sanity check; should be zero (within floating
    point error) at every ``t``.
    """
    return pv_net_cf(t) - pv_net_cf_for_check(t)


def pv_exps_acq(t):
    """Present value of acquisition expenses"""
    if t > proj_len():
        return 0
    else:
        return - exps_acq(t) + pv_exps_acq(t+1) / (1 + disc_rate_mth(t))


def pv_commissions(t):
    """Present value of commission expenses"""
    if t > proj_len():
        return 0
    else:
        return - commissions(t) + pv_commissions(t+1) / (1 + disc_rate_mth(t))


def pv_exps_maint(t):
    """Present value of maintenance expenses"""
    if t > proj_len():
        return 0
    else:
        return - exps_maint(t) + pv_exps_maint(t+1) / (1 + disc_rate_mth(t))


def pv_expenses(t):
    """Present value of total expenses"""
    if t > proj_len():
        return 0
    else:
        return - expenses(t) + pv_expenses(t+1) / (1 + disc_rate_mth(t))


def pv_net_cf(t):
    """Present value of net cashflow"""
    return (pv_premiums(t)
            + pv_expenses(t)
            + pv_claims(t))


def pv_net_cf_for_check(t):
    """Present value of net cashflow computed recursively for validation.

    An alternative recursive definition of :func:`pv_net_cf` used by
    :func:`pv_check` to verify that the closed-form sum and the
    recursion agree.
    """
    if t > proj_len():
        return 0
    else:
        return (premiums(t)
                - expenses(t)
                - claims(t) / (1 + disc_rate_mth(t))
                + pv_net_cf(t+1) / (1 + disc_rate_mth(t)))


def pv_premiums(t):
    """Present value of premium income"""
    if t > proj_len():
        return 0
    else:
        return premiums(t) + pv_premiums(t+1) / (1 + disc_rate_mth(t))


def pv_sum_insur_if(t):
    """Present value of insurance in-force"""
    if t > proj_len():
        return 0
    else:
        return insur_if_beg1(t) + pv_sum_insur_if(t+1) / (1 + disc_rate_mth(t))


