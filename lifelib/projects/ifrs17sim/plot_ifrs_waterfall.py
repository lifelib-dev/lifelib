"""
:mod:`ifrs17sim` IFRS waterfall chart
=====================================

The script draws multiple waterfall charts,
each of which depict sources of changes in balances related to IFRS17.
The script is broken down into pieces of code, and explained in a Jupyter notebook,
:doc:`/projects/ifrs17sim_ifrs_waterfall`.

The live version of the notebook is available online.

*Launch this notebook online!* |binder ifrs17sim_ifrs_waterfall|

.. include:: /binderlinks.rst
   :start-after: Begin binder ifrs17sim_ifrs_waterfall
   :end-before: End binder ifrs17sim_ifrs_waterfall

"""
import matplotlib.pyplot as plt
from draw_charts import draw_waterfall

try:
    import ifrs17sim.ifrs17sim as ifrs17sim
except ImportError:
    import ifrs17sim

model = ifrs17sim.build()
proj = model.OuterProjection[1]

# %% CSM Amortization

csmrf = proj.cells['CSM_Unfloored',
                   'IntAccrCSM',
                   'AdjCSM_FulCashFlows',
                   'TransServices'].to_frame(range(3))

csmrf['TransServices'] = -1 * csmrf['TransServices']

draw_waterfall(csmrf, title='CSM Amortization')

# %% Expected Cashflow Rollforwad

estcf = proj.cells['PV_FutureCashflow',
                   'ExpectedPremium',
                   'ExpectedInterestCashflow',
                   'ExpectedAcqCashflow',
                   'ExpectedClaims',
                   'ExpectedExps'].to_frame(range(3))

estcf['ExpectedPremium'] = -1 * estcf['ExpectedPremium'] 

plt.figure()
draw_waterfall(estcf, title='Expected Cashflows')
    
# %% Actual Cashflow Rollforward
    
actcf = proj.cells['prj_AccumCashflow',
                   'prj_incm_Premium',
                   'prj_InterestAccumCashflow',
                   'prj_exps_AcqTotal',
                   'prj_bnft_Total',
                   'prj_exps_MaintTotal'].to_frame(range(3))

for outflow in ['prj_exps_AcqTotal',
                'prj_bnft_Total',
                'prj_exps_MaintTotal']:
    actcf[outflow] = -1 * actcf[outflow]
    

plt.figure()
draw_waterfall(actcf, title='Actual Cashflows')

# %% IFRS17 Financial Performance

ifrspl = proj.cells['NetBalance',
                    'InsRevenue',
                    'InsServiceExps',
                    'InsFinanceIncomeExps'].to_frame(range(5))

ifrspl['InsServiceExps'] = -1 * ifrspl['InsServiceExps']

plt.figure()
draw_waterfall(ifrspl, title='IFRS17 Profit/Loss')

