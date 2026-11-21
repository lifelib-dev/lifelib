"""Closed sets used by the Sofort_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1
    U = 2


class Basis(IntEnum):
    FIRST = 0
    SECOND = 1


class RefundForm(IntEnum):
    none = 0
    full = 1


class PaymentTiming(IntEnum):
    advance = 0
    arrears = 1


class SurplusForm(IntEnum):
    none = 0
    konstant = 1
    teildynamisch = 2
    volldynamisch = 3


class AnnuityKind(IntEnum):
    ANNUITANT = 0
    SURVIVOR = 1
    ALL = 2


class ClaimKind(IntEnum):
    GUARANTEE = 0
    REFUND = 1
    ALL = 2
