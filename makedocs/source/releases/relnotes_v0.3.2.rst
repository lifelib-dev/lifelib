.. currentmodule:: lifelib.libraries

.. _relnotes_v0.3.2:

=================================
lifelib v0.3.2 (23 November 2021)
=================================

This release adds a new example,
:doc:`/libraries/notebooks/savings/savings_example2` in the :mod:`~savings` library,
and reflects some cosmetic changes in the :mod:`~savings` models.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade


New Example
===============

An example notebook, :doc:`/libraries/notebooks/savings/savings_example2`
is added to the :mod:`~savings` library.
This example shows how to extend the ``CashValue_ME_EX1`` model in the :doc:`/libraries/notebooks/savings/savings_example1`
and reflect maintenance fees, policy decrement, GMDB and dynamic lapse.
The extended model is included in the :mod:`~savings` library
as ``CashValue_ME_EX2``.

This example consists of the Jupyter notebook, sample model,
and some Python scripts to plot graphs.
The Python scripts are used to
draw graphs on the :doc:`Gallery</generated_examples/index>` page.
The Jupyter notebook describes the ``CashValue_ME_EX2`` model,
explains the changes from the original model,
and outputs some graphs on the :doc:`Gallery</generated_examples/index>` page.

.. table::
   :widths: 20 80

   ========================================= ===============================================================
   File or Folder                            Description
   ========================================= ===============================================================
   CashValue_ME_EX2                          The example model for *savings_example2.ipynb*
   savings_example2.ipynb                    Jupyter notebook :doc:`/libraries/notebooks/savings/savings_example2`
   plot_ex2_comp_option_values.py            Python script for :doc:`/generated_examples/savings_gallery/plot_ex2_comp_option_values`
   plot_ex2_lapse_decrement.py               Python script for :doc:`/generated_examples/savings_gallery/plot_ex2_lapse_decrement`
   plot_ex2_av_to_pols.py                    Python script for :doc:`/generated_examples/savings_gallery/plot_ex2_av_to_pols`
   ========================================= ===============================================================



Fixes and Updates
===================

* ``plot_av_paths.py`` in the :mod:`~savings` library is renamed to :doc:`plot_ex1_av_paths.py</generated_examples/savings_gallery/plot_ex1_av_paths>`
* ``plot_rand.py`` in the :mod:`~savings` library is renamed to :doc:`plot_ex1_rand.py</generated_examples/savings_gallery/plot_ex1_rand>`
* ``plot_option_value.py`` in the :mod:`~savings` library is renamed to :doc:`plot_ex1_option_value.py</generated_examples/savings_gallery/plot_ex1_option_value>`
