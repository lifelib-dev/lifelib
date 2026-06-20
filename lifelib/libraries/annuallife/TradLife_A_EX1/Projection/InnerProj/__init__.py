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
    """Number of policies: End of period.

    The inner projection is anchored at the valuation time ``t0`` (where
    this returns the outer projection's in-force) and is defined only for
    ``t >= t0``. Present values are taken at ``t0`` (e.g.
    :func:`~annuallife.TradLife_A.PV.pv_net_cf` at ``t0``), so the
    ``t < t0`` region is never reached in normal use; evaluating any
    in-force cell there would recurse without terminating.
    """
    if t == t0:
        return _space._parent._parent.pols_if(t) #_parent._parent # pol.policy_count
    else:
        return pols_if_beg1(t-1) - pols_death(t-1) - pols_lapse(t-1)


def pols_lapse_mass(t):
    """Number of policies that instantly surrender under the mass-lapse shock.

    Solvency II models mass lapse as an instantaneous discontinuance at
    the valuation time ``t0`` rather than an elevated surrender rate
    spread over the year. At ``t == t0`` a segment-dependent fraction
    (the ``LAPSE`` / ``MASS`` factor from the ``LifeShocks`` input,
    selected by :func:`~annuallife.TradLife_A.PolicyAttrs.segment`) of
    the policies in force at the beginning of the period instantly
    surrenders. The amount is removed from :func:`pols_if_beg1` so those
    policies neither pay premiums nor are exposed to mortality or ongoing
    lapse during the period, and is added to the surrender benefit in
    :func:`claims_surr`. It is zero for every other risk / shock and for
    ``t != t0``.

    Mirrors ``Override.LapseMass.PolsSurrMass`` in the ``solvency2``
    library.
    """
    if t == t0 and risk == LifeRiskID.LAPSE and shock == LapseShockID.MASS:
        factor = asmp.life_shock_param(risk, shock, pol.segment()[idx])
    else:
        factor = 0

    return (pols_if_beg(t) + pols_renewal(t) + pols_if_init(t)) * factor


def pols_if_beg1(t):
    """Number of policies: Beginning of period 1.

    Overrides the base cell to remove the instantaneous mass-lapse
    surrenders (:func:`pols_lapse_mass`) from the in-force at the start
    of the period, so the mass lapsers drop out instantly under the
    Solvency II mass-lapse shock. Identical to the base cell for every
    other risk / shock, where :func:`pols_lapse_mass` is zero.
    """
    return pols_if_beg(t) + pols_renewal(t) + pols_if_init(t) - pols_lapse_mass(t)


def claims_surr_mass_pp(t):
    """Surrender benefit per policy for the instantaneous mass-lapse surrenders.

    The ongoing surrenders are assumed to occur throughout the period, so
    :func:`~annuallife.TradLife_A.BaseProj.claims_surr_pp` pays the
    mid-period average of the cash value at ``t`` and ``t+1``. The
    mass-lapse surrenders, by contrast, occur instantaneously at the
    valuation time, so the benefit is the cash value at time ``t`` only
    (:func:`~annuallife.TradLife_A.BaseProj.cash_value_rate` at ``t``).
    """
    return sum_assured(t) * cash_value_rate(t)


def claims_surr(t):
    """Surrender benefits.

    Overrides the base cell so the surrender benefit is paid on both the
    ongoing surrenders (:func:`pols_lapse`) and the instantaneous
    mass-lapse surrenders (:func:`pols_lapse_mass`). The ongoing
    surrenders receive the mid-period average cash value
    (:func:`~annuallife.TradLife_A.BaseProj.claims_surr_pp`), while the
    mass-lapse surrenders receive the cash value at time ``t``
    (:func:`claims_surr_mass_pp`).
    """
    return (claims_surr_pp(t) * pols_lapse(t)
            + claims_surr_mass_pp(t) * pols_lapse_mass(t))


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
        # The mass-lapse shock is an instantaneous discontinuance at t0
        # modelled by pols_lapse_mass / pols_if_beg1, not an elevated
        # surrender rate; ongoing surrenders stay at the base rate.
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


def inflation_rate():
    """Expense inflation rate with the expense-inflation shock applied.

    Under the ``EXPS`` risk the base expense inflation rate is increased
    by the ``INFL`` factor read from the ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A.Assumptions.life_shock_param` (a +1
    percentage-point stress to the annual expense inflation rate). The
    inherited :func:`~annuallife.TradLife_A.BaseProj.inflation_factor`
    then compounds at this stressed rate, so future expense cashflows
    inflate faster. For any other risk the base rate is returned
    unchanged.
    """
    if risk == LifeRiskID.EXPS:
        return asmp.inflation_rate() + asmp.life_shock_param(risk, extra_key=ExtraKeyID.INFL)

    else:
        return asmp.inflation_rate()


# ---------------------------------------------------------------------------
# References

LifeRiskID = ("Interface", ("...", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("...", "Enums", "LapseShockID"), "auto")

LapseScopeID = ("Interface", ("...", "Enums", "LapseScopeID"), "auto")

ExtraKeyID = ("Interface", ("...", "Enums", "ExtraKeyID"), "auto")