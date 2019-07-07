"""
:mod:`ifrs17sim` IFRS waterfall chart
=====================================

The script draws multiple waterfall charts,
each of which depict sources of changes in balances related to IFRS17.
The script is broken down into pieces of code, and explained in a Jupyter notebook,
:doc:`/projects/ifrs17sim_charts_baseline`.

The live version of the notebook is available online.

*Launch this notebook online!* |binder ifrs17sim_charts_baseline|

.. include:: /binderlinks.rst
   :start-after: Begin binder ifrs17sim_charts_baseline
   :end-before: End binder ifrs17sim_charts_baseline

"""
import matplotlib.pyplot as plt
from draw_charts import draw_waterfall, get_waterfalldata

try:
    import ifrs17sim.ifrs17sim as ifrs17sim
except ImportError:
    import ifrs17sim

model = ifrs17sim.build()
proj = model.OuterProj[1]

# %% CSM Amortization

csmrf = get_waterfalldata(
            proj, 
            items=['CSM',
                   'IntAccrCSM',
                   'AdjCSM_FlufCF',
                   'TransServices'],
            length=3,
            reverseitems=['TransServices'])

draw_waterfall(csmrf, title='CSM Amortization')

# %% Expected Cashflow Rollforwad

estcf = get_waterfalldata(
            proj,
            items=['PV_FutureCF',
                   'EstPremIncome',
                   'EstIntOnCF',
                   'EstAcqCashflow',
                   'EstClaim',
                   'EstExps'],
            length=3,
            reverseitems=['EstPremIncome'])

draw_waterfall(estcf, title='Expected Cashflows')
    
# %% Actual Cashflow Rollforward
    
actcf = get_waterfalldata(
            proj,
            items=['PremIncome',
                   'IntAccumCF',
                   'ExpsAcqTotal',
                   'BenefitTotal',
                   'ExpsMaintTotal',
                   'ActualNetCF'],
            length=3,
            reverseitems=['ExpsAcqTotal',
                          'BenefitTotal',
                          'ExpsMaintTotal'])

draw_waterfall(actcf, stocks=[0, 5], title='Actual Cashflows')

# %% IFRS17 Financial Performance

ifrspl = get_waterfalldata(
            proj,
            items=['InsurRevenue',
                   'InsurServiceExps',
                   'InsurFinIncomeExps',
                   'ProfitBefTax'],
            length=5,
            reverseitems=['InsurServiceExps'])

draw_waterfall(ifrspl, stocks=[0, 3], title='IFRS17 Profit/Loss')

