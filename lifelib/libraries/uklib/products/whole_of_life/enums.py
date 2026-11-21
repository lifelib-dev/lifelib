"""Closed sets used by the WOL_UK_S saved model."""

from enum import IntEnum


class Cell(IntEnum):
    O50 = 0
    UW = 1


class Sex(IntEnum):
    M = 0
    F = 1


class Smoker(IntEnum):
    NS = 0
    S = 1


class Escalation(IntEnum):
    level = 0
    fixed_5pct = 1
    rpi = 2


class MortBasis(IntEnum):
    population = 0
    assured = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class BenefitKind(IntEnum):
    NON_ACC = 0
    ACC = 1
    DEATH = 2
    PAID_UP = 3


class Kind(IntEnum):
    DEATH = 0
    DEATH_PU = 1
    LAPSE = 2
    ALL = 3
