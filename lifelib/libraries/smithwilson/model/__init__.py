"""The Smith-Wilson model

This model extrapolates observed risk-free interest rates using the Smith-Wilson method.

The Smith-Wilson method is used for extrapolating risk-free interest rates under the Solvency II framework.
The method is described in
`QIS 5 Risk-free interest rates – Extrapolation method`_,
a technical paper issued by CEIOPS (the predecessor of EIOPA).
Cells in this model are named consistently
with the mathematical symbols in the technical paper.

.. _QIS 5 Risk-free interest rates – Extrapolation method: https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf

"""

from modelx.serialize.jsonvalues import *

_name = "smithwilson"

_allow_none = False

_spaces = [
    "SmithWilson"
]

