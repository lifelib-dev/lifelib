"""Closed sets used by the Child_KR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class CvForm(IntEnum):
    std = 0
    susp = 1
    graded = 2


class LapseBasis(IntEnum):
    loglinear = 0
    disclosed = 1
    flat = 2


class LapseColumn(IntEnum):
    first_year_rate = 0
    completion_rate = 1
    ultimate_rate = 2


class Cover(IntEnum):
    disability = 0
    disease_disab = 1
    cancer = 2
    minor_cancer = 3
    cerebral = 4
    cardiac = 5
    surgery = 6
    fracture = 7
    burn = 8
    hosp_acc = 9
    hosp_dis = 10
    liability = 11
    neonatal = 12


class Kind(IntEnum):
    DISABILITY = 0
    DIAGNOSIS = 1
    SURGERY = 2
    HOSPITAL = 3
    EVENT = 4
    LIABILITY = 5
    NEONATAL = 6
    DEATH = 7
    LAPSE = 8
    MATURITY = 9
    VOID = 10
    ALL = 11


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class NeoTiming(IntEnum):
    birth = 0
    block = 1


class BasisParam(IntEnum):
    disab_severity = 0
    disease_disab_severity = 1
    surgery_rate_cancer = 2
    surgery_rate_cerebral = 3
    surgery_rate_cardiac = 4
    liability_severity = 5
    hosp_cap_factor = 6
    waiver_disab_share = 7
    payer_disab_ratio = 8
    leak_share = 9
    void_rate_ann = 10
    broad_def_factor = 11
    net_prem_ratio = 12


class AvCurve(IntEnum):
    build = 0
    taper = 1
