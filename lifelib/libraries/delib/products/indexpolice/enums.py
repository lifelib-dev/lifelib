"""Closed sets used by the Index_DE_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PremForm(IntEnum):
    level = 0
    single = 1


class PremFreq(IntEnum):
    annual = 0
    half_yearly = 1
    quarterly = 2
    monthly = 3


class PayoffForm(IntEnum):
    cap = 0
    quote = 1


class AnnOption(IntEnum):
    annuity = 0
    cash = 1


class AvTiming(IntEnum):
    BEF_PREM = 0
    AFT_PREM = 1
    AFT_CHARGE = 2
    AFT_GUAR = 3
    AFT_CREDIT = 4


class PolsTiming(IntEnum):
    BEF_DECR = 0
    AFT_DEATH = 1
    AFT_LAPSE = 2


class ClaimKind(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3
