"""Closed sets used by the Immediate_KR_S saved model."""

from enum import IntEnum


class Shape(IntEnum):
    life = 0
    inheritance = 1
    certain = 2


class Sex(IntEnum):
    M = 0
    F = 1


class RetentionBasis(IntEnum):
    as_designed = 0
    as_ordered = 1


class CreditingBasis(IntEnum):
    decl_2017 = 0
    min_guar = 1


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
