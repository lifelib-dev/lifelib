"""Closed sets used by the ULSG_US_S saved model."""

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


class PremiumType(IntEnum):
    SINGLE = 0
    TEN_PAY = 1
    LEVEL = 2


class PremiumMode(IntEnum):
    A = 0
    S = 1
    Q = 2
    M = 3


class Timing(IntEnum):
    BEF_PREM = 0
    BEF_WD = 1
    BEF_FEE = 2
    BEF_COI = 3
    BEF_INV = 4
    EOM = 5


class LoanTiming(IntEnum):
    BEF_INT = 0


class PolTiming(IntEnum):
    BEF_MAT = 0
    BEF_NB = 1
    BEF_DECR = 2


class Claim(IntEnum):
    DEATH = 0
    LAPSE = 1
    REFUND = 2
    WITHDRAWAL = 3
    GRACE = 4
    MATURITY = 5
    ALL = 6
