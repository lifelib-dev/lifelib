"""Closed sets used by the RV_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PremiumForm(IntEnum):
    laufend = 0
    einmal = 1


class PremFreq(IntEnum):
    annual = 0
    half_yearly = 1
    quarterly = 2
    monthly = 3


class DeathBenefitForm(IntEnum):
    prem_refund = 0
    deckungskapital = 1
    max = 2


class PayoutSystem(IntEnum):
    konstant = 0
    volldynamisch = 1
    teildynamisch = 2


class AvTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_INT = 2


class PolsTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class ClaimKind(IntEnum):
    DEATH = 0
    LAPSE = 1
    COMMUTATION = 2
    ALL = 3


class ParamItem(IntEnum):
    expense_acq_pp = 0
    expense_maint_pp = 1
    expense_annuity_pp = 2
    expense_claim_pp = 3
    expense_infl = 4
    mort_be_factor = 5
    mort_base_year = 6
    omega_age = 7
    val_reserve_rate = 8
    sur_ann_rate = 9
    sur_ann_growth = 10
    sur_ann_theta = 11
    roll_fwd_tol = 12


class ChargeItem(IntEnum):
    alpha_rate = 0
    alpha_spread_years = 1
    beta_rate = 2
    gamma_rate = 3
    gamma_pup_rate = 4
    stornoabzug_rate = 5
    min_annuity_mth = 6
    annuity_admin_rate = 7
