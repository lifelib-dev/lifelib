# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Base Space for the :mod:`~simplelife.model.Projection` Space.

This Space serves as a base Space for :mod:`~simplelife.model.Projection`
Space, and it contains Cells for cashflow projection.

.. rubric:: Inheritance Structure

.. figure:: /images/projects/simplelife/model/BaseProj/diagram1.png


``Pols``:
    Cells whose names start with ``Pols`` deal with number of policies.
    For example, ``pols_death(t)`` represents number of deaths between
    time ``t`` and ``t+1``.

``Size``:
    Cells whose names start with ``Size`` represents an amount per policy.
    For example, ``claim_pp`` represents sum assured per policy.

``Exps``:
    Cells whose names start with ``Exps`` represents expense cashflows.
    For example, ``exps_comm_ren`` means the renewal commission cashflow.

``Benefit``:
    Cells whose names start with ``Benefit`` represents benefit cashflows.
    For example, ``claims(t)`` death benefits incurred
    between ``t`` and ``t+1``.

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


def benefit_acc_dth(t):
    """Accidental death benefits"""
    return size_benefit_acc_dth(t) * pols_acc_death(t)


def benefit_acc_hosp(t):
    """Accidental hospitalization benefits"""
    return size_benefit_acc_hosp(t) * pols_acc_hosp(t)


def benefit_ann(t):
    """Annuity benefits"""
    return size_benefit_ann(t) * pols_annuity(t)


def claims(t):
    """Death benefits"""
    return claim_pp(t) * pols_death(t)


def benefit_living(t):
    """Living benefits"""
    return size_benefit_living(t) * pols_living(t)


def benefit_mat(t):
    """Matuirty benefits"""
    return size_benefit_mat(t) * pols_maturity(t)


def benefit_other(t):
    """Other benefits"""
    return size_benefit_other(t) * pols_other(t)


def benefit_sick_hosp(t):
    """Sickness hospitalization benefits"""
    return size_benefit_sick_hosp(t) * pols_sick_hosp(t)


def benefit_surg(t):
    """Surgery benefits"""
    return size_benefit_surg(t) * pols_surg(t)


def benefit_surr(t):
    """Surrender benefits"""
    return size_benefit_surr(t) * pols_lapse(t)


def benefit_total(t):
    """Benefit Total"""
    return (benefit_mat(t)
            + claims(t)
            + benefit_acc_dth(t)
            + benefit_surr(t)
            + benefit_ann(t)
            + benefit_acc_hosp(t)
            + benefit_sick_hosp(t)
            + benefit_surg(t)
            + benefit_living(t)
            + benefit_other(t))


def change_rsrv(t):
    """Change in reserve"""
    return reserve_total_end(t+1) - reserve_total_end(t)


def exps_acq(t):
    """Acquisition expenses"""
    return expense_acq(t) * (pols_if_init(t) + pols_renewal(t))


def exps_acq_total(t):
    """Commissions and acquisition expenses"""
    return commissions(t) + exps_acq(t)


def exps_comm_init(t):
    """Initial commissions"""
    return size_exps_comm_init(t) * pols_if_beg1(t)


def exps_comm_ren(t):
    """Renewal commissions"""
    return size_exps_comm_ren(t) * pols_if_beg1(t)


def commissions(t):
    """Commissions Total"""
    return exps_comm_init(t) + exps_comm_ren(t)


def exps_maint(t):
    """Maintenance expenses"""
    return expense_maint(t) * pols_if_beg1(t)


def exps_maint_total(t):
    """Total maintenance expenses including other expenses"""
    return exps_maint(t) + exps_other(t)


def exps_other(t):
    """Other expenses"""
    return 0


def expenses(t):
    """Total expenses"""
    return (exps_comm_init(t)
            + exps_comm_ren(t)
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
    """Intrest on accumulated cashflows"""
    return (accum_cf(t)
            + premiums(t)
            - expenses(t)) * disc_rate_mth(t)


def invst_income(t):
    """Investment income"""
    return size_invst_income(t) * pols_if_beg1(t)


def net_cf(t):
    """Net liability cashflow"""
    return (premiums(t)
            - benefit_total(t)
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
    """Number of policies: Maturity"""
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
            - benefit_total(t)
            - expenses(t)
            - change_rsrv(t))


def reserve_hosp_rsrv_end(t):
    """Hospitalization reserve: End of period"""
    return 0


def reserve_prem_rsrv_end(t):
    """Premium reserve: End of period"""
    return size_reserve_prem_rsrv_end(t) * pols_if(t)


def reserve_total_end(t):
    """Total reserve: End of period"""
    return (reserve_prem_rsrv_end(t)
            + reserve_uern_prem_end(t)
            + reserve_hosp_rsrv_end(t))


def reserve_uern_prem_end(t):
    """Unearned Premium: End of period"""
    return 0


def size_ann_prem(t):
    """Annualized premium per policy at time ``t``"""
    return sum_assured(t) * ann_prem_rate()


def size_benefit_acc_dth(t):
    """Accidental death benefit per policy"""
    return 0


def size_benefit_acc_hosp(t):
    """Accidental hospitalization benefit per policy"""
    return 0


def size_benefit_ann(t):
    """Annuity benefit per policy"""
    return 0


def claim_pp(t):
    """Death benefit per policy"""
    return sum_assured(t)


def size_benefit_living(t):
    """Living benefit per policy"""
    return 0


def size_benefit_mat(t):
    """Maturity benefit per policy"""
    return 0


def size_benefit_other(t):
    """Other benefit per policy"""
    return 0


def size_benefit_sick_hosp(t):
    """Sickness hospitalization benefit per policy"""
    return 0


def size_benefit_surg(t):
    """Surgery benefit per policy"""
    return 0


def size_benefit_surr(t):
    """Surrender benefit per policy"""
    return sum_assured(t) * (cash_value_rate(t)
                                + cash_value_rate(t+1)) / 2


def expense_acq(t):
    """Acquisition expense per policy at time t"""
    if t == 0:
        return (size_ann_prem(t) * asmp.exps_acq_ann_prem()[idx]
                + (sum_assured(t) * asmp.exps_acq_sa()[idx] + asmp.exps_acq_pol()[idx])
                * inflation_factor(t) / inflation_factor(0))
    else:
        return 0


def size_exps_comm_init(t):
    """Initial commission per policy at time t"""
    if t == 0:
        return premium_pp(t) * asmp.comm_init_prem()[idx] * (1 + asmp.cnsmp_tax())
    else:
        return 0


def size_exps_comm_ren(t):
    """Renewal commission per policy at time t"""
    if t == 0:
        return 0
    elif t < asmp.comm_ren_term()[idx]:
        return premium_pp(t) * asmp.comm_ren_prem()[idx] * (1 + asmp.cnsmp_tax())
    else:
        return 0


def expense_maint(t):
    """Maintenance expense per policy at time t"""
    return (size_ann_prem(t) * asmp.exps_maint_ann_prem()[idx]
            + (sum_assured(t) * asmp.exps_maint_sa()[idx] + asmp.exps_maint_pol()[idx])
            * inflation_factor(t))


def size_exps_other(t):
    """Other expenses per policy at time t"""
    return 0


def size_invst_income(t):
    """Investment Income per policy from t to t+1"""
    return (size_reserve_total_aft_mat(t) + premium_pp(t)) * invst_ret_rate(t)


def premium_pp(t):
    """Premium income per policy from t to t+1"""
    return sum_assured(t) * gross_prem_rate() * pol.prem_freq()[idx]


def size_reserve_prem_rsrv_aft_mat(t):
    """Premium reserve per policy: After maturity"""
    return sum_assured(t) * pol.ReserveNLP_Rate('VAL', t)


def size_reserve_prem_rsrv_end(t):
    """Premium reserve per policy: End of period"""
    return sum_assured(t) * pol.ReserveNLP_Rate('VAL', t)


def size_reserve_total_aft_mat(t):
    """Total reserve per policy: After maturity"""
    return (size_reserve_prem_rsrv_aft_mat(t)
           + size_reserve_uern_prem_aft_mat(t))


def size_reserve_uern_prem_aft_mat(t):
    """Unearned premium: After maturity"""
    return 0 # sum_assured(t) * polset.UnernPremRate(polset, tt, True)


def size_reserve_uern_prem_end(t):
    """Unearned reserve per policy: End of period"""
    return 0 # sum_assured(t) * pol.UnernPremRate(polset, tt)


def sum_assured(t):
    """Sum assured per policy at time ``t``"""
    return  pol.sum_assured()[idx]


def proj_len():
    return min(last_age() - pol.issue_age()[idx], 
               pol.policy_term()[idx])


def mort_rate(x):
    """Bae mortality rate"""

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
    # comf = life_table[sex(), int_rate(basis), table_id(basis)]


    comf = comm_table[
        pol.sex()[idx], 
        pol.int_rate(basis)[idx], 
        pol.table_id(basis)[idx]]


    # x, n, m = issue_age(), policy_term(), prem_term()

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

    # lt = life_table[sex(), int_rate(basis), table_id(basis)]
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


def last_age():
    """Age at which mortality becomes 1"""
    x = 0
    while True:
        if mort_rate(x) == 1:
            return x
        x += 1


def inflation_factor(t):
    """Inflation factors to adjust expense cashflows"""
    if t == 0:
        return 1
    else:
        return inflation_factor(t-1) / (1 + asmp.inflation_rate())


def disc_rate_mth(t):
    return scen.disc_rate_mth(t)


