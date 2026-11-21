"""Closed sets used by the Rente_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1
    mix = 2


class PalierScheme(IntEnum):
    none = 0
    inc1 = 1
    inc2 = 2
    dec1 = 3
    dec2 = 4


class PaymentTiming(IntEnum):
    arrears = 0
    advance = 1


class MortBasis(IntEnum):
    table = 0
    scenario = 1


class AnnuityKind(IntEnum):
    ANNUITANT = 0
    ALL = 1


class Kind(IntEnum):
    PRORATA = 0
    ALL = 1
