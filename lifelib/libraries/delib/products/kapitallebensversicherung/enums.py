"""Closed sets used by the KLV_DE_S saved model."""

from enum import IntEnum


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


class UnterjaehrigForm(IntEnum):
    echt = 0
    unecht = 1


class SurplusUse(IntEnum):
    ansammlung = 0
    bonus = 1
    beitragsverrechnung = 2


class ResTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_INT = 2


class SurTiming(IntEnum):
    BEF_INT = 0
    AFT_INT = 1
    AFT_CREDIT = 2


class PolsTiming(IntEnum):
    BEF_DECR = 0
    AFT_MORT = 1
    AFT_LAPSE = 2


class Kind(IntEnum):
    DEATH = 0
    MATURITY = 1
    LAPSE = 2
    ALL = 3
