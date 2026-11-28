# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""LMM interest rate scenario generator for TVOG calculations with lifelib.

Generates risk-neutral monthly scenarios from the LIBOR market model, with shifted-lognormal
forward rates fitted exactly to an initial curve, and all inputs read at run time from the
Excel file ``lmm_input.xlsx`` next to the model folder. See the
:mod:`~economic.BasicLMM.LMM` space.
"""

from modelx.serialize.jsonvalues import *

_name = "BasicLMM"

_allow_none = False

_spaces = [
    "LMM",
    "Validation"
]

