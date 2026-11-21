"""Closed sets used by the VA_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class FundSet(IntEnum):
    bond50_eq50 = 0
    bond70_eq30 = 1
    bond80_eq20 = 2


class Scenario(IntEnum):
    base = 0
    low = 1
    high = 2


class CreditingBasis(IntEnum):
    decl_2026 = 0
    min_guar = 1


class FundTiming(IntEnum):
    BEF_PREM = 0
    BEF_DEDUCT = 1
    AFT_DEDUCT = 2
    AFT_DERISK = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    ANNUITY = 2
    MATURITY = 3
    ALL = 4


class AssetClass(IntEnum):
    bond = 0
    equity = 1


class ChargeLine(IntEnum):
    acq_charge = 0
    maint_charge_in = 1
    maint_charge_after = 2
    other_charge = 3
    gmdb_charge = 4
    gmab_charge_asset = 5
    gmab_charge_prem = 6
    surr_charge = 7
    surr_charge_cap = 8
    annuity_charge = 9
    fund_expense = 10
    comm_yr1 = 11
    comm_yr2 = 12
    comm_yr3 = 13
    comm_yr4 = 14
    comm_yr5 = 15
    expense_acq = 16
    expense_maint = 17
