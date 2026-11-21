"""Closed sets used by the WholeLife_JP_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class DividendType(IntEnum):
    none = 0
    five_year = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    BEF_SPIKE = 2
    AFT_DECR = 3


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    ALL = 2
