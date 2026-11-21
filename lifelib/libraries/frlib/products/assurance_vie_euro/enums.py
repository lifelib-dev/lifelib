"""Closed sets used by the Euro_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class GuaranteeForm(IntEnum):
    net = 0
    gross = 1


class Scenario(IntEnum):
    base = 0
    low = 1
    high = 2


class AvTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_WD = 2
    AFT_INT = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    ALL = 2
