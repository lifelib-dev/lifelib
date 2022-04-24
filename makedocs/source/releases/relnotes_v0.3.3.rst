.. currentmodule:: lifelib.libraries

.. _relnotes_v0.3.3:

=================================
lifelib v0.3.3 (24 April 2022)
=================================

This release adds a new example,
:doc:`/libraries/notebooks/savings/savings_example3` in the :mod:`~savings` library.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


New Example
===============

An example notebook, :doc:`/libraries/notebooks/savings/savings_example3`
is added to the :mod:`~savings` library.
This example demonstrates how to effectively
run a heavy model with a large data set.
The demonstration utilizes techniques such as:

* Multiprocessing using ipyparallel
* Memory-optimized runs introduced in modelx v0.19.0

This example is included as a Jupyter notebook.
Another notebook for generating a table of 100K model points used for the
example is included.

.. table::
   :widths: 20 80

   ========================================= =========================================================================================
   File or Folder                            Description
   ========================================= =========================================================================================
   savings_example3.ipynb                    Jupyter notebook :doc:`/libraries/notebooks/savings/savings_example3`
   generate_100K_model_points.ipynb          Jupyter notebook :doc:`/libraries/notebooks/savings/generate_100K_model_points`
   ========================================= =========================================================================================



