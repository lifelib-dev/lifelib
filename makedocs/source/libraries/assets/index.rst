.. module:: assets
.. include:: /banners.rst

The **assets** Library
==========================

|modelx badge|

Overview
---------

This library is for modeling portfolios of financial instruments.
Currently, the library includes one model:

.. toctree::
   :maxdepth: 1

   BasicBonds

:mod:`~assets.BasicBonds` models a portfolio of fixed rate bonds,
generates cashflows and calculates the market value of the portfolio.
:mod:`~assets.BasicBonds` uses `QuantLib`_, a third-party
open-source library for financial instrument valuation.

.. _QuantLib: https://www.quantlib.org/


.. seealso::

    * `Modeling assets with QuantLib | modelx blog <https://modelx.io/blog/2022/02/13/modeling-assets-with-quantlib/>`_


.. todo::
    This library is in its early alpha release stage, and more
    contents will be added in near future.

Prerequisites
--------------

To use this library you need `Quantlib-Python`_,
a Python wrapper for `QuantLib`_.
To install `Quantlib-Python`_ from PyPI, run the following command:

.. _Quantlib-Python: https://quantlib-python-docs.readthedocs.io/en/latest/

.. code-block:: console

    pip install QuantLib


How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *assets* library.
For example, to copy as a folder named *assets*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("assets", r"C:\path\to\your\assets")

Jupyter Notebooks
------------------------------

========================= ==================================
:doc:`generate_bond_data` |colab assets generate_bond_data|
========================= ==================================

.. toctree::
   :hidden:
   :maxdepth: 1

   generate_bond_data


Library Contents
------------------

.. table::
   :widths: 20 80

   ========================================= ===============================================================
   File or Folder                            Description
   ========================================= ===============================================================
   BasicBonds                                The :mod:`~assets.BasicBonds` model.
   generate_bond_data.ipynb                  Jupyter notebook :doc:`generate_bond_data`
   ========================================= ===============================================================


