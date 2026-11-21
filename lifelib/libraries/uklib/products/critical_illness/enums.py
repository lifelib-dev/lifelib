"""Closed sets used by the CI_UK_S saved model."""

from enum import IntEnum


class ContractType(IntEnum):
    accelerated = 0
    standalone = 1


class LifeBasis(IntEnum):
    single = 0
    joint_first_event = 1


class Sex(IntEnum):
    M = 0
    F = 1


class Smoker(IntEnum):
    NS = 0
    S = 1


class CoverBasis(IntEnum):
    level = 0


class PremiumGuarantee(IntEnum):
    guaranteed = 0
    reviewable = 1


class PremiumMode(IntEnum):
    monthly = 0
    annual = 1


class RateColumn(IntEnum):
    i_ci = 0
    q_d = 1


class PolTiming(IntEnum):
    BEF_DECR = 0
    BEF_LAPSE = 1
    AFT_DECR = 2


class BenefitKind(IntEnum):
    MAIN = 0
    AP = 1
    CHILD = 2


class Kind(IntEnum):
    MAIN = 0
    AP = 1
    CHILD = 2
    LAPSE = 3
    ALL = 4
