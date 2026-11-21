"""Closed sets used by the Pension_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PayoutForm(IntEnum):
    life_guar = 0
    certain = 1


class MortVintage(IntEnum):
    issue = 0
    commencement = 1
    ratchet = 2


class LapseBasis(IntEnum):
    pension = 0
    savings = 1


class RateScenario(IntEnum):
    base = 0
    floor = 1
    hybrid = 2


class MortTable(IntEnum):
    annuitant_issue = 0
    annuitant_revised = 1


class Segment(IntEnum):
    premium_paying = 0
    paid_up = 1
    in_payment = 2


class AnchorItem(IntEnum):
    law_a = 0
    law_b = 1
    law_c = 2
    age_setback = 3
    omega_age = 4
    improve_factor = 5
    pub_q_40 = 6
    pub_q_50 = 7
    pub_q_60 = 8
    pub_q_70 = 9
    pub_q_80 = 10


class PricingItem(IntEnum):
    prem_freq = 0
    annuity_freq = 1
    prem_int_rate = 2
    avg_decl_rate = 3
    acq_charge_rate = 4
    acq_charge_years = 5
    maint_charge_rate = 6
    maint_charge_rate_paid_up = 7
    addl_charge_rate = 8
    addl_prem_cap_ratio = 9
    annuity_charge_rate = 10
    min_fund_ratio = 11
    mort_be_factor = 12
    surr_chg_years = 13
    surr_chg_cap_rate = 14
    surr_chg_cap_rate_par = 15
    surr_chg_cap_term_cap = 16
    surr_chg_cap_level_years = 17
    loan_rate = 18
    loan_draw_frac = 19
    loan_draw_year = 20
    holiday_start_year = 21
    holiday_max_years = 22
    div_int_rate = 23


class ExpenseItem(IntEnum):
    expense_acq = 0
    expense_maint_defer = 1
    expense_maint_payout = 2
    expense_claim = 3
    inflation_rate = 4
    comm_init_rate = 5
    comm_renewal_rate = 6


class TaxItem(IntEnum):
    credit_rate_low_income = 0
    credit_rate_high_income = 1
    credit_income_threshold = 2
    credit_cap = 3
    contribution_ceiling = 4
    other_income_tax_rate = 5
    pension_tax_rate_under70 = 6
    pension_tax_rate_70to79 = 7
    pension_tax_rate_80plus = 8
    pension_tax_rate_life = 9
    aggregation_threshold = 10
    min_annuity_age = 11
    min_account_years = 12
    limit_denominator_base = 13
    limit_uplift = 14


class AvTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_INT = 2


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    ANNUITY = 0
    DEATH = 1
    LAPSE = 2
    ALL = 3
