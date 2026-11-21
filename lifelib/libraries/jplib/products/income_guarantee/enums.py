"""Closed sets used by the IncomeTerm_JP_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class RateClass(IntEnum):
    nonsmoker_preferred = 0
    smoker_preferred = 1
    nonsmoker_standard = 2
    smoker_standard = 3


class PremMode(IntEnum):
    monthly = 0
    semiannual = 1
    annual = 2


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    ANNUITY = 0
    COMMUTATION = 1
    LIVING_NEEDS = 2
    LAPSE = 3
    ALL = 4
