"""
:mod:`simplelife` present values of cashflows
=============================================

Present values of liability cashflows of a simple whole life policy.
"""
try:
    import simplelife.simplelife as simplelife
except ImportError:
    import simplelife

proj = simplelife.build().Projection

vars = ['PV_PremIncome',
        'PV_BenefitSurr',
        'PV_BenefitDeath',
        'PV_ExpsMaint',
        'PV_ExpsCommTotal',
        'PV_ExpsAcq']

polid = 171

for cells in vars:
    list(proj[polid].cells[cells](t) for t in range(50))

cfs = proj[polid].frame[vars].sort_index().dropna()

[proj[polid].PV_NetCashflow[t] for t in range(50)]

ncf = proj[polid].PV_NetCashflow.frame.sort_index()

import seaborn as sns
sns.set()

axes = ncf.plot.line(marker='o', color='r')
cfs.plot(kind='bar', stacked=True, ax=axes)
