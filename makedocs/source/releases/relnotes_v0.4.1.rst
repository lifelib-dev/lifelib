.. currentmodule:: lifelib.libraries

.. _relnotes_v0.4.1:

=================================
lifelib v0.4.1 (22 May 2022)
=================================

This release introduces a new library, :mod:`~assets`.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


New Library
===============

The :mod:`~assets` library is for modeling portfolios of financial instruments.
Currently, the library includes one model, :mod:`~assets.BasicBonds`.

:mod:`~assets.BasicBonds` models a portfolio of fixed rate bonds,
generates cashflows and calculates the market value of the portfolio.
:mod:`~assets.BasicBonds` uses `QuantLib`_, a third-party
open-source library for financial instrument valuation.

.. _QuantLib: https://www.quantlib.org/

.. seealso::

    * `Modeling assets with QuantLib | modelx blog <https://modelx.io/blog/2022/02/13/modeling-assets-with-quantlib/>`_




