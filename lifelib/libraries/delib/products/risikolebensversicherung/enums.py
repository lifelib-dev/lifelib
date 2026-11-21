"""Closed sets used by the RLV_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Smoker(IntEnum):
    N = 0
    R = 1


class PremiumForm(IntEnum):
    laufend = 0
    einmal = 1


class PremFreq(IntEnum):
    jaehrlich = 0
    halbjaehrlich = 1
    vierteljaehrlich = 2
    monatlich = 3


class SurplusForm(IntEnum):
    beitragsverrechnung = 0
    keine = 1


class ResTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1


class PolsTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class ClaimKind(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3
