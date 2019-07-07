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
from draw_charts import draw_waterfall, get_waterfalldata

try:
    import ifrs17sim.ifrs17sim as ifrs17sim
except ImportError:
    import ifrs17sim

model = ifrs17sim.build(True)
proj = model.OuterProj[1]

csmrf = get_waterfalldata(
        proj,
        items=['CSM',
               'IntAccrCSM',
               'AdjCSM_FlufCF',
               'TransServices'],
        length=15,
        reverseitems=['TransServices'])

draw_waterfall(csmrf)
