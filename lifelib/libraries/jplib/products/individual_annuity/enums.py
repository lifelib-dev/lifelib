"""Closed sets used by the Annuity_JP_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PayoutForm(IntEnum):
    certain = 0
    life_guar = 1


class MortTable(IntEnum):
    death_cover_2018 = 0
    annuity_payout_2007 = 1


class Segment(IntEnum):
    premium_paying = 0
    defer_gap = 1
    pre_annuitisation = 2


class PricingItem(IntEnum):
    int_rate_defer = 0
    int_rate_payout = 1
    expense_loading = 2
    annuitisation_charge = 3
    surr_charge_years = 4
    surr_charge_prems = 5
    mort_be_factor_defer = 6
    mort_be_factor_payout = 7
    annuity_round_to = 8
    div_int_rate = 9
    loan_rate = 10
    apl_rate = 11
    loan_draw_frac = 12
    loan_draw_year = 13
    lapse_dyn_phi = 14
    lapse_dyn_cap = 15
    commute_int_rate = 16


class ExpenseItem(IntEnum):
    expense_acq = 0
    comm_init_rate = 1
    comm_renewal_rate = 2
    expense_maint_defer = 3
    expense_maint_payout = 4
    expense_claim = 5
    inflation_rate = 6


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
    COMMUTATION = 3
    ALL = 4


class Weighting(IntEnum):
    count = 0
    fund = 1
