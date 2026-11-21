"""Closed sets used by the Medical_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Stream(IntEnum):
    ge_in = 0
    ge_out = 1
    np_in = 2
    np_room = 3
    np_out = 4
    physio = 5
    inject = 6
    mri = 7


class UtilColumn(IntEnum):
    adm_rate = 0
    los_days = 1
    visit_rate_ge = 2
    visit_rate_np = 3
    act_rate_physio = 4
    act_rate_inject = 5
    act_rate_mri = 6


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    BEF_SUSPEND = 2
    BEF_RENEWAL = 3
    AFT_DECR = 4


class Kind(IntEnum):
    GE_IN = 0
    GE_OUT = 1
    NP_IN = 2
    NP_OUT = 3
    NP_THREE = 4
    ALL = 5
