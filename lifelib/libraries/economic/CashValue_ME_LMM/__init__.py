# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""lifelib's savings model CashValue_ME_EX4, driven by LMM interest rate scenarios.

The space ESG is a copy of the :mod:`~economic.BasicLMM.LMM` space of BasicLMM. It reads
``lmm_input.xlsx`` next to the model folder and supplies the deflators and the fund
returns of every scenario. Scenario 0 is the certainty-equivalent (CE) scenario, so one
run gives both terms of TVOG = mean of the stochastic present values - the CE present
value. See ``Projection.result_tvog``, and the notebook ``lmm-tvog.ipynb``, which
describes this example model. Apart from its ESG and its closed form, the model is
CashValue_ME_G2PP.
"""

from modelx.serialize.jsonvalues import *

_name = "CashValue_ME_LMM"

_allow_none = False

_spaces = [
    "Projection",
    "ESG"
]

