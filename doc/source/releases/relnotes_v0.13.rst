.. currentmodule:: lifelib.libraries

==================================
lifelib v0.13 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.13.0:

lifelib v0.13.0 (28 June 2026)
==================================

New Model
----------------

This release adds a new model, :mod:`~annuallife.TradLife_A_EX1`, to the
:mod:`~annuallife` library. :mod:`~annuallife.TradLife_A_EX1` is a
nested-projection example derived from :mod:`~annuallife.TradLife_A`
that demonstrates how to build a Solvency II Life capital calculation
at each projection step. Each nested valuation is modelled by
``Projection.InnerProj[t0, risk, shock]``, which re-runs the policy
projection from the valuation time ``t0`` under a stressed assumption set.

The model applies the prescribed Solvency II life sub-risk shocks
(lapse up, down and mass, mortality, longevity and expense) inside the
inner projection, computes the loss in the value of in-force under each
shock as ``risk_life_sub(t, risk)``, aggregates the sub-risks into the
life SCR ``risk_life(t)`` using the prescribed correlation matrix, and
derives the cost-of-capital ``risk_margin(t)``. Example plot scripts for the SCR
cashflows, the life-risk radar charts and the lapse-up in-force run-off
are included.

:mod:`~annuallife.TradLife_A_EX1` supersedes the legacy :mod:`~solvency2`
project, which is now deprecated.

Changes
------------

* lifelib now requires Python 3.9 or newer. The packaging metadata in
  ``setup.py`` and ``pyproject.toml`` is reconciled to drop Python 3.7
  and 3.8 and add Python 3.14 (``requires-python >= 3.9``), enforcing at
  install time the support policy first announced in v0.12.0.

* ``disc_rate_mth`` is renamed to ``disc_rate`` across the
  :mod:`~annuallife` traditional-life models
  (:mod:`~annuallife.TradLife_A`, ``TradLife_A_EX1`` and
  ``TradLife_A_mx30``). The cell holds an annual discount rate, so the
  ``_mth`` suffix was a misnomer. Numerical results are unchanged.

* In :mod:`~annuallife.TradLife_A`, the present-value outflow cells in
  the ``PV`` Space (claims, expenses and commissions) now return their
  present values as positive amounts, and ``pv_net_cf`` subtracts them
  from ``pv_premiums``. The value of ``pv_net_cf`` is unchanged.

* ``InputData.get_named_range_as_dict`` is generalised to support named
  ranges with more than two columns, building a tuple key from the
  left-hand columns and taking the right-most column as the value
  (two-column ranges keep scalar keys as before). The enhancement is
  applied across :mod:`~annuallife.TradLife_A`, ``TradLife_A_EX1`` and
  ``TradLife_A_mx30``.

* The :mod:`~solvency2` project is deprecated and superseded by
  :mod:`~annuallife.TradLife_A_EX1`. A deprecation notice is added to the
  affected page.

* The documentation for :mod:`~annuallife.TradLife_A` is substantially
  expanded, including per-Space docstrings, actuarial formulas for
  ``net_prem_rate`` and ``reserve_nlp_rate``, an Input File reference with
  per-named-range subsections, and additional model-structure diagrams.

Fixes
------------

* ``inflation_factor`` in the :mod:`~annuallife` models
  (:mod:`~annuallife.TradLife_A` and ``TradLife_A_mx30``) now compounds
  upward as ``(1 + rate) ** t`` instead of dividing by ``(1 + rate)``,
  matching its docstring. The shipped input has ``InflRate = 0``, so
  existing results are numerically unchanged.
