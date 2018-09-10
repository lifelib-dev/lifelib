"""
Actual vs Estimated
===================

Lapse assumption changes based on previous year experience.
"""
import modelx as mx

try:
    import nestedlife.nestedlife as nestedlife
except ImportError:
    import nestedlife

model = nestedlife.build()

# Policy point ID and aliases
polid = 171
outer = model.OuterProj[polid]
inner = outer.InnerProj

# %% Code block for overriding the default model

outer.SurrRateMult[1] = 2
outer.SurrRateMult[2] = 0.5
outer.SurrRateMult[3] = 1

inner[1].SurrRateMult[1] = 2
inner[2].SurrRateMult[2] = 0.5
inner[3].SurrRateMult[3] = 1

# %% Code block for drawing graphs

from draw_charts import draw_actest_pairs

draw_actest_pairs(outer, inner, ['PolsSurr', 'PolsIF_End'], 5, 10)

