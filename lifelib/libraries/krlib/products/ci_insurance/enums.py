"""Closed sets used by the CI_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class FirstYearScope(IntEnum):
    breast = 0
    all = 1


class LapseBasis(IntEnum):
    log_linear = 0
    table = 1


class Cause(IntEnum):
    cancer = 0
    ami = 1
    stroke = 2
    other = 3
    ltc = 4


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    CI = 0
    DEATH = 1
    DEATH_CI = 2
    LAPSE = 3
    LAPSE_CI = 4
    ALL = 5


class ClaimBasis(IntEnum):
    FULL = 0
    REDUCED = 1
