"""Closed sets used by the WholeLife_US_S saved model."""

from enum import IntEnum


class Product(IntEnum):
    WL_PAR = 0
    WL_FE_LEVEL = 1
    WL_FE_GRADED = 2


class PremiumPeriod(IntEnum):
    TO_100 = 0
    PAY_10 = 1
    PAY_20 = 2
    TO_65 = 3


class Sex(IntEnum):
    M = 0
    F = 1


class RiskClass(IntEnum):
    PREF_NT = 0
    STD_NT = 1
    TOB = 2


class DividendOption(IntEnum):
    CASH = 0
    REDUCE_PREM = 1
    ACCUM = 2
    PUA = 3
    NONE = 4


class PremiumMode(IntEnum):
    A = 0
    SA = 1
    Q = 2
    M = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_SURR = 1
    BEF_MAT = 2
    AFT_DECR = 3


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3
