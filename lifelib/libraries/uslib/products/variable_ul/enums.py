"""Closed sets used by the VUL_US_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class RateClass(IntEnum):
    PPlusNT = 0
    PNT = 1
    StdPlusNT = 2
    StdNT = 3
    PTob = 4
    StdTob = 5


class DeathBenefitOption(IntEnum):
    A = 0
    B = 1


class Qualification(IntEnum):
    GPT = 0
    CVAT = 1


class PremiumType(IntEnum):
    SINGLE = 0
    LEVEL = 1


class Timing(IntEnum):
    BEF_PREM = 0
    BEF_WD = 1
    BEF_FEE = 2
    BEF_INV = 3
    BEF_ME = 4
    EOM = 5


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
