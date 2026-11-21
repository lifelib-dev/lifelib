"""Closed sets used by the Term_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class RenewalType(IntEnum):
    gaengsin = 0
    bi_gaengsin = 1


class RateClass(IntEnum):
    standard = 0
    nonsmoker = 1
    preferred = 2
    super_preferred = 3


class MaturityForm(IntEnum):
    pure = 0
    rop = 1


class PremiumMode(IntEnum):
    monthly = 0


class ContractBoundary(IntEnum):
    ceiling = 0
    current_term = 1


class Segment(IntEnum):
    in_payment_start = 0
    in_payment_end = 1
    post_payment = 2


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    BEF_DECLINE = 2
    AFT_DECR = 3


class Kind(IntEnum):
    DEATH = 0
    ACC_DEATH = 1
    ACCEL = 2
    MATURITY = 3
    LAPSE = 4
    ALL = 5
