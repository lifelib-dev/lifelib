"""Closed sets used by the WholeLife_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class IntBasis(IntEnum):
    fixed = 0
    linked = 1


class LapseBasis(IntEnum):
    loglinear = 0
    flat = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    REDUCTION = 2
    ALL = 3
