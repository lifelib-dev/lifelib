"""Closed sets used by the Obseques_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PremiumForm(IntEnum):
    single = 0
    temporary = 1
    lifetime = 2


class RefundBasis(IntEnum):
    gross = 0
    net_assistance = 1
    net_instalment = 2


class SurrScale(IntEnum):
    s14_50_viager = 0
    s14_50_temp10 = 1
    s5_50_viager = 2
    s5_50_unique = 3
    s15_70_viager = 4
    s2_50_temp25 = 5


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class BenefitKind(IntEnum):
    ILL = 0
    ACC = 1
    DEATH = 2
    PAID_UP = 3


class Kind(IntEnum):
    DEATH = 0
    DEATH_PAID_UP = 1
    LAPSE = 2
    ALL = 3


class CrossoverBasis(IntEnum):
    ISSUE = 0
    CURRENT = 1
