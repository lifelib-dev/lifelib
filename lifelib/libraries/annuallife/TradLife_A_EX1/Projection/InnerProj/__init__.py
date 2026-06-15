# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

from modelx.serialize.jsonvalues import *

_formula = lambda t0, risk=0, shock=0: None

_bases = [
    "..BaseProj",
    "..PV"
]

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def pols_if(t):
    """Number of policies: End of period"""
    if t == t0:
        return _space._parent._parent.pols_if(t) #_parent._parent # pol.policy_count
    else:
        return pols_if_beg1(t-1) - pols_death(t-1) - pols_lapse(t-1)


def lapse_rate(t):
    """Surrender Rate"""
    if not risk == LifeRiskID.LAPSE:
        return base_lapse_rate(t)

    elif shock == LapseShockID.UP:
        shock_factor = 1 + asmp.life_shock_param(risk, shock)
        shock_limit = asmp.life_shock_param(risk, shock, extra_key=ExtraKeyID.LIMIT)
        return min(shock_factor * base_lapse_rate(t), shock_limit)

    elif shock == LapseShockID.DOWN:
        shock_factor = 1 - asmp.life_shock_param(risk, shock)
        shock_limit = asmp.life_shock_param(risk, shock, extra_key=ExtraKeyID.LIMIT)
        return max(shock_factor * base_lapse_rate(t), base_lapse_rate(t) - shock_limit)

    elif shock == LapseShockID.MASS:
        if t == t0:
            shock_lapse = asmp.life_shock_param(risk, shock, pol.segment()[idx])
            return shock_lapse
        else:
            return base_lapse_rate(t)

    else:
        raise ValueError(f'invalid lapse shock id: {shock}')


def mort_rate(x):
    """Mortality rate at age ``x`` with the mortality / longevity shock applied.

    Under the ``MORT`` risk the base mortality rate is increased and
    under the ``LONGV`` risk it is decreased, by the factor read from
    the ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A.Assumptions.life_shock_param`. For any
    other risk the base rate is returned unchanged.
    """
    if risk == LifeRiskID.MORT:
        return base_mort_rate(x) * (1 + asmp.life_shock_param(risk))

    elif risk == LifeRiskID.LONGV:
        return base_mort_rate(x) * (1 - asmp.life_shock_param(risk))

    else:
        return base_mort_rate(x)


def expense_acq_pp(t):
    """Acquisition expense per policy with the expense shock applied.

    Under the ``EXPS`` risk the base acquisition expense is increased by
    the factor read from the ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A.Assumptions.life_shock_param`. For any
    other risk the base amount is returned unchanged.
    """
    if risk == LifeRiskID.EXPS:
        return base_expense_acq_pp(t) * (1 + asmp.life_shock_param(risk))

    else:
        return base_expense_acq_pp(t)


def expense_maint_pp(t):
    """Maintenance expense per policy with the expense shock applied.

    Under the ``EXPS`` risk the base maintenance expense is increased by
    the factor read from the ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A.Assumptions.life_shock_param`. For any
    other risk the base amount is returned unchanged.
    """
    if risk == LifeRiskID.EXPS:
        return base_expense_maint_pp(t) * (1 + asmp.life_shock_param(risk))

    else:
        return base_expense_maint_pp(t)


def commissions_ren_pp(t):
    """Renewal commission per policy with the expense shock applied.

    Under the ``EXPS`` risk the base renewal commission is increased by
    the factor read from the ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A.Assumptions.life_shock_param`. For any
    other risk the base amount is returned unchanged.
    """
    if risk == LifeRiskID.EXPS:
        return base_commissions_ren_pp(t) * (1 + asmp.life_shock_param(risk))

    else:
        return base_commissions_ren_pp(t)


# ---------------------------------------------------------------------------
# References

LifeRiskID = ("Interface", ("...", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("...", "Enums", "LapseShockID"), "auto")

LapseScopeID = ("Interface", ("...", "Enums", "LapseScopeID"), "auto")

ExtraKeyID = ("Interface", ("...", "Enums", "ExtraKeyID"), "auto")