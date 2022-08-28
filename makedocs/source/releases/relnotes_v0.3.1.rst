.. currentmodule:: lifelib.libraries

.. _relnotes_v0.3.1:

=================================
lifelib v0.3.1 (24 October 2021)
=================================

This release adds a new example in the :mod:`~savings` library,
and updates some formulas in the :mod:`~savings` models.

To update lifelib, execute the command::

    >>> pip install lifelib --upgrade


New Example
===============

An example is added to the :mod:`~savings` library.
This example shows how to extend :mod:`~savings.CashValue_ME`
to a stochastic model,
by going through a classic exercise of calculating the time value of options and guarantees
on a plain variable annuity with GMAB by two methods,
the Black-Scholes-Merton formula and Monte Carlo simulation with risk-neutral scenarios.

This example consists of an example model, a Jupyter notebook
and some Python scripts.
The model is developed from :mod:`~savings.CashValue_ME` and named ``CashValue_ME_EX1``.
The Python scripts included in :mod:`~savings` are used to
draw graphs on the :doc:`Gallery</generated_examples/index>` page
The Jupyter notebook describes the ``CashValue_ME_EX1`` model,
explains the changes from the original model,
and outputs some graphs on the :doc:`Gallery</generated_examples/index>` page.

.. table::
   :widths: 20 80

   ========================================= ===============================================================
   File or Folder                            Description
   ========================================= ===============================================================
   CashValue_ME_EX1                          The example model for *savings_example1.ipynb*
   savings_example1.ipynb                    Jupyter notebook :doc:`/libraries/notebooks/savings/savings_example1`
   plot_av_paths.py                          Python script for :doc:`/generated_examples/savings/plot_ex1_av_paths`
   plot_rand.py                              Python script for :doc:`/generated_examples/savings/plot_ex1_rand`
   plot_option_value.py                      Python script for :doc:`/generated_examples/savings/plot_ex1_option_value`
   ========================================= ===============================================================



Fixes and Updates
===================

* The following formulas are updated.

    * :func:`savings.CashValue_SE.Projection.inv_return_table`
    * :func:`savings.CashValue_ME.Projection.claims_over_av`
    * :func:`savings.CashValue_ME.Projection.claims_from_av`
    * :func:`savings.CashValue_ME.Projection.inv_return_table`
    * :func:`savings.CashValue_ME.Projection.margin_expense`
