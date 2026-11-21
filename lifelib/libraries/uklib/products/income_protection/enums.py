"""Closed sets used by the IP_UK_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Escalation(IntEnum):
    RPI = 0
    none = 1


class PremiumBasis(IntEnum):
    guaranteed = 0


class Status(IntEnum):
    active = 0
    in_claim = 1


class RecoveryBasis(IntEnum):
    return_to_h = 0
    exit = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    AFT_DECR = 1


class Kind(IntEnum):
    BENEFIT = 0
    DEATH = 1
    LAPSE = 2
    ALL = 3
