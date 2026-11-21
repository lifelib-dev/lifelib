"""Closed sets used by the UC_FR_S saved model."""

from enum import IntEnum


class Sex(IntEnum):
    M = 0
    F = 1


class PlancherBasis(IntEnum):
    simple = 0
    indexee = 1
    cliquet = 2


class LevySource(IntEnum):
    euro_first = 0
    uc_units = 1


class WdPattern(IntEnum):
    none = 0
    one_off = 1
    programmed = 2


class ArbPattern(IntEnum):
    none = 0
    one_off = 1
    progressive = 2


class LapseDynamic(IntEnum):
    none = 0
    full = 1


class AvTiming(IntEnum):
    OPENING = 0
    BEF_FEE = 1
    BEF_WD = 2
    BEF_LEVY = 3
    BEF_DECR = 4


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class Kind(IntEnum):
    DEATH = 0
    LAPSE = 1
    ALL = 2
