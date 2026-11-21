"""Closed sets used by the ULB_UK_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Lives(IntEnum):
    single = 0


class WdPattern(IntEnum):
    none = 0
    allowance_5pct = 1
    custom = 2


class AvTiming(IntEnum):
    BEF_GROWTH = 0
    AFT_GROWTH = 1
    AFT_CHARGE = 2
    AFT_WD = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_SURR = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    SURRENDER = 1
    ALL = 2
