"""
Smith-Wilson extrapolation with various alphas
==============================================

This notebook extrapolates forward rates
using the Smith-Wilson methods with various alphas, and draws
the forward rates.
"""

import modelx as mx
import pandas as pd

#%%
# The code below reads the ``smithwilson`` model from "model" folder,
# and assign the SmithWilson space of the model to ``space``.

space = mx.read_model("model").SmithWilson

#%%
# The code below is for parametrizing the SmithWilson space by ``x``.
# The parameter ``x`` takes integer values, and it means that
# the alpha in the space is increased by ``x`` times 10% of the original
# alpha. ``x`` can be negative.

def parametrize(x):
    return {"refs": {"alpha": alpha * (1 + 0.1 * x)}}

space.formula = parametrize

#%%
# The code below creates the ``ForwardRates`` cells,
# which calculates extrapolated forward rates from
# the present values of bond prices.

@mx.defcells
def ForwardRates(t):
    return P(t) / P(t+1) - 1


#%%
# The code below plots the extrapolated forward rates
# with various alphas.

d = {"{0:.3}".format(space.alpha * (1 + 0.1*x)):
         [space[x].ForwardRates[t] for t in range(1, 101)]
     for x in range(-6, 5)}

df = pd.DataFrame(d, index=range(1, 101))

df.plot.line()