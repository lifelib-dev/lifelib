"""
ifrs17sim: CSM waterfall chart
====================================

The script draws a CSM waterfall chart.
The script is broken down into pieces of code, and explained in a Jupyter notebook,
:doc:`/projects/notebooks/ifrs17sim/ifrs17sim_csm_waterfall`.

The live version of the notebook is available online.

*Launch this notebook online!* |binder ifrs17sim_csm_waterfall|

.. include:: /binderlinks.rst
   :start-after: Begin binder ifrs17sim_csm_waterfall
   :end-before: End binder ifrs17sim_csm_waterfall

.. seealso::
    * The :mod:`~ifrs17sim` library
"""
import modelx as mx
from draw_charts import draw_waterfall, get_waterfalldata
import seaborn as sns
sns.set_theme(style="darkgrid")

model = mx.read_model("model")
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
