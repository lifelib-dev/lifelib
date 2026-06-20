# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Per-policy cashflow projection and present values for one model point and scenario.

This is the user-facing Space of :mod:`~annuallife.TradLife_A`: each
ItemSpace ``Projection[idx, scen_id]`` projects the cashflows and
their present values for one policy under one scenario.

.. rubric:: Inheritance Structure

The ``Projection`` Space inherits its contents from its base Spaces,
:mod:`~annuallife.TradLife_A.BaseProj` and
:mod:`~annuallife.TradLife_A.PV`.
The projection cells are inherited from
:mod:`~annuallife.TradLife_A.BaseProj`, and the present values of those
cashflow items are inherited from :mod:`~annuallife.TradLife_A.PV`.

.. rubric:: Cells

In addition to the inherited cashflow and present-value Cells, this
Space defines :func:`risk_life`, the Solvency II life underwriting
capital requirement for each life sub-risk. It is the loss in the value
of in-force, i.e. the baseline less the stressed present value of
:func:`~annuallife.TradLife_A.PV.pv_net_cf`, taken from the inner
projection :mod:`~annuallife.TradLife_A.Projection.InnerProj`. It
mirrors ``SCR_life.Life`` in the ``solvency2`` library.

Parameters and References
-------------------------

This Space is parameterized with ``idx`` and ``scen_id``::

    >>> m.Projection.parameters
    ('idx', 'scen_id')

Calling this Space with a pair of integers returns the ItemSpace for
the policy index and scenario ID. ``scen_id`` has a default value of 1,
so for example ``Projection[0]`` represents the Projection Space for
the first policy under scenario 1.

Attributes:
    idx(:obj:`int`): 0-based policy index into the policy data array.
    scen_id(:obj:`int`, optional): Scenario ID, defaults to 1.

.. rubric:: References

The following references are inherited from
:mod:`~annuallife.TradLife_A.BaseProj`:

Attributes:
    pol: Alias for :mod:`~annuallife.TradLife_A.PolicyAttrs`.
    asmp: Alias for :mod:`~annuallife.TradLife_A.Assumptions`.
    scen: Alias for :mod:`~annuallife.TradLife_A.Economic`.
    comm_table: Alias for :mod:`~annuallife.TradLife_A.CommTable`.

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

def risk_life(t, risk):
    r"""Life underwriting capital requirement for ``risk`` at valuation time ``t``.

    The capital requirement for a life sub-risk is the loss in the value
    of in-force business caused by applying the prescribed Solvency II
    life stress: the baseline present value of net cashflows less the
    stressed present value, floored at zero.

    .. math::

        \mathrm{risk\_life}(t, risk) =
        \max\left(\mathrm{pv\_net\_cf}_{base}(t)
        - \mathrm{pv\_net\_cf}_{risk}(t),\; 0\right)

    Both present values are taken at the valuation time ``t`` from the
    inner projection :mod:`~annuallife.TradLife_A.Projection.InnerProj`,
    which is anchored at ``t``. ``InnerProj[t]`` is the unstressed
    (baseline) run, while ``InnerProj[t, risk]`` applies the life shock
    selected by ``risk``. For the lapse risk the requirement is the worst
    loss across the three prescribed lapse shocks (up, down and mass).

    This mirrors ``SCR_life.Life`` (and, for the lapse shocks,
    ``SCR_life.LapseRisk``) in the ``solvency2`` library, with
    :func:`~annuallife.TradLife_A.PV.pv_net_cf` standing in for the net
    asset value.

    Args:
        t: Valuation time at which the inner projection is anchored.
        risk: A :class:`~annuallife.TradLife_A.Enums.LifeRiskID.LifeRiskID`
            value selecting the life sub-risk (e.g. ``MORT``, ``LONGV``,
            ``LAPSE``, ``EXPS``).

    .. seealso::

        * :func:`~annuallife.TradLife_A.PV.pv_net_cf`
        * :mod:`~annuallife.TradLife_A.Projection.InnerProj`
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


# ---------------------------------------------------------------------------
# References

LifeRiskID = ("Interface", ("..", "Enums", "LifeRiskID"), "auto")

LapseShockID = ("Interface", ("..", "Enums", "LapseShockID"), "auto")