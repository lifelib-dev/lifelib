"""Closed sets used by the TD_FR_S saved model."""

from enum import IntEnum


class PremiumForm(IntEnum):
    revisable = 0
    constante = 1


class BenefitShape(IntEnum):
    constant = 0
    decreasing = 1


class Sex(IntEnum):
    M = 0
    F = 1


class Smoker(IntEnum):
    N = 0
    S = 1


class PremFreq(IntEnum):
    annual = 0
    half_yearly = 1
    quarterly = 2
    monthly = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    PTIA = 1
    LAPSE = 2
    ALL = 3
