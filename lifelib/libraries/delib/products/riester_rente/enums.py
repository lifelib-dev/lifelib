"""Closed sets used by the Riester_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class ContribForm(IntEnum):
    mindest = 0
    fixed = 1


class PremFreq(IntEnum):
    annual = 0
    half_yearly = 1
    quarterly = 2
    monthly = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    AFT_DECR = 1


class AvTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_INT = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    TRANSFER = 2
    LUMPSUM = 3
    COMMUTATION = 4
    ANNUITY = 5
    ALL = 6
