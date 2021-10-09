.. currentmodule:: lifelib.libraries

.. _relnotes_v0.3.0:

=================================
lifelib v0.3.0 (9 October 2021)
=================================

This release introduces a new library and some updates.

New Library
===============

The :mod:`savings` library is introduced.
The :mod:`savings` library is for
modeling savings products, such as universal life, unit-linked,
variable life and annuities.
The library includes two models, :mod:`~savings.CashValue_SE`
and :mod:`~savings.CashValue_ME`.
The models project cashflows
and account values of generic hypothetical savings products.
See :doc:`/libraries/savings/index` page for details.


Fixes and Updates
===================

* The inflation factor in :mod:`basiclife`
  is updated so that the factor is compounded every month instead of once every year.

    * :func:`basiclife.BasicTerm_S.Projection.inflation_factor`
    * :func:`basiclife.BasicTerm_M.Projection.inflation_factor`
    * :func:`basiclife.BasicTerm_SE.Projection.inflation_factor`
    * :func:`basiclife.BasicTerm_ME.Projection.inflation_factor`


* The formula of the number of lapse in :mod:`basiclife`
  is updated so that the number of lapse is based on the number of
  polices after deduction of the number of death.

    * :func:`basiclife.BasicTerm_S.Projection.pols_lapse`
    * :func:`basiclife.BasicTerm_M.Projection.pols_lapse`
    * :func:`basiclife.BasicTerm_SE.Projection.pols_lapse`
    * :func:`basiclife.BasicTerm_ME.Projection.pols_lapse`

.. currentmodule:: lifelib.projects

* The base spaces of
  :mod:`ifrs17sim.model.OuterProj` are now in the order of
  :mod:`~ifrs17sim.model.IFRS` and :mod:`~ifrs17sim.model.BaseProj`.
