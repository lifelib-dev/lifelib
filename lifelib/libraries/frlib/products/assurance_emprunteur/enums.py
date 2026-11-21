"""Closed sets used by the ADE_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PremiumBasis(IntEnum):
    capital_initial = 0
    capital_restant_du = 1


class IndemnityBasis(IntEnum):
    forfaitaire = 0
    indemnitaire = 1


class IptBenefitBasis(IntEnum):
    echeance = 0
    crd = 1


class Status(IntEnum):
    healthy = 0
    itt = 1
    ipt = 2


class PolTiming(IntEnum):
    BEF_DECR = 0
    AFT_DECR = 1


class Kind(IntEnum):
    DEATH = 0
    PTIA = 1
    ITT = 2
    IPT = 3
    LAPSE = 4
    MATURITY = 5
    ALL = 6
