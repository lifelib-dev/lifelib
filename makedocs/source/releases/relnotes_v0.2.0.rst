.. currentmodule:: lifelib.libraries

.. _relnotes_v0.2.0:

================================
lifelib v0.2.0 (28 August 2021)
================================

.. rubric:: Introduction of in-force models in :mod:`basiclife`

This release introduces two new models,
:mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`
in the :mod:`basiclife` library.
While
:mod:`~basiclife.BasicTerm_M` and :mod:`~basiclife.BasicTerm_S`
are new business models,
:mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`
are in-force projection models
which project the cashflows of in-force policies at time 0 and
new business policies at 0 or any future time.


.. rubric:: Updated items

* :mod:`basiclife.BasicTerm_S.Projection.premium_pp`
* :mod:`basiclife.BasicTerm_M.Projection.premium_pp`
* :mod:`basiclife.BasicTerm_S.Projection.expenses`
* :mod:`basiclife.BasicTerm_M.Projection.expenses`
* :mod:`basiclife.BasicTerm_S.Projection.mort_rate`
* Cells are now sorted alphabetically.




