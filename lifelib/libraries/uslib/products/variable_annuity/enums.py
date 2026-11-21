"""Closed sets used by the VA_US_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class DesignatedLives(IntEnum):
    single = 0
    joint = 1


class TaxStatus(IntEnum):
    NQ = 0
    Q = 1


class StepupBasis(IntEnum):
    annual_CV = 0
    highest_quarterly_CV = 1


class GmdbOption(IntEnum):
    basic = 0
    rollup = 1
    ratchet = 2


class FeeResetRule(IntEnum):
    none = 0
    quinquennial = 1
    vix = 2


class RollupRule(IntEnum):
    fixed = 0
    cmt_linked = 1


class Phase(IntEnum):
    ACCUM = 0
    DEPLETED = 1
    EXPIRED = 2


class RateColumn(IntEnum):
    vix_sq = 0
    cmt10 = 1


class Timing(IntEnum):
    BEF_PREM = 0
    BEF_WD = 1
    BEF_INV = 2
    BEF_FEE = 3
    BEF_ANNIV = 4
    EOM = 5


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Claim(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3
