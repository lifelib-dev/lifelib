"""Codes for Registered Index-Linked Annuity claim types and market fields."""
from enum import IntEnum


class Claim(IntEnum):
    DEATH = 0
    LAPSE = 1
    MATURITY = 2
    ALL = 3


class MarketField(IntEnum):
    index_level = 0
    mvr = 1
    risk_free = 2
    div_yield = 3
    impl_vol = 4


class OptionLeg(IntEnum):
    ATM_CALL = 0
    OTM_CALL = 1
    OTM_PUT = 2
    ATM_PUT = 3
    FLOOR_PUT = 4
    STEP_BINARY = 5
    EDGE_BINARY = 6


class MarketQuote(IntEnum):
    CURRENT = 0
    TERM_START = 1


class Timing(IntEnum):
    BEF_CREDIT = 0
    BEF_ROLL = 1
    BEF_WD = 2
    AFT_WD = 3
    BEF_DECR = 4
    BEF_LAPSE = 5
    BEF_TERM_SURR = 6
    AFT_DECR = 7


class Bucket(IntEnum):
    OPTION = 0
    FIXED = 1
    HOLDING = 2


class CreditType(IntEnum):
    CAP = 0
    STEP = 1
    EDGE = 2
    FLOOR = 3


class InterimValueFamily(IntEnum):
    portfolio = 0
    notional = 1
    delta = 2
    legacy = 3


class Amortization(IntEnum):
    straight_line = 0
    updated_expiry = 1


class Sex(IntEnum):
    M = 0
    F = 1
