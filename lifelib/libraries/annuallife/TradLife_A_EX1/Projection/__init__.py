# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Per-policy projection, present values and Solvency II life-risk results.

This Space is :mod:`TradLife_A.Projection <annuallife.TradLife_A.Projection>` with the Solvency
II life-risk outputs added and a new inner projection child Space. The
parameters (``idx``, ``scen_id``), the inherited cashflow Cells (from
:mod:`TradLife_A.BaseProj <annuallife.TradLife_A.BaseProj>`) and present-value Cells (from
:mod:`TradLife_A.PV <annuallife.TradLife_A.PV>`) are unchanged; see
:mod:`TradLife_A.Projection <annuallife.TradLife_A.Projection>`.

.. rubric:: New child Space

:mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj` re-runs the
cashflows under a single prescribed life stress, anchored at a valuation
time ``t0``.

Cells Summary
-------------

New Cells
^^^^^^^^^

:func:`risk_life_sub` is the capital requirement for a single life
sub-risk -- the loss in :func:`TradLife_A.PV.pv_net_cf <annuallife.TradLife_A.PV.pv_net_cf>` under
the stress, floored at zero. :func:`risk_life` aggregates the sub-risks
with the correlation matrix from
:func:`~annuallife.TradLife_A_EX1.Assumptions.life_corr`.
:func:`risk_margin` is the Solvency II risk margin: the cost-of-capital
rate :func:`~annuallife.TradLife_A_EX1.Assumptions.coc_rate` applied to
the projected :func:`risk_life`, discounted to ``t``.

.. autosummary::

   ~risk_life_sub
   ~risk_life
   ~risk_margin

"""

from modelx.serialize.jsonvalues import *

_formula = lambda idx, scen_id=1: None

_bases = [
    ".BaseProj",
    ".PV"
]

_allow_none = None

_spaces = [
    "InnerProj"
]

# ---------------------------------------------------------------------------
# Cells

def risk_life_sub(t, risk):
    r"""Life underwriting capital requirement for sub-risk ``risk`` at time ``t``.

    The capital requirement for a single life sub-risk is the loss in the
    value of in-force business caused by applying the prescribed
    Solvency II life stress: the baseline present value of net cashflows
    less the stressed present value, floored at zero.

    .. math::

        \mathrm{risk\_life\_sub}(t, risk) =
        \max\left(\mathrm{pv\_net\_cf}_{base}(t)
        - \mathrm{pv\_net\_cf}_{risk}(t),\; 0\right)

    Both present values are taken at the valuation time ``t`` from the
    inner projection :mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`,
    which is anchored at ``t``. ``InnerProj[t]`` is the unstressed
    (baseline) run, while ``InnerProj[t, risk]`` applies the life shock
    selected by ``risk``. For the lapse risk the requirement is the worst
    loss across the three prescribed lapse shocks (up, down and mass).

    The individual sub-risk requirements are aggregated into the total
    life underwriting requirement by :func:`risk_life`.

    This mirrors ``SCR_life.Life`` (and, for the lapse shocks,
    ``SCR_life.LapseRisk``) in the ``solvency2`` library, with
    :func:`TradLife_A.PV.pv_net_cf <annuallife.TradLife_A.PV.pv_net_cf>` standing in for the net
    asset value.

    Args:
        t: Valuation time at which the inner projection is anchored.
        risk: A ``LifeRiskID``
            value selecting the life sub-risk (e.g. ``MORT``, ``LONGV``,
            ``LAPSE``, ``EXPS``).

    .. seealso::

        * :func:`risk_life`
        * :func:`TradLife_A.PV.pv_net_cf <annuallife.TradLife_A.PV.pv_net_cf>`
        * :mod:`~annuallife.TradLife_A_EX1.Projection.InnerProj`
    """
    base_pv = InnerProj[t].pv_net_cf(t)

    if risk == LifeRiskID.LAPSE:
        return max(
            max(base_pv - InnerProj[t, risk, shock].pv_net_cf(t), 0)
            for shock in (LapseShockID.UP,
                          LapseShockID.DOWN,
                          LapseShockID.MASS))
    else:
        return max(base_pv - InnerProj[t, risk].pv_net_cf(t), 0)


def risk_life(t):
    r"""Aggregated life underwriting capital requirement at valuation time ``t``.

    The individual life sub-risk requirements :func:`risk_life_sub` are
    combined with the prescribed life-risk correlation matrix:

    .. math::

        \mathrm{risk\_life}(t) =
        \sqrt{\sum_{i,j} Corr_{i,j}\,
        \mathrm{risk\_life\_sub}(t, i)\,\mathrm{risk\_life\_sub}(t, j)}

    where ``i`` and ``j`` range over the life sub-risks and
    :math:`Corr_{i,j}` is the correlation coefficient between them,
    supplied per pair by
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_corr`.

    This mirrors ``SCR_life.SCR_life`` in the ``solvency2`` library,
    parameterized by the valuation time ``t``. The aggregation is kept on
    native scalar types (a tuple of integer risk codes, with
    :func:`risk_life_sub` and
    :func:`~annuallife.TradLife_A_EX1.Assumptions.life_corr` returning
    :obj:`float`) so the Space stays efficient when compiled with Cython.

    Args:
        t: Valuation time at which the inner projections are anchored.

    .. seealso::

        * :func:`risk_life_sub`
        * :func:`~annuallife.TradLife_A_EX1.Assumptions.life_corr`
    """
    risks = (LifeRiskID.MORT, LifeRiskID.LONGV, LifeRiskID.DISAB,
             LifeRiskID.LAPSE, LifeRiskID.EXPS, LifeRiskID.REV,
             LifeRiskID.CAT)
    return sum(risk_life_sub(t, i) * risk_life_sub(t, j) * asmp.life_corr(i, j)
               for i in risks for j in risks) ** 0.5


def risk_margin(t):
    r"""Solvency II risk margin at valuation time ``t``.

    The risk margin is the cost of holding the future life underwriting
    capital over the run-off of the in-force business: the
    cost-of-capital rate
    :func:`~annuallife.TradLife_A_EX1.Assumptions.coc_rate` applied to each
    future aggregated life SCR :func:`risk_life`, discounted to ``t``.

    .. math::

        \mathrm{risk\_margin}(t) = \mathrm{CoC}
        \sum_{s=t}^{\mathrm{proj\_len}}
        \frac{\mathrm{risk\_life}(s)}
        {\prod_{u=t}^{s}\left(1 + \mathrm{disc\_rate}(u)\right)}

    The cost of capital for the capital held over year ``[s, s+1]`` is
    taken to be incurred at ``s + 1``, so each ``risk_life(s)`` is
    discounted by ``s - t + 1`` periods (the standard EIOPA convention).
    This is evaluated by the recursion

    .. math::

        \mathrm{risk\_margin}(t) =
        \frac{\mathrm{CoC}\cdot\mathrm{risk\_life}(t)
        + \mathrm{risk\_margin}(t + 1)}
        {1 + \mathrm{disc\_rate}(t)}

    which terminates at ``0`` once ``t`` is beyond
    :func:`TradLife_A.BaseProj.proj_len <annuallife.TradLife_A.BaseProj.proj_len>`. At ``t = 0`` it is
    the risk margin at the valuation date.

    Args:
        t: Valuation time at which the risk margin is evaluated.

    .. seealso::

        * :func:`risk_life`
        * :func:`~annuallife.TradLife_A_EX1.Assumptions.coc_rate`
    """
    if t > proj_len():
        return 0
    else:
        return (asmp.coc_rate() * risk_life(t)
                + risk_margin(t + 1)) / (1 + disc_rate(t))


# ---------------------------------------------------------------------------
# References

LifeRiskID = ("Interface", ("..", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("..", "Enums", "LapseShockID"), "auto")