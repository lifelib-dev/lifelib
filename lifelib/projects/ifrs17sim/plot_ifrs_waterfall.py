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
proj = model.OuterProj[1]

# %% CSM Amortization

csmrf = proj.cells['CSM_Unfloored',
                   'IntAccrCSM',
                   'AdjCSM_FlufCF',
                   'TransServices'].to_frame(range(3))

csmrf['TransServices'] = -1 * csmrf['TransServices']

draw_waterfall(csmrf, title='CSM Amortization')

# %% Expected Cashflow Rollforwad

estcf = proj.cells['PV_FutureCF',
                   'EstPremIncome',
                   'EstIntOnCF',
                   'EstAcqCashflow',
                   'EstClaim',
                   'EstExps'].to_frame(range(3))

estcf['EstPremIncome'] = -1 * estcf['EstPremIncome'] 

draw_waterfall(estcf, title='Expected Cashflows')
    
# %% Actual Cashflow Rollforward
    
actcf = proj.cells['AccumCF',
                   'PremIncome',
                   'IntAccumCF',
                   'ExpsAcqTotal',
                   'BenefitTotal',
                   'ExpsMaintTotal'].to_frame(range(3))

for outflow in ['ExpsAcqTotal',
                'BenefitTotal',
                'ExpsMaintTotal']:
    actcf[outflow] = -1 * actcf[outflow]

draw_waterfall(actcf, title='Actual Cashflows')

# %% IFRS17 Financial Performance

ifrspl = proj.cells['NetBalance',
                    'InsurRevenue',
                    'InsurServiceExps',
                    'InsurFinIncomeExps'].to_frame(range(5))

ifrspl['InsurServiceExps'] = -1 * ifrspl['InsurServiceExps']

draw_waterfall(ifrspl, title='IFRS17 Profit/Loss')

