"""Closed sets used by the Dep_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class CoverType(IntEnum):
    total_and_partial = 0
    total_only = 1


class TriggerGrid(IntEnum):
    avq5 = 0
    avq6 = 1
    aggir = 2


class PremiumMode(IntEnum):
    monthly = 0
    quarterly = 1
    half_yearly = 2
    annual = 3


class Cause(IntEnum):
    accident = 0
    illness = 1
    neuro = 2


class Status(IntEnum):
    autonomous = 0
    partial = 1
    total = 2
    reduced = 3


class PrevParam(IntEnum):
    prev_ceil = 0
    prev_beta = 1
    prev_x_mid = 2


class Severity(IntEnum):
    partial = 0
    total = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    AFT_DECR = 1


class Kind(IntEnum):
    RENTE = 0
    CAPITAL = 1
    LAPSE = 2
    ALL = 3
