"""Closed sets used by the Term_JP_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class TermType(IntEnum):
    nen = 0
    sai = 1


class PremMode(IntEnum):
    monthly = 0
    semiannual = 1
    annual = 2


class ContractBoundary(IntEnum):
    ceiling = 0
    current_term = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    BEF_DECLINE = 2
    AFT_DECR = 3


class Kind(IntEnum):
    DEATH = 0
    LIVING_NEEDS = 1
    LAPSE = 2
    ALL = 3
