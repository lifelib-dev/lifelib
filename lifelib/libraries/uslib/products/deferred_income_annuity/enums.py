"""Closed sets used by the DIA_US_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class ReductionTrigger(IntEnum):
    either = 0
    primary = 1


class MarketType(IntEnum):
    NQ = 0
    TradIRA = 1
    RothIRA = 2
    QLAC = 3


class IncomeForm(IntEnum):
    LO = 0
    LO_ROP = 1
    CR = 2
    IR = 3
    PC = 4


class DbForm(IntEnum):
    ROP = 0
    NONE = 1


class PaymentTiming(IntEnum):
    arrears = 0
    advance = 1


class MortBasis(IntEnum):
    anchor = 0
    generational = 1


class FactorBasis(IntEnum):
    table = 0
    formula = 1


class Phase(IntEnum):
    DEFERRAL = 0
    PAYOUT = 1
    TERMINATED = 2


class Claim(IntEnum):
    DEATH = 0
    REFUND = 1
    ALL = 2
