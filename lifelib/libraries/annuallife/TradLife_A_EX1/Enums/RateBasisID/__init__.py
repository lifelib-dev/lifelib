# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Rate basis codes.

Integer codes used to select between the premium and valuation
interest-rate / mortality-table bases. Consumed by
:func:`~annuallife.TradLife_A.PolicyAttrs.int_rate` and
:func:`~annuallife.TradLife_A.PolicyAttrs.table_id` and by the
commutation-table lookups in
:func:`~annuallife.TradLife_A.BaseProj.gross_prem_rate`,
:func:`~annuallife.TradLife_A.BaseProj.net_prem_rate` and
:func:`~annuallife.TradLife_A.BaseProj.reserve_nlp_rate`.

Members:
    PREM(:obj:`int`): Premium basis.
    VAL(:obj:`int`): Valuation basis.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

PREM = 1

VAL = 2