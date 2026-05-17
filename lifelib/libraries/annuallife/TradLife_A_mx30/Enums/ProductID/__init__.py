"""Product type codes.

Integer codes identifying the product of a policy. Used by
:func:`~annuallife.TradLife_A.PolicyAttrs.product` and by the
product-dependent branches in
:func:`~annuallife.TradLife_A.BaseProj.gross_prem_rate` and
:func:`~annuallife.TradLife_A.BaseProj.net_prem_rate`.

Members:
    TERM(:obj:`int`): Term insurance.
    WL(:obj:`int`): Whole life insurance.
    ENDW(:obj:`int`): Endowment insurance.

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# References

TERM = 1

WL = 2

ENDW = 3