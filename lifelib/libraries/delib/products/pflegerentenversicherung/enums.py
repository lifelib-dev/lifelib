"""Closed sets used by the Pflege_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Status(IntEnum):
    aktiv = 0
    pg1 = 1
    pg2 = 2
    pg3 = 3
    pg4 = 4
    pg5 = 5


class BasisParam(IntEnum):
    rechnungszins = 0
    omega_age = 1
    unisex_mix_male = 2
    rec_age_ref = 3
    rec_age_decay = 4
    inc_cap = 5
    beitragssumme_cap_age = 6
    roll_fwd_tol = 7
    inc_margin = 8
    det_margin = 9
    rec_margin = 10
    care_mort_margin = 11
    act_mort_margin = 12


class ExpenseItem(IntEnum):
    acq_permille = 0
    admin_prem_pct = 1
    admin_mth_pp = 2
    claim_expense_pp = 3
    expense_infl = 4


class PremMode(IntEnum):
    monthly = 0
    quarterly = 1
    half_yearly = 2
    annual = 3
    single = 4


class Timing(IntEnum):
    BEG = 0
    END = 1


class Kind(IntEnum):
    ANNUITY = 0
    LAPSE = 1
    DEATH = 2
    ALL = 3
