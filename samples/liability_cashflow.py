"""Draw a graph of liability cashflows of a simple whole life policy"""

from lifelib.projects.simplelife.build import *

vars = ['prj_incm_Premium',
        'prj_bnft_Surrender',
        'prj_bnft_Death',
        'prj_exps_Maint',
        'prj_exps_CommTotal',
        'prj_exps_Acq']

polid = 171

for cells in vars:
    list(getattr(proj[polid], cells)(t) for t in range(50))

cfs = proj[polid].frame[vars].sort_index().dropna()
cfs[vars[1:]] = cfs[vars[1:]].mul(-1)

[proj[polid].prj_NetLiabilityCashflow[t] for t in range(50)]

ncf = proj[polid].prj_NetLiabilityCashflow.frame.sort_index()

import seaborn as sns
sns.set()

axes = ncf.plot.line(marker='o', color='r')
cfs.plot(kind='bar', stacked=True, ax=axes)
