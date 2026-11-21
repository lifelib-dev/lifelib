"""Closed sets used by the SPIA_US_S saved model."""

from enum import IntEnum


class Form(IntEnum):
    life_only = 0
    life_certain = 1
    cash_refund = 2
    installment_refund = 3
    certain_only = 4


class Sex(IntEnum):
    M = 0
    F = 1


class ReductionTrigger(IntEnum):
    either = 0
    primary = 1


class PaymentTiming(IntEnum):
    arrears = 0
    advance = 1


class MortBasis(IntEnum):
    table = 0
    scenario = 1


class Kind(IntEnum):
    REFUND = 0
    ALL = 1


class DiscConvention(IntEnum):
    compound = 0
    simple = 1
