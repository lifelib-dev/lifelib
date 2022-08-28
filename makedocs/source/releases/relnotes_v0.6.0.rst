.. currentmodule:: lifelib.libraries

.. _relnotes_v0.6.0:

================================
lifelib v0.6.0 (28 August 2022)
================================

This release adds a new library, :mod:`~economic`.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


New Library
===============

The new :mod:`~economic` library currently has one model, :mod:`~economic.BasicHullWhite`.
:mod:`~economic.BasicHullWhite` is a simple implementation of `the Hull-White model <https://en.wikipedia.org/wiki/Hull%E2%80%93White_model>`_.
:mod:`~economic.BasicHullWhite` preforms Monte-Carlo simulations
and generates paths of the instantaneous short rate based on the Hull-White model.
Many properties of the Hull-White model are analytically solvable,
and :mod:`~economic.BasicHullWhite` also includes formulas analytically solving for the properties.


See :mod:`~economic` and :mod:`~economic.BasicHullWhite` for more details.




