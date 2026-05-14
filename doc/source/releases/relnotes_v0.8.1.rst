.. currentmodule:: lifelib.libraries

.. _relnotes_v0.8.1:

==================================
lifelib v0.8.1 (3 May 2023)
==================================

This release adds a new example in :mod:`~savings`.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


New Example
===============

This release adds a new example,  :doc:`/libraries/savings/savings_example4` in :mod:`~savings`.
The example shows how to profile and optimize a model using ``CashValue_ME_EX1`` as an example.
The optimization approach involves replacing pandas DataFrames and Series with numpy arrays.
The optimized model used in the example is included in :mod:`~savings` as ``CashValue_ME_EX4``.
The example is based on recommendation given by `alexeybaran <https://github.com/fumitoh/modelx/discussions/79>`_



