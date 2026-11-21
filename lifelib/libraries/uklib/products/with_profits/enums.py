"""Closed sets used by the WP_UK_S saved model."""

from enum import IntEnum


class Chassis(IntEnum):
    UWP_bond = 0
    CWP_endowment = 1


class Sex(IntEnum):
    M = 0
    F = 1


class TaxBasis(IntEnum):
    life_net = 0
    pension_gross = 1


class AsTiming(IntEnum):
    BEF_PREM = 0
    BEF_RETURN = 1
    AFT_RETURN = 2
    AFT_CHARGE = 3
    AFT_ST = 4
    AFT_MC = 5


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_SURR = 1
    AFT_DECR = 2


class ClaimKind(IntEnum):
    DEATH = 0
    SURRENDER = 1
    GUARANTEE = 2
    MATURITY = 3


class Kind(IntEnum):
    DEATH = 0
    SURRENDER = 1
    MATURITY = 2
    ALL = 3
