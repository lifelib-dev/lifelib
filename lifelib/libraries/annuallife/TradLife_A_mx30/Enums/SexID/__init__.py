"""Sex codes.

Integer codes used to identify the sex column of a mortality table.
Returned per policy by :func:`~annuallife.TradLife_A.PolicyAttrs.sex`
and consumed by the indexing logic in
:func:`~annuallife.TradLife_A.Assumptions.mort_array_index` and
:func:`~annuallife.TradLife_A.CommTable.mortality_rates`.

Members:
    M(:obj:`int`): Male.
    F(:obj:`int`): Female.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

M = 1

F = 2