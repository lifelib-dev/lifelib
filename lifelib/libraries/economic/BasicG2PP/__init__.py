# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""G2++ interest rate scenario generator for TVOG calculations with lifelib.

Generates risk-neutral monthly scenarios from the two-additive-factor Gaussian model G2++,
fitted exactly to an initial curve, with all inputs read at run time from the Excel file
``g2pp_input.xlsx`` next to the model folder. See the :mod:`~economic.BasicG2PP.G2PP` space.
"""

from modelx.serialize.jsonvalues import *

_name = "BasicG2PP"

_allow_none = False

_spaces = [
    "G2PP",
    "Validation"
]

