"""
:mod:`simplelife` cashflow
==========================

Draw a graph of liability cashflows of a simple whole life policy

*Run this sample now!* |binder simplelife_demo|

.. include:: /binderlinks.rst
   :start-after: Begin binder simplelife_demo
   :end-before: End binder simplelife_demo

"""
import pandas as pd
import modelx as mx

import seaborn as sns
sns.set()

try:
    import simplelife.simplelife as simplelife
except ImportError:
    import simplelife


polid = 171
proj = simplelife.build().Projection[polid]

# %% Draw NetCashflows Graph
data = {'NetCashflows': [proj.NetInsurCF[t] for t in range(50)]}
ax = pd.DataFrame(data).plot.line(marker='o', color='r')

# %% Draw componets of net cashflows

vars = ['PremIncome',
        'BenefitSurr',
        'BenefitDeath',
        'ExpsMaint',
        'ExpsCommTotal',
        'ExpsAcq']


df = proj.cells[vars].to_frame(range(50))

df[vars[1:]] = df[vars[1:]].mul(-1)   # Change outflows to negatives
df.plot(kind='bar', stacked=True, ax=ax, title='Insurance Cashflows')

