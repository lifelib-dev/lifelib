"""Closed sets used by the EC_FR_S saved model."""

from enum import IntEnum


class EngagementModality(IntEnum):
    euro_and_parts = 0
    parts_only = 1


class Sex(IntEnum):
    M = 0
    F = 1


class DecrementBasis(IntEnum):
    table = 0
    none = 1


class Scenario(IntEnum):
    shock = 0
    base = 1
    downside = 2
    sloped = 3
    zero_rate = 4


class AcctTiming(IntEnum):
    BOM = 0
    AFT_LEVY = 1
    AFT_EXIT = 2
    AFT_PREM = 3
    AFT_STRIKE = 4
    AFT_RETURN = 5
    AFT_PERF = 6
    AFT_TOP_UP = 7


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3
