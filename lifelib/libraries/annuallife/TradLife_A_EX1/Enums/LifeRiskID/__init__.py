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

MORT = 1

LONGV = 2

DISAB = 3

LAPSE = 4

EXPS = 5

REV = 6

CAT = 7

BASE = 0