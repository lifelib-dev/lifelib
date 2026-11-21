"""Closed sets used by the Cancer_JP_S saved model."""

from enum import IntEnum


class Chassis(IntEnum):
    shushin = 0
    teiki = 1


class Sex(IntEnum):
    M = 0
    F = 1


class PremPeriod(IntEnum):
    whole_life = 0
    to_65 = 1


class PremMode(IntEnum):
    monthly = 0
    semiannual = 1
    annual = 2


class WaiverTrigger(IntEnum):
    cancer_diag = 0
    disability = 1
    none = 2


class StayBasis(IntEnum):
    all_ages = 0
    age_band = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DIAG = 0
    INSITU = 1
    HOSP = 2
    SURGERY = 3
    TREAT = 4
    OUTPATIENT = 5
    ADVANCED = 6
    DISCHARGE = 7
    LAPSE = 8
    ALL = 9
