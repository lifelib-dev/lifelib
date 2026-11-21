"""Closed sets used by the Medical_JP_S saved model."""

from enum import IntEnum


class Chassis(IntEnum):
    shushin = 0
    teiki = 1


class Sex(IntEnum):
    M = 0
    F = 1


class PremPeriod(IntEnum):
    whole_life = 0
    to_65 = 1


class PremMode(IntEnum):
    monthly = 0
    semiannual = 1
    annual = 2


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    HOSP = 0
    SURGERY = 1
    ADVANCED = 2
    LUMP = 3
    LAPSE = 4
    ALL = 5
