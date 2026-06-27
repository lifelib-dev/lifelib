# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Inner projection that re-runs the cashflows under a single life stress.

This Space is the engine behind the Solvency II life-risk results in
:mod:`~annuallife.TradLife_A_EX1.Projection`. Each ItemSpace
``InnerProj[t0, risk, shock]`` re-runs the per-policy projection from the
valuation time ``t0`` under one prescribed life stress, so that the
stressed present value of net cashflows can be compared with the
unstressed (baseline) one by
:func:`~annuallife.TradLife_A_EX1.Projection.risk_life_sub`.

It inherits all cashflow and present-value Cells from
:mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>` and
:mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`, and overrides only the Cells needed to
anchor the projection at ``t0`` and to apply the stress. The unstressed
mortality, lapse and renewal-commission rates are taken from the outer
projection and scaled by the shock; the acquisition and maintenance
expenses are recomputed locally so they pick up the stressed
:func:`inflation_factor`.

Parameters and References
-------------------------

Attributes:
    t0(:obj:`int`): Valuation time the inner projection is anchored at;
        at ``t0`` the in-force equals that of the outer projection.
    risk(:obj:`int`, optional): A ``LifeRiskID`` code selecting the life
        sub-risk to stress. Defaults to ``BASE`` (0), the unstressed run.
    shock(:obj:`int`, optional): A ``LapseShockID`` code selecting the
        lapse shock (``UP``, ``DOWN`` or ``MASS``) when ``risk`` is
        ``LAPSE``. Defaults to 0.

Cells Summary
-------------

Overridden Cells
^^^^^^^^^^^^^^^^

The following Cells override their
:mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>` counterparts to anchor the
projection at ``t0`` and to apply the life shocks.

.. autosummary::

   ~pols_if
   ~pols_if_beg1
   ~pols_lapse_mass
   ~claims_surr
   ~claims_surr_mass_pp
   ~mort_rate
   ~lapse_rate
   ~expense_acq_pp
   ~expense_maint_pp
   ~commissions_ren_pp
   ~inflation_factor

"""

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
    :func:`TradLife_A.PV.pv_net_cf <annuallife.TradLife_A.PV.pv_net_cf>` at ``t0``), so the
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
    selected by :func:`~annuallife.TradLife_A_EX1.PolicyAttrs.segment`) of
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
    :func:`TradLife_A.BaseProj.claims_surr_pp <annuallife.TradLife_A.BaseProj.claims_surr_pp>` pays the
    mid-period average of the cash value at ``t`` and ``t+1``. The
    mass-lapse surrenders, by contrast, occur instantaneously at the
    valuation time, so the benefit is the cash value at time ``t`` only
    (:func:`TradLife_A.BaseProj.cash_value_rate <annuallife.TradLife_A.BaseProj.cash_value_rate>` at ``t``).
    """
    return sum_assured(t) * cash_value_rate(t)


def claims_surr(t):
    """Surrender benefits.

    Overrides the base cell so the surrender benefit is paid on both the
    ongoing surrenders (:func:`pols_lapse`) and the instantaneous
    mass-lapse surrenders (:func:`pols_lapse_mass`). The ongoing
    surrenders receive the mid-period average cash value
    (:func:`TradLife_A.BaseProj.claims_surr_pp <annuallife.TradLife_A.BaseProj.claims_surr_pp>`), while the
    mass-lapse surrenders receive the cash value at time ``t``
    (:func:`claims_surr_mass_pp`).
    """
    return (claims_surr_pp(t) * pols_lapse(t)
            + claims_surr_mass_pp(t) * pols_lapse_mass(t))


def lapse_rate(t):
    """Surrender Rate

    The unstressed rate is taken from the outer projection
    (:func:`TradLife_A.BaseProj.lapse_rate <annuallife.TradLife_A.BaseProj.lapse_rate>`); the lapse-up /
    lapse-down shocks scale it (capped by the ``LIMIT`` factor), while the
    mass-lapse shock leaves the ongoing rate unchanged (it is modelled by
    :func:`pols_lapse_mass` instead).
    """
    base = _space._parent._parent.lapse_rate(t)

    if not risk == LifeRiskID.LAPSE:
        return base

    elif shock == LapseShockID.UP:
        shock_factor = 1 + asmp.life_shock_param(risk, shock)
        shock_limit = asmp.life_shock_param(risk, shock, extra_key=ExtraKeyID.LIMIT)
        return min(shock_factor * base, shock_limit)

    elif shock == LapseShockID.DOWN:
        shock_factor = 1 - asmp.life_shock_param(risk, shock)
        shock_limit = asmp.life_shock_param(risk, shock, extra_key=ExtraKeyID.LIMIT)
        return max(shock_factor * base, base - shock_limit)

    elif shock == LapseShockID.MASS:
        # The mass-lapse shock is an instantaneous discontinuance at t0
        # modelled by pols_lapse_mass / pols_if_beg1, not an elevated
        # surrender rate; ongoing surrenders stay at the base rate.
        return base

    else:
        raise ValueError(f'invalid lapse shock id: {shock}')


def mort_rate(x):
    """Mortality rate at age ``x`` with the mortality / longevity shock applied.

    The unstressed rate is taken from the outer projection
    (:func:`TradLife_A.BaseProj.mort_rate <annuallife.TradLife_A.BaseProj.mort_rate>`). Under the
    ``MORT`` risk it is increased and under the ``LONGV`` risk it is
    decreased, by the factor read from the ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param`. For any
    other risk the unstressed rate is returned unchanged.
    """
    base = _space._parent._parent.mort_rate(x)

    if risk == LifeRiskID.MORT:
        return base * (1 + asmp.life_shock_param(risk))

    elif risk == LifeRiskID.LONGV:
        return base * (1 - asmp.life_shock_param(risk))

    else:
        return base


def expense_acq_pp(t):
    """Acquisition expense per policy with the expense shock applied.

    Recomputes the acquisition expense locally (mirroring
    :func:`TradLife_A.BaseProj.expense_acq_pp <annuallife.TradLife_A.BaseProj.expense_acq_pp>`) so it uses
    this Space's stressed :func:`inflation_factor`, then under the
    ``EXPS`` risk increases it by the factor read from the ``LifeShocks``
    input via
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param`. For any
    other risk the unstressed amount is returned.
    """
    if t == 0:
        base = (ann_prem_pp(t) * asmp.exps_acq_ann_prem()[idx]
                + (sum_assured(t) * asmp.exps_acq_sa()[idx] + asmp.exps_acq_pol()[idx])
                * inflation_factor(t) / inflation_factor(0))
    else:
        base = 0

    if risk == LifeRiskID.EXPS:
        return base * (1 + asmp.life_shock_param(risk))

    else:
        return base


def expense_maint_pp(t):
    """Maintenance expense per policy with the expense shock applied.

    Recomputes the maintenance expense locally (mirroring
    :func:`TradLife_A.BaseProj.expense_maint_pp <annuallife.TradLife_A.BaseProj.expense_maint_pp>`) so it uses
    this Space's stressed :func:`inflation_factor`, then under the
    ``EXPS`` risk increases it by the factor read from the ``LifeShocks``
    input via
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param`. For any
    other risk the unstressed amount is returned.
    """
    base = (ann_prem_pp(t) * asmp.exps_maint_ann_prem()[idx]
            + (sum_assured(t) * asmp.exps_maint_sa()[idx] + asmp.exps_maint_pol()[idx])
            * inflation_factor(t))

    if risk == LifeRiskID.EXPS:
        return base * (1 + asmp.life_shock_param(risk))

    else:
        return base


def commissions_ren_pp(t):
    """Renewal commission per policy with the expense shock applied.

    The unstressed renewal commission is taken from the outer projection
    (:func:`TradLife_A.BaseProj.commissions_ren_pp <annuallife.TradLife_A.BaseProj.commissions_ren_pp>`); under
    the ``EXPS`` risk it is increased by the factor read from the
    ``LifeShocks`` input via
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param`. For any
    other risk the unstressed amount is returned unchanged.
    """
    base = _space._parent._parent.commissions_ren_pp(t)

    if risk == LifeRiskID.EXPS:
        return base * (1 + asmp.life_shock_param(risk))

    else:
        return base


def inflation_factor(t):
    """Expense inflation factor with the expense-inflation shock applied.

    Overrides :func:`TradLife_A.BaseProj.inflation_factor <annuallife.TradLife_A.BaseProj.inflation_factor>` to
    compound at a stressed inflation rate under the ``EXPS`` risk: the
    base rate plus the ``INFL`` factor read from the ``LifeShocks`` input
    via :func:`~annuallife.TradLife_A_EX1.Assumptions.life_shock_param` (a +1
    percentage-point stress). The locally recomputed expenses
    (:func:`expense_maint_pp`, :func:`expense_acq_pp`) therefore inflate
    faster. For any other risk it equals the unstressed factor.
    """
    if t == 0:
        return 1

    rate = asmp.inflation_rate()
    if risk == LifeRiskID.EXPS:
        rate += asmp.life_shock_param(risk, extra_key=ExtraKeyID.INFL)

    return inflation_factor(t - 1) * (1 + rate)


# ---------------------------------------------------------------------------
# References

LifeRiskID = ("Interface", ("...", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("...", "Enums", "LapseShockID"), "auto")

LapseScopeID = ("Interface", ("...", "Enums", "LapseScopeID"), "auto")

ExtraKeyID = ("Interface", ("...", "Enums", "ExtraKeyID"), "auto")