# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

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