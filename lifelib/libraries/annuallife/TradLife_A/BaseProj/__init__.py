# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Core annual cashflow projection logic for a single traditional life policy.

This Space defines the period-by-period Cells that project policy
decrement, benefits, premiums, commissions, expenses, investment
income, reserves and the resulting net cashflow and profit for one
model point. It is the base Space inherited by
:mod:`~annuallife.TradLife_A.Projection`, which parameterizes these
Cells by policy and scenario.

The following references are defined in this Space and inherited by
:mod:`~annuallife.TradLife_A.Projection`:

* ``pol`` -> :mod:`~annuallife.TradLife_A.PolicyAttrs`
* ``asmp`` -> :mod:`~annuallife.TradLife_A.Assumptions`
* ``scen`` -> :mod:`~annuallife.TradLife_A.Economic`
* ``comm_table`` -> :mod:`~annuallife.TradLife_A.CommTable`

The integer ``idx`` from the enclosing
:mod:`~annuallife.TradLife_A.Projection` ItemSpace is used to index into
the per-policy NumPy arrays returned by ``pol`` and ``asmp``.


Cells Summary
-------------

Projection Parameters
^^^^^^^^^^^^^^^^^^^^^

Parameters that define the scope of the projection for the selected
policy, such as its length and the attained age.

.. autosummary::

   ~proj_len
   ~age
   ~last_mort_age


Assumptions
^^^^^^^^^^^

Cells that retrieve or derive the actuarial and economic assumptions
applied to the selected policy: mortality, lapse, premium and reserve
rates, surrender charge, inflation and discounting.

.. autosummary::

   ~mort_rate
   ~mort_factor
   ~lapse_rate
   ~gross_prem_rate
   ~ann_prem_rate
   ~net_prem_rate
   ~reserve_nlp_rate
   ~cash_value_rate
   ~surr_charge
   ~inflation_factor
   ~disc_rate_mth


Policy Decrement
^^^^^^^^^^^^^^^^

The number of in-force policies and the movements (new business,
death, surrender, maturity and rider exposures) that change it over
the projection. Cells whose names start with ``pols_`` deal with
numbers of policies.

.. autosummary::

   ~pols_if_init
   ~pols_renewal
   ~pols_if_beg
   ~pols_if_beg1
   ~pols_if
   ~pols_if_aft_mat
   ~pols_death
   ~pols_lapse
   ~pols_maturity
   ~pols_annuity
   ~pols_living
   ~pols_acc_death
   ~pols_acc_hosp
   ~pols_sick_hosp
   ~pols_surg
   ~pols_other


Policy Values
^^^^^^^^^^^^^

The sum assured for the selected policy and the insurance in force at
the beginning and the end of the period.

.. autosummary::

   ~sum_assured
   ~insur_if_beg1
   ~insur_if_end


Claims
^^^^^^

Aggregate benefit cashflows by cause, each shown together with its
per-policy amount. Cells whose names start with ``claims_`` represent
benefit cashflows for the period from ``t`` to ``t+1``, and those
ending with ``_pp`` are the corresponding benefit per policy.

.. autosummary::

   ~claims
   ~claims_death
   ~claims_death_pp
   ~claims_mat
   ~claims_mat_pp
   ~claims_surr
   ~claims_surr_pp
   ~claims_ann
   ~claims_ann_pp
   ~claims_acc_dth
   ~claims_acc_dth_pp
   ~claims_acc_hosp
   ~claims_acc_hosp_pp
   ~claims_sick_hosp
   ~claims_sick_hosp_pp
   ~claims_surg
   ~claims_surg_pp
   ~claims_living
   ~claims_living_pp
   ~claims_other
   ~claims_other_pp


Premiums
^^^^^^^^

Premium income with its per-policy and annualized amounts, and the
total income for the period.

.. autosummary::

   ~premiums
   ~premium_pp
   ~ann_prem_pp
   ~income_total


Investment Income
^^^^^^^^^^^^^^^^^

Investment income earned on accumulated funds, with the corresponding
per-policy amount.

.. warning::

   Investment income depends on reserve balances that are not yet
   fully implemented (see the warning in the Reserves subsection);
   the values produced are provisional and subject to change.

.. autosummary::

   ~invst_income
   ~invst_income_pp


Commissions and Expenses
^^^^^^^^^^^^^^^^^^^^^^^^

Acquisition, maintenance and other expense cashflows together with
initial and renewal commissions, each with its per-policy amount.
Cells whose names start with ``exps_`` represent expense cashflows.

.. autosummary::

   ~expenses
   ~exps_acq
   ~exps_acq_total
   ~expense_acq_pp
   ~exps_maint
   ~exps_maint_total
   ~expense_maint_pp
   ~exps_other
   ~exps_other_pp
   ~commissions
   ~commissions_init
   ~commissions_init_pp
   ~commissions_ren
   ~commissions_ren_pp


Reserves
^^^^^^^^

End-of-period reserve balances, their per-policy and after-maturity
components, and the change in reserve over the period.

.. warning::

   Reserve calculations are not yet fully implemented. The
   hospitalization reserve and the unearned premium reserve currently
   return placeholder zeros and are to be implemented.

.. autosummary::

   ~reserve_prem_rsrv_end
   ~reserve_prem_rsrv_end_pp
   ~reserve_prem_rsrv_aft_mat_pp
   ~reserve_uern_prem_end
   ~reserve_uern_prem_end_pp
   ~reserve_uern_prem_aft_mat_pp
   ~reserve_hosp_rsrv_end
   ~reserve_total_end
   ~reserve_total_aft_mat_pp
   ~change_rsrv


Net Cashflows
^^^^^^^^^^^^^

The net liability cashflow and the accumulated cashflows with
interest.

.. autosummary::

   ~net_cf
   ~accum_cf
   ~int_accum_cf


Profits
^^^^^^^

Profit before tax for the period.

.. warning::

   Profit before tax depends on the change in reserves, which is not
   yet fully implemented (see the warning in the Reserves subsection);
   the values produced are provisional and subject to change.

.. autosummary::

   ~profit_bef_tax

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def accum_cf(t):
    """Accumulated cashflows"""
    if t == 0:
        return 0
    else:
        return (accum_cf(t-1)
                + int_accum_cf(t-1)
                + net_cf(t-1))


def age(t):
    """Attained age at time ``t``"""
    return pol.issue_age()[idx] + t


def claims_acc_dth(t):
    """Accidental death benefits"""
    return claims_acc_dth_pp(t) * pols_acc_death(t)


def claims_acc_hosp(t):
    """Accidental hospitalization benefits"""
    return claims_acc_hosp_pp(t) * pols_acc_hosp(t)


def claims_ann(t):
    """Annuity benefits"""
    return claims_ann_pp(t) * pols_annuity(t)


def claims_death(t):
    """Death benefits"""
    return claims_death_pp(t) * pols_death(t)


def claims_living(t):
    """Living benefits"""
    return claims_living_pp(t) * pols_living(t)


def claims_mat(t):
    """Maturity benefits"""
    return claims_mat_pp(t) * pols_maturity(t)


def claims_other(t):
    """Other benefits"""
    return claims_other_pp(t) * pols_other(t)


def claims_sick_hosp(t):
    """Sickness hospitalization benefits"""
    return claims_sick_hosp_pp(t) * pols_sick_hosp(t)


def claims_surg(t):
    """Surgery benefits"""
    return claims_surg_pp(t) * pols_surg(t)


def claims_surr(t):
    """Surrender benefits"""
    return claims_surr_pp(t) * pols_lapse(t)


def claims(t):
    """Total benefits"""
    return (claims_mat(t)
            + claims_death(t)
            + claims_acc_dth(t)
            + claims_surr(t)
            + claims_ann(t)
            + claims_acc_hosp(t)
            + claims_sick_hosp(t)
            + claims_surg(t)
            + claims_living(t)
            + claims_other(t))


def change_rsrv(t):
    """Change in reserve"""
    return reserve_total_end(t+1) - reserve_total_end(t)


def exps_acq(t):
    """Acquisition expenses"""
    return expense_acq_pp(t) * (pols_if_init(t) + pols_renewal(t))


def exps_acq_total(t):
    """Commissions and acquisition expenses"""
    return commissions(t) + exps_acq(t)


def commissions_init(t):
    """Initial commissions"""
    return commissions_init_pp(t) * pols_if_beg1(t)


def commissions_ren(t):
    """Renewal commissions"""
    return commissions_ren_pp(t) * pols_if_beg1(t)


def commissions(t):
    """Commissions Total"""
    return commissions_init(t) + commissions_ren(t)


def exps_maint(t):
    """Maintenance expenses"""
    return expense_maint_pp(t) * pols_if_beg1(t)


def exps_maint_total(t):
    """Total maintenance expenses including other expenses"""
    return exps_maint(t) + exps_other(t)


def exps_other(t):
    """Other expenses"""
    return 0


def expenses(t):
    """Total expenses"""
    return (commissions_init(t)
            + commissions_ren(t)
            + exps_acq(t)
            + exps_maint(t)
            + exps_other(t))


def income_total(t):
    """Income Total"""
    return premiums(t) + invst_income(t)


def insur_if_beg1(t):
    """Insurance in-force: Beginning of period 1"""
    return pols_if_beg1(t) * sum_assured(t)


def insur_if_end(t):
    """Insurance in-force: End of period"""
    return pols_if(t) * sum_assured(t)


def int_accum_cf(t):
    """Interest on accumulated cashflows"""
    return (accum_cf(t)
            + premiums(t)
            - expenses(t)) * disc_rate_mth(t)


def invst_income(t):
    """Investment income"""
    return invst_income_pp(t) * pols_if_beg1(t)


def net_cf(t):
    """Net liability cashflow"""
    return (premiums(t)
            - claims(t)
            - expenses(t))


def pols_acc_death(t):
    """Number of policies: Accidental death"""
    return 0


def pols_acc_hosp(t):
    """Number of policies: Accidental Hospitalization"""
    return 0


def pols_annuity(t):
    """Number of policies: Annuity"""
    return 0


def pols_death(t):
    """Number of policies: Death"""
    return pols_if_beg1(t) * mort_rate(age(t)) * mort_factor(t)


def pols_if_aft_mat(t):
    """Number of policies: After maturity"""
    return pols_if(t) - pols_maturity(t)


def pols_if_beg(t):
    """Number of policies: Beginning of period"""
    return pols_if_aft_mat(t)


def pols_if_beg1(t):
    """Number of policies: Beginning of period 1"""
    return pols_if_beg(t) + pols_renewal(t) + pols_if_init(t)


def pols_if(t):
    """Number of policies: End of period"""
    if t == 0:
        return 0 # pol.policy_count
    else:
        return pols_if_beg1(t-1) - pols_death(t-1) - pols_lapse(t-1)


def pols_living(t):
    """Number of policies: Living benefits"""
    return 0


def pols_maturity(t):
    """Number of policies: Maturity"""
    if t == pol.policy_term()[idx]:
        return pols_if(t)
    else:
        return 0


def pols_if_init(t):
    """Number of policies: New business"""
    return pol.policy_count()[idx] if t == 0 else 0


def pols_other(t):
    """Number of policies: Other benefits"""
    return 0


def pols_renewal(t):
    """Number of policies: Renewal policies"""
    return 0


def pols_sick_hosp(t):
    """Number of policies: Sickness Hospitalization"""
    return 0


def pols_surg(t):
    """Number of policies: Surgery"""
    return 0


def pols_lapse(t):
    """Number of policies: Surrender"""
    return pols_if_beg1(t) * lapse_rate(t)


def premiums(t):
    """Premium income"""
    return premium_pp(t) * pols_if_beg1(t)


def profit_bef_tax(t):
    """Profit before Tax"""

    return (premiums(t)
            + invst_income(t)
            - claims(t)
            - expenses(t)
            - change_rsrv(t))


def reserve_hosp_rsrv_end(t):
    """Hospitalization reserve: End of period"""
    return 0


def reserve_prem_rsrv_end(t):
    """Premium reserve: End of period"""
    return reserve_prem_rsrv_end_pp(t) * pols_if(t)


def reserve_total_end(t):
    """Total reserve: End of period"""
    return (reserve_prem_rsrv_end(t)
            + reserve_uern_prem_end(t)
            + reserve_hosp_rsrv_end(t))


def reserve_uern_prem_end(t):
    """Unearned Premium: End of period"""
    return 0


def ann_prem_pp(t):
    """Annualized premium per policy at time ``t``"""
    return sum_assured(t) * ann_prem_rate()


def claims_acc_dth_pp(t):
    """Accidental death benefit per policy"""
    return 0


def claims_acc_hosp_pp(t):
    """Accidental hospitalization benefit per policy"""
    return 0


def claims_ann_pp(t):
    """Annuity benefit per policy"""
    return 0


def claims_death_pp(t):
    """Death benefit per policy"""
    return sum_assured(t)


def claims_living_pp(t):
    """Living benefit per policy"""
    return 0


def claims_mat_pp(t):
    """Maturity benefit per policy"""
    return 0


def claims_other_pp(t):
    """Other benefit per policy"""
    return 0


def claims_sick_hosp_pp(t):
    """Sickness hospitalization benefit per policy"""
    return 0


def claims_surg_pp(t):
    """Surgery benefit per policy"""
    return 0


def claims_surr_pp(t):
    """Surrender benefit per policy"""
    return sum_assured(t) * (cash_value_rate(t)
                                + cash_value_rate(t+1)) / 2


def expense_acq_pp(t):
    """Acquisition expense per policy at time t"""
    if t == 0:
        return (ann_prem_pp(t) * asmp.exps_acq_ann_prem()[idx]
                + (sum_assured(t) * asmp.exps_acq_sa()[idx] + asmp.exps_acq_pol()[idx])
                * inflation_factor(t) / inflation_factor(0))
    else:
        return 0


def commissions_init_pp(t):
    """Initial commission per policy at time t"""
    if t == 0:
        return premium_pp(t) * asmp.comm_init_prem()[idx] * (1 + asmp.cnsmp_tax())
    else:
        return 0


def commissions_ren_pp(t):
    """Renewal commission per policy at time t"""
    if t == 0:
        return 0
    elif t < asmp.comm_ren_term()[idx]:
        return premium_pp(t) * asmp.comm_ren_prem()[idx] * (1 + asmp.cnsmp_tax())
    else:
        return 0


def expense_maint_pp(t):
    """Maintenance expense per policy at time t"""
    return (ann_prem_pp(t) * asmp.exps_maint_ann_prem()[idx]
            + (sum_assured(t) * asmp.exps_maint_sa()[idx] + asmp.exps_maint_pol()[idx])
            * inflation_factor(t))


def exps_other_pp(t):
    """Other expenses per policy at time t"""
    return 0


def invst_income_pp(t):
    """Investment Income per policy from t to t+1"""
    return (reserve_total_aft_mat_pp(t) + premium_pp(t)) * invst_ret_rate(t)


def premium_pp(t):
    """Premium income per policy from t to t+1"""
    return sum_assured(t) * gross_prem_rate() * pol.prem_freq()[idx]


def reserve_prem_rsrv_aft_mat_pp(t):
    """Premium reserve per policy: After maturity"""
    return sum_assured(t) * pol.ReserveNLP_Rate('VAL', t)


def reserve_prem_rsrv_end_pp(t):
    """Premium reserve per policy: End of period"""
    return sum_assured(t) * pol.ReserveNLP_Rate('VAL', t)


def reserve_total_aft_mat_pp(t):
    """Total reserve per policy: After maturity"""
    return (reserve_prem_rsrv_aft_mat_pp(t)
           + reserve_uern_prem_aft_mat_pp(t))


def reserve_uern_prem_aft_mat_pp(t):
    """Unearned premium: After maturity"""
    return 0 # sum_assured(t) * polset.UnernPremRate(polset, tt, True)


def reserve_uern_prem_end_pp(t):
    """Unearned reserve per policy: End of period"""
    return 0 # sum_assured(t) * pol.UnernPremRate(polset, tt)


def sum_assured(t):
    """Sum assured per policy at time ``t``"""
    return  pol.sum_assured()[idx]


def proj_len():
    """Projection length in years for the selected policy.

    The projection ends at whichever comes first: the age at which
    base mortality reaches 1 (returned by :func:`last_mort_age`),
    or the end of the policy term.
    """
    return min(last_mort_age() - pol.issue_age()[idx],
               pol.policy_term()[idx])


def mort_rate(x):
    """Base mortality rate at age ``x``"""

    return asmp.mortality_tables()[x, asmp.mort_array_index()[idx]]


def gross_prem_rate():
    """Gross Premium Rate per Sum Assured per payment"""

    alpha = pol.load_acq_sa()[idx]
    beta = pol.load_maint_prem()[idx]
    gamma = pol.load_maint_sa()[idx]
    gamma2 = pol.load_maint_sa2()[idx]
    delta = pol.load_maint_prem_waiver_prem()[idx]

    x, n, m = pol.issue_age()[idx], pol.policy_term()[idx], pol.prem_term()[idx]

    freq = pol.prem_freq()[idx]

    comf = comm_table[
        pol.sex()[idx],
        pol.int_rate(RateBasisID.PREM)[idx],
        pol.table_id(RateBasisID.PREM)[idx]]

    if pol.product()[idx] == ProductID.TERM or pol.product()[idx] == ProductID.WL:
        return (comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, freq)
                + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / freq / comf.AnnDuenx(x, m, freq)

    elif pol.product()[idx] == ProductID.ENDW:
        return (comf.Exn(x, n) + comf.Axn(x, n) + alpha + gamma * comf.AnnDuenx(x, n, freq)
                + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / (1-beta-delta) / freq / comf.AnnDuenx(x, m, freq)
    else:
        raise ValueError('invalid product')


def mort_factor(y):
    """Mortality factor"""
    return asmp.asmp_tables()[min(y, asmp.asmp_table_len() - 1), asmp.mort_factor_index()[idx]]


def lapse_rate(y):
    """Surrender Rate"""
    return asmp.asmp_tables()[min(y, asmp.asmp_table_len() - 1), asmp.lapse_rate_index()[idx]]


def ann_prem_rate():
    """Annualized Premium Rate per Sum Assured"""
    return gross_prem_rate() * (1/10 if pol.prem_freq()[idx] == 0 else pol.prem_freq()[idx])


def cash_value_rate(t):
    """Cash Value Rate per Sum Assured"""
    return max(reserve_nlp_rate(RateBasisID.PREM, t) - surr_charge(t), 0)


def net_prem_rate(basis):
    """Net Premium Rate"""

    gamma2 = pol.load_maint_sa2()[idx]

    comf = comm_table[
        pol.sex()[idx],
        pol.int_rate(basis)[idx],
        pol.table_id(basis)[idx]]

    x, n, m = pol.issue_age()[idx], pol.policy_term()[idx], pol.prem_term()[idx]

    if pol.product()[idx] == ProductID.TERM or pol.product()[idx] == ProductID.WL:
        return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

    elif pol.product()[idx] == ProductID.ENDW:
        return (comf.Axn(x, n) + gamma2 * comf.AnnDuenx(x, n-m, 1, m)) / comf.AnnDuenx(x, n)

    else:
        raise ValueError('invalid product')


def reserve_nlp_rate(basis, t):
    """Net level premium reserve rate"""

    gamma2 = pol.load_maint_sa2()[idx]

    comf = comm_table[
        pol.sex()[idx],
        pol.int_rate(basis)[idx],
        pol.table_id(basis)[idx]]

    x, n, m = pol.issue_age()[idx], pol.policy_term()[idx], pol.prem_term()[idx]

    if t <= m:
        return comf.Axn(x+t, n-t) + gamma2 * comf.AnnDuenx(x+t, n-m, 1, m-t) \
                - net_prem_rate(basis) * comf.AnnDuenx(x+t, m-t)
    else:
        return comf.Axn(x+t, n-t) + gamma2 * comf.AnnDuenx(x+t, n-m, 1, m-t)


def surr_charge(t):
    """Surrender Charge Rate per Sum Assured"""
    m = pol.prem_term()[idx]
    return pol.init_surr_charge()[idx] * max((min(m, 10) - t) / min(m, 10), 0)


def last_mort_age():
    """Age at which the base mortality rate reaches 1 for this policy.

    Refers to
    :func:`~annuallife.TradLife_A.Assumptions.last_mort_age` for the
    selected policy.
    """
    return asmp.last_mort_age()[idx]


def inflation_factor(t):
    """Inflation factor at time ``t`` used to adjust expense cashflows.

    Compounded from :func:`~annuallife.TradLife_A.Assumptions.inflation_rate`
    starting from ``inflation_factor(0) = 1``.
    """
    if t == 0:
        return 1
    else:
        return inflation_factor(t-1) / (1 + asmp.inflation_rate())


def disc_rate_mth(t):
    """Discount rate at time ``t``.

    Refers to
    :func:`Economic[scen_id].disc_rate_mth<annuallife.TradLife_A.Economic.disc_rate_mth>`.
    """
    return scen.disc_rate_mth(t)


# ---------------------------------------------------------------------------
# References

scen = ("Interface", ("..", "Economic"), "auto")

asmp = ("Interface", ("..", "Assumptions"), "auto")

pol = ("Interface", ("..", "PolicyAttrs"), "auto")

comm_table = ("Interface", ("..", "CommTable"), "auto")
