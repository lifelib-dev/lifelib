"""Closed sets used by the Cancer_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Chassis(IntEnum):
    bi_gaengsin = 0
    gaengsin = 1


class WaiverTrigger(IntEnum):
    cancer_diag = 0
    none = 1


class CvForm(IntEnum):
    mijigeup = 0
    pyojun = 1


class Tier(IntEnum):
    high = 0
    general = 1
    minor = 2
    similar = 3


class Segment(IntEnum):
    first_year = 0
    at_completion = 1
    post_payment = 2


class ShareColumn(IntEnum):
    minor_share = 0
    high_share = 1
    similar_share = 2


class PolTiming(IntEnum):
    BEF_DECR = 0
    AFT_DECR = 1
    BEF_LAPSE = 2


class Kind(IntEnum):
    DIAG_GEN = 0
    DIAG_HIGH = 1
    DIAG_MINOR = 2
    DIAG_SIMILAR = 3
    HOSP = 4
    SURGERY = 5
    TREAT = 6
    DEATH = 7
    LAPSE = 8
    MATURITY = 9
    ALL = 10
