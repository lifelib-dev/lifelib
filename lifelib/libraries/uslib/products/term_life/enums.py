"""Category values used by the Term_US_S saved model."""

from enum import IntEnum


class Plan(IntEnum):
    T10 = 0
    T20 = 1
    T30 = 2


class Sex(IntEnum):
    M = 0
    F = 1


class PremiumMode(IntEnum):
    A = 0
    SA = 1
    Q = 2
    M = 3


class RateClass(IntEnum):
    PPlusNT = 0
    PNT = 1
    StdNT = 2
    StdTob = 3
