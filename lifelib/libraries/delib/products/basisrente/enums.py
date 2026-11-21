"""Closed sets used by the Basis_DE_S saved model."""

from enum import IntEnum


class PremForm(IntEnum):
    regular = 0
    single = 1


class OptionId(IntEnum):
    prem_mode = 0
    guarantee_period = 1
    survivor = 2


class PremMode(IntEnum):
    annual = 0
    half_yearly = 1
    quarterly = 2
    monthly = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    AFT_DEATH = 1
    AFT_FREEZE = 2


class AvTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_INT = 2


class Kind(IntEnum):
    DEATH = 0
    ANNUITY = 1
    SURVIVOR = 2
    ALL = 3
