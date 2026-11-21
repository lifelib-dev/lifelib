"""Closed sets used by the FIA_US_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class TaxStatus(IntEnum):
    NQ = 0
    Q = 1


class GlwbBasis(IntEnum):
    single = 0
    joint = 1


class CreditMethod(IntEnum):
    cap = 0
    par = 1
    par_cap = 2
    spread = 3
    trigger = 4


class Phase(IntEnum):
    ACCUM = 0
    INCOME = 1
    DEPLETED = 2
    TERMINATED = 3


class StepUpMode(IntEnum):
    annual = 0
    at_exercise = 1


class RbWdConvention(IntEnum):
    pro_rata = 0
    dollar = 1


class MvaCollarBasis(IntEnum):
    gross = 0
    surrender_value = 1


class ScenarioField(IntEnum):
    index_level = 0
    mva_ref_yield = 1


class Timing(IntEnum):
    BEF_PREM = 0
    BEF_INV = 1
    BEF_FEE = 2
    BEF_ROLLUP = 3
    BEF_STEP_UP = 4
    BEF_WD = 5
    EOY = 6


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_MORT = 1
    BEF_LAPSE = 2
    AFT_DECR = 3


class Claim(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3
