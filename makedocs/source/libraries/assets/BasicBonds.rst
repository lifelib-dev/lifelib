.. module:: assets.BasicBonds

The **BasicBond** Model
==========================

Overview
---------

:mod:`~assets.BasicBonds` models a portfolio of fixed rate bonds,
generates cashflows and calculates the market value of the portfolio
from a risk-free curve and Z-spreads.

A table of bond attributes, a zero curve, a valuation date are
given as inputs in the model.
Based on the inputs, the cashflows and market values of the bonds are calculated.

The Z-spreads of the bonds are given as an attribute of the input data,
but the models has a cells to recalculate the Z-spreads
from the market values of the bonds for validation.

:mod:`~assets.BasicBonds` uses `QuantLib`_, a third-party
open-source library for financial instrument valuation.

:mod:`~assets.BasicBonds` contains only once space, :mod:`~assets.BasicBonds.Bonds`
and all the inputs and calculations are defined in :mod:`~assets.BasicBonds.Bonds`.
See :mod:`~assets.BasicBonds.Bonds` for the specification details.

.. _QuantLib:
   https://www.quantlib.org/

Model Specifications
---------------------

The :mod:`~assets.BasicBonds.Bonds` Space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~Bonds
