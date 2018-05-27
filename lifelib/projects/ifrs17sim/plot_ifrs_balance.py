"""
:mod:`ifrs17sim` IFRS balancesheet itms
=======================================

Fulfilment CF, CSM, Cash balances
"""
import collections
import pandas as pd
import matplotlib.pyplot as plt
import modelx as mx

# When the current directory is this folder,
# The try-except statement below can be replaced by just the last two
# import statements.
try:
    import ifrs17sim.ifrs17sim as ifrs17sim
    import ifrs17sim.draw_charts as draw_charts
except ImportError:
    import ifrs17sim
    import draw_charts

model = ifrs17sim.build()
proj = model.OuterProjection[171]

# From Python 3.7, dict is ordered so no need to use OrderedDict.
data = collections.OrderedDict()
data['CSM'] = [proj.CSM_Unfloored(t) for t in range(10)]
data['FCF'] = [-proj.PV_FutureCashflow(t) for t in range(10)]
data['Cash'] = [-proj.prj_AccumCashflow(t) for t in range(10)]


draw_charts.draw_stackedbarpairs(pd.DataFrame(data),
                                 title='Fulfilment CF and CSM')

plt.show()
