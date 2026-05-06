"""
TradLife_A: present values of cashflows
=============================================

Present values of liability cashflows of a simple whole life policy
projected by the :mod:`~annuallife` ``TradLife_A`` model.

.. seealso::
    * The :mod:`~annuallife` library
"""
import modelx as mx
proj = mx.read_model("TradLife_A").Projection

vars = ['pv_premiums',
        'pv_benefit_surr',
        'pv_claims',
        'pv_exps_maint',
        'pv_commissions',
        'pv_exps_acq']

# PolicyID 171 in simplelife corresponds to idx 170 (0-based array index)
# in TradLife_A.
idx = 170

for cells in vars:
    list(proj[idx].cells[cells](t) for t in range(50))

cfs = proj[idx].frame[vars].sort_index().dropna().droplevel(['x', 'y', 'basis'])

[proj[idx].pv_net_cf[t] for t in range(50)]

ncf = proj[idx].pv_net_cf.frame.sort_index()

import seaborn as sns
sns.set_theme(style="darkgrid")

axes = ncf.plot.line(marker='o', color='r')
cfs.plot(kind='bar', stacked=True, ax=axes)
