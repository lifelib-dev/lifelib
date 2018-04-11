"""
:mod:`simplelife` cashflow
==========================

Draw a graph of liability cashflows of a simple whole life policy
"""
try:
    import simplelife.simplelife as simplelife
except ImportError:
    import simplelife

proj = simplelife.build().Projection

vars = ['pv_incm_Premium',
        'pv_bnft_Surrender',
        'pv_bnft_Death',
        'pv_exps_Maint',
        'pv_exps_CommTotal',
        'pv_exps_Acq']

polid = 171

for cells in vars:
    list(proj[polid].cells[cells](t) for t in range(50))

cfs = proj[polid].frame[vars].sort_index().dropna()

[proj[polid].pv_NetLiabilityCashflow[t] for t in range(50)]

ncf = proj[polid].pv_NetLiabilityCashflow.frame.sort_index()

import seaborn as sns
sns.set()

axes = ncf.plot.line(marker='o', color='r')
cfs.plot(kind='bar', stacked=True, ax=axes)
