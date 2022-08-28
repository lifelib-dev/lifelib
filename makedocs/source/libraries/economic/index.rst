.. module:: economic

The **economic** Library
==========================

Overview
---------

The **economic** library is for modeling economic scenarios.
Currently, the library includes one primary model:

.. toctree::
   :maxdepth: 1

   BasicHullWhite

.. todo::
    This library is in its early alpha release stage, and more
    contents will be added in near future.


How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *economic* library.
For example, to copy as a folder named *economic*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("economic", r"C:\path\to\your\economic")

Jupyter Notebooks
------------------------------

.. toctree::
   :maxdepth: 1

   /libraries/notebooks/economic/hull-white-simulation.ipynb


Library Contents
------------------

.. table::

   ======================================= ========================================================================================
   File or Folder                          Description
   ======================================= ========================================================================================
   BasicHullWhite                          The :mod:`~economic.BasicHullWhite` model.
   hull-white-simulation.ipynb             Jupyter notebook :doc:`/libraries/notebooks/economic/hull-white-simulation`
   plot_ex1_short_rate_paths.py            Python script for :doc:`/generated_examples/economic/plot_ex1_short_rate_paths`
   plot_ex2_short_rate_mean_variance.py    Python script for :doc:`/generated_examples/economic/plot_ex2_short_rate_mean_variance`
   plot_ex3_disc_factor_convergence.py     Python script for :doc:`/generated_examples/economic/plot_ex3_disc_factor_convergence`
   ======================================= ========================================================================================

