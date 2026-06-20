# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Enum-style codes used across :mod:`~annuallife.TradLife_A`.

This Space groups the small integer-coded enumerations referenced by
the projection cells. Each enum is exposed as a child Space whose
References hold the integer codes for its members:

* :mod:`~annuallife.TradLife_A.Enums.ProductID` - product type codes
  (``TERM``, ``WL``, ``ENDW``).
* :mod:`~annuallife.TradLife_A.Enums.SexID` - sex codes used to index
  mortality tables (``M``, ``F``).
* :mod:`~annuallife.TradLife_A.Enums.RateBasisID` - rate-basis codes
  used by the commutation lookup (``PREM``, ``VAL``).

The three child spaces are also re-exported at the model level as
``ProductID``, ``SexID`` and ``RateBasisID`` for convenience.

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

