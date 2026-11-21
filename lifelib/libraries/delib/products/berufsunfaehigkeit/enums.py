"""Closed sets used by the BU_DE_S saved model."""

from enum import IntEnum


class Status(IntEnum):
    aktiv = 0
    leistung = 1


class Sex(IntEnum):
    M = 0
    F = 1


class Berufsgruppe(IntEnum):
    BG1 = 0
    BG2 = 1
    BG3 = 2
    BG4 = 3
    BG5 = 4


class PremiumForm(IntEnum):
    level = 0
    dynamik = 1


class PremMode(IntEnum):
    annual = 0
    half_yearly = 1
    quarterly = 2
    monthly = 3


class Timing(IntEnum):
    BEG = 0
    END = 1


class Kind(IntEnum):
    BU_RENTE = 0
    REINTEGRATION = 1
    LAPSE = 2
    ALL = 3
