"""Codes for Universal Life claim types and account-value timing."""
from enum import IntEnum


class Claim(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3


class Timing(IntEnum):
    BEF_PREM = 0
    BEF_WD = 1
    BEF_FEE = 2
    BEF_INV = 3
    EOM = 4


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


class PolTiming(IntEnum):
    BEF_MAT = 0
    BEF_NB = 1
    BEF_DECR = 2
