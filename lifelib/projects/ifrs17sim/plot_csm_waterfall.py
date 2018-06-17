"""
:mod:`ifrs17sim` CSM waterfall chart
====================================

The script draws a CSM waterfall chart.
The script is broken down into pieces of code, and explained in a Jupyter notebook,
:doc:`/projects/ifrs17sim_csm_waterfall`.

The live version of the notebook is available online.

*Launch this notebook online!* |binder ifrs17sim_csm_waterfall|

.. include:: /binderlinks.rst
   :start-after: Begin binder ifrs17sim_csm_waterfall
   :end-before: End binder ifrs17sim_csm_waterfall

"""
import matplotlib.pyplot as plt
from draw_charts import draw_waterfall

try:
    import ifrs17sim.ifrs17sim as ifrs17sim
except ImportError:
    import ifrs17sim

model = ifrs17sim.build()
proj = model.OuterProj[1]

csmrf = proj.cells['CSM_Unfloored',
                   'IntAccrCSM',
                   'AdjCSM_FlufCF',
                   'TransServices'].to_frame(range(15))

csmrf['TransServices'] = -1 * csmrf['TransServices']

draw_waterfall(csmrf)
plt.show()

