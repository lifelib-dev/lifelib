"""Closed sets used by the PER_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Compartment(IntEnum):
    c1 = 0
    c2 = 1
    c3 = 2


class AllocationProfile(IntEnum):
    prudent = 0
    equilibre = 1
    dynamique = 2
    offensif = 3


class ExitForm(IntEnum):
    capital_single = 0
    capital_staged = 1
    annuity = 2
    mixed = 3


class MortBasis(IntEnum):
    flat = 0
    table = 1


class AvTiming(IntEnum):
    BEF_REBAL = 0
    BOM = 1
    BEF_CHARGE = 2
    EOM = 3


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_RELEASE = 1
    BEF_TRANSFER = 2
    AFT_DECR = 3


class Kind(IntEnum):
    DEATH = 0
    EARLY_RELEASE = 1
    TRANSFER = 2
    MATURITY = 3
    ALL = 4
