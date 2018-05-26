"""
:mod:`ifrs17sim` CSM waterfall chart
====================================

Draw a graph of CSM amortization pattern.

*Run this sample now!* |launch binder|

.. |launch binder| image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/fumitoh/ifrs17sim-demo/master?filepath=ifrs17sim-demo.ipynb

"""
import pandas as pd
import collections
import matplotlib.pyplot as plt
from draw_charts import draw_waterfall

try:
    import ifrs17sim.ifrs17sim as ifrs17sim
except ImportError:
    import ifrs17sim

model = ifrs17sim.build(True)
proj = model.OuterProjection[1]

proj.CSM_Unfloored(15)
data = collections.OrderedDict()

for cells in ['CSM_Unfloored',
              'IntAccrCSM',
              'AdjCSM_FulCashFlows',
              'TransServices']:
    data[cells] = [proj.cells[cells](t) for t in range(3)]


df = pd.DataFrame(data)
df['TransServices'] = -1 * df['TransServices']

# plt.figure()
draw_waterfall(df, title='CSM Amortization')

# %% Expected Cashflow Rollforwad

data.clear()
for cells in ['PV_FutureCashflow',
              'ExpectedPremium',
              'ExpectedInterestCashflow',
              'ExpectedAcqCashflow',
              'ExpectedClaims',
              'ExpectedExps']:
    data[cells] = [proj.cells[cells](t) for t in range(3)]

estcf = pd.DataFrame(data)


# Want to express like below
#
#revenue = proj.cells['PV_FutureCashflow',
#                     'ExpectedPremium',
#                     'ExpectedInterestCashflow',
#                     'ExpectedAcqCashflow',
#                     'ExpectedClaims',
#                     'ExpectedExps'](t=range(3)).frame

for inflow in ['ExpectedPremium']:
    estcf[inflow] = -1 * estcf[inflow] 

plt.figure()
draw_waterfall(estcf, title='Expected Cashflows')
    
# %% Actual Cashflow Rollforward
    
data.clear()
for cells in ['prj_AccumCashflow',
              'prj_incm_Premium',
              'prj_InterestAccumCashflow',
              'prj_exps_AcqTotal',
              'prj_bnft_Total',
              'prj_exps_MaintTotal']:
    data[cells] = [proj.cells[cells](t) for t in range(3)]
    
actcf = pd.DataFrame(data)
for outflow in ['prj_exps_AcqTotal',
                'prj_bnft_Total',
                'prj_exps_MaintTotal']:
    actcf[outflow] = -1 * actcf[outflow]
    

plt.figure()
draw_waterfall(actcf, title='Actual Cashflows')

# %% IFRS17 Financial Performance

data.clear()
for cells in ['NetBalance',
              'InsRevenue',
              'InsServiceExps',
              'InsFinanceIncomeExps']:
    data[cells] = [proj.cells[cells](t) for t in range(5)]    


ifrspl = pd.DataFrame(data)
for pl in ['InsServiceExps']:
    ifrspl[pl] = -1 * ifrspl[pl]

#fg, ax = plt.subplots(nrows=3)
#draw_waterfall(estcf, ax[0])
#draw_waterfall(actcf, ax[1])
#draw_waterfall(df, ax[2])
#fg.tight_layout()

plt.figure()
draw_waterfall(ifrspl, title='IFRS17 Profit/Loss')
