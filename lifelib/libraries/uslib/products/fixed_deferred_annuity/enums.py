"""Category values used by the MYGA_US_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1

class Renewal(IntEnum):
    rollover = 0
    annual_redeclare = 1

class FreeRule(IntEnum):
    pct_av = 0
    interest_only = 1

class MgsvWithdrawal(IntEnum):
    gross = 0
    net_of_charges = 1

class MvaFamily(IntEnum):
    linear_duration = 0
    geometric = 1
    declared_differential = 2

class Cap(IntEnum):
    none = 0
    sym_sc = 1
    min_sc_interest = 2
    asym_sc_snfl = 3
    gmir_floor = 4

class Schedule(IntEnum):
    initial = 0
    renewal = 1
    none = 2

class AvTiming(IntEnum):
    BEF_WD = 0
    BEF_INV = 1
    EOM = 2

class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_MORT = 1
    BEF_LAPSE = 2
    AFT_DECR = 3

class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    ANNUITIZATION = 2
    MATURITY = 3
    ALL = 4

class RateColumn(IntEnum):
    mva_ref_yield = 0
    market_rate = 1
