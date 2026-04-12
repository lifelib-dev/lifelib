"""
nestedlife: Actual vs Estimated
================================

Lapse assumption changes based on previous year experience.

.. seealso::
    * The :mod:`~nestedlife` library
"""
import modelx as mx

model = mx.read_model("model")

# Policy point ID and aliases
polid = 171
outer = model.OuterProj[polid]
inner = outer.InnerProj

# Code block for overriding the default model

outer.asmp.SurrRateMult[1] = 2
outer.asmp.SurrRateMult[2] = 0.5
outer.asmp.SurrRateMult[3] = 1

inner[1].asmp.SurrRateMult[1] = 2
inner[2].asmp.SurrRateMult[2] = 0.5
inner[3].asmp.SurrRateMult[3] = 1

# Code block for drawing graphs

from draw_charts import draw_actest_pairs

draw_actest_pairs(outer, inner, ['PolsSurr', 'PolsIF_End'], 5, 10)

