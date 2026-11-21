"""Closed sets used by the FRV_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PremForm(IntEnum):
    laufend = 0
    einmal = 1


class DbForm(IntEnum):
    fund = 0
    prem_return = 1
    pct_fund = 2
    sum_assured = 3


class AvTiming(IntEnum):
    BEF_CHARGE = 0
    AFT_CHARGE = 1
    AFT_WD = 2
    BEF_DECR = 3


class PolsTiming(IntEnum):
    BEF_DECR = 0
    AFT_DEATH = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
