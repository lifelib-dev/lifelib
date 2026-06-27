# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Enum-style codes used across :mod:`~annuallife.TradLife_A_EX1`.

This Space extends :mod:`TradLife_A.Enums <annuallife.TradLife_A.Enums>` with the
enumerations used by the Solvency II life-risk calculations. The
``ProductID``, ``SexID`` and ``RateBasisID`` enums are unchanged from
:mod:`TradLife_A.Enums <annuallife.TradLife_A.Enums>`.

.. rubric:: New enum child Spaces

The following enum child Spaces are added. Each exposes its members as
integer References.

* ``LifeRiskID`` -- life sub-risks: ``MORT``, ``LONGV``, ``DISAB``,
  ``LAPSE``, ``EXPS``, ``REV`` and ``CAT``, plus ``BASE`` (0) for the
  unstressed run.
* ``LapseShockID`` -- lapse shocks: ``UP``, ``DOWN`` and ``MASS``.
* ``LapseScopeID`` -- lapse scope: ``RETAIL`` and ``INST``.
* ``ExtraKeyID`` -- extra qualifiers for shock parameters, such as
  ``LIMIT`` (a cap on the shocked rate) and ``INFL`` (the
  expense-inflation stress).

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = [
    "ProductID",
    "SexID",
    "RateBasisID",
    "LifeRiskID",
    "LapseShockID",
    "LapseScopeID",
    "ExtraKeyID"
]

