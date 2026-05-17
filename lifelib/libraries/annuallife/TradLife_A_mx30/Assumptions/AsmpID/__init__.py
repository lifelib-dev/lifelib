"""Assumption table identifiers.

Integer codes identifying columns of the ``AsmpByDuration`` table
(loaded by :func:`~annuallife.TradLife_A.InputData.assumption_tables`).
Each member corresponds to one duration-based assumption series:

* ``MortAsmp1``, ``MortAsmp2`` - mortality-factor tables, picked up by
  :func:`~annuallife.TradLife_A.Assumptions.mort_factor_index`.
* ``Morb1`` ... ``Morb5`` - morbidity-factor tables (reserved for
  benefit categories not currently exercised by the model).
* ``LapseRate1`` - lapse-rate table, picked up by
  :func:`~annuallife.TradLife_A.Assumptions.lapse_rate_index`.

The numeric values reflect the column position in
``AsmpByDuration``; consumers should refer to the names rather than the
numbers.

.. todo::

   Split the combined duration table into per-type tables so that
   morbidity, mortality factor and lapse rates each live in dedicated
   ranges with self-explanatory member names.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

MortAsmp1 = 1

MortAsmp2 = 2

Morb1 = 3

Morb2 = 4

Morb3 = 5

Morb4 = 6

Morb5 = 7

LapseRate1 = 8