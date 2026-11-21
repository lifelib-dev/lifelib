"""Closed sets used by the IUL_US_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class RateClass(IntEnum):
    PElite = 0
    PPlus = 1
    Pref = 2
    NT = 3
    PTob = 4
    Tob = 5
    Juv = 6


class DeathBenefitOption(IntEnum):
    A = 0
    B = 1


class Qualification(IntEnum):
    GPT = 0
    CVAT = 1


class PremiumType(IntEnum):
    SINGLE = 0
    LEVEL = 1
    TARGET = 2


class PremiumMode(IntEnum):
    ANNUAL = 0
    MONTHLY = 1


class Basis(IntEnum):
    CURRENT = 0
    GUARANTEED = 1


class CreditBase(IntEnum):
    REMAINING = 0
    ADJ_BEGIN = 1


class Timing(IntEnum):
    BEF_PREM = 0
    BEF_CREDIT = 1
    BEF_WD = 2
    BEF_FEE = 3
    BEF_SWEEP = 4
    BEF_INV = 5
    EOM = 6


class PolTiming(IntEnum):
    BEF_MAT = 0
    BEF_NB = 1
    BEF_DECR = 2


class Claim(IntEnum):
    DEATH = 0
    LAPSE = 1
    WITHDRAWAL = 2
    MATURITY = 3
    ALL = 4
