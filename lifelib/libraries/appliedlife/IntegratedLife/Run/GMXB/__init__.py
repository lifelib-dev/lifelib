"""Product space for GMXB products

:mod:`~appliedlife.IntegratedLife.Run.GMXB` is a product space for GMDB and GMAB products.
It is a child space of :mod:`~appliedlife.IntegratedLife.Run`,
and a subspace of :mod:`~appliedlife.IntegratedLife.ProductBase`.
All the contents are inherited from :mod:`~appliedlife.IntegratedLife.ProductBase`,
so see :mod:`~appliedlife.IntegratedLife.ProductBase` for the details.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda product_id, segment_id="ALL": None

_bases = [
    "..ProductBase"
]

_allow_none = None

_spaces = []

