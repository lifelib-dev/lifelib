"""Closed sets used by the Term_UK_S saved model."""

from enum import IntEnum


class Shape(IntEnum):
    level = 0
    decreasing = 1
    fib = 2


class Sex(IntEnum):
    M = 0
    F = 1


class Smoker(IntEnum):
    N = 0
    S = 1


class PremiumMode(IntEnum):
    monthly = 0
    annual = 1


class MortBasis(IntEnum):
    applied = 0
    select = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    FIB = 1
    LAPSE = 2
    ALL = 3
