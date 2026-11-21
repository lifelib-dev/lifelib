"""Closed sets used by the LTC_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class Grade(IntEnum):
    g1 = 0
    g2 = 1
    g3 = 2
    g4 = 3
    g5 = 4
    g6 = 5


class PremMode(IntEnum):
    monthly = 0


class CvForm(IntEnum):
    mijigeup = 0
    half_during = 1
    pyojun = 2


class LapseForm(IntEnum):
    mujihae = 0
    pyojun = 1


class LapseParam(IntEnum):
    lapse_year1 = 0
    lapse_completion = 1
    lapse_ultimate = 2
    lapse_level_std = 3


class PrevParam(IntEnum):
    prev_ceil = 0
    prev_beta = 1
    prev_x_mid = 2
    prev_obs_67 = 3
    prev_obs_72 = 4
    prev_obs_77 = 5
    prev_obs_82 = 6
    prev_obs_88 = 7


class DemParam(IntEnum):
    dem_ceil = 0
    dem_beta = 1
    dem_x_mid = 2
    dem_factor_m = 3
    dem_factor_f = 4
    dem_obs_67 = 5
    dem_obs_72 = 6
    dem_obs_77 = 7
    dem_obs_82 = 8
    dem_obs_88 = 9


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    LUMP = 0
    ANNUITY = 1
    DEMENTIA = 2
    DEATH = 3
    LAPSE = 4
    VOID = 5
    MATURITY = 6
    ALL = 7
