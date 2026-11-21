"""Closed sets used by the PA_UK_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PaymentTiming(IntEnum):
    arrears = 0
    advance = 1


class EscalationType(IntEnum):
    level = 0
    fixed = 1
    rpi_catchup = 2
    lpi5 = 3


class VpBasis(IntEnum):
    first_death = 0
    last_survivor = 1


class MortBasis(IntEnum):
    table = 0
    scenario = 1


class AnnuityKind(IntEnum):
    ANNUITANT = 0
    ALL = 1


class Kind(IntEnum):
    VP = 0
    PROP = 1
    ALL = 2
