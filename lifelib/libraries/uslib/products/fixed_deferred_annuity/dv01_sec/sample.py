"""modelx-cython's sample run for the DV01 model: the calls that type every Cell the report uses.

The compiler runs this file in the build directory, beside the exported package ``model``
and the CSVs the build copied there (``compiled.py``).  It computes the annual risk report
of the shipped book, MYGA_US_SEC's fourteen points, on ESG path 1 at years 0, 1 and 2, through
the ``Outer`` Cells, releasing each close's Valuation ItemSpaces once summed, as
``report.live_report`` does, and asks ``Outer`` for the actual cash flows.  A Cell the
report never calls, such as MYGA_US_SEC's own reports, compiles as a Python object.
"""
import sys

sys.setrecursionlimit(20_000)

from model import mx_model  # noqa: E402

outer, valuation = mx_model.Outer, mx_model.Valuation
ids = valuation.point_indices()
keys = range(len(mx_model.Data.shock_key_months()))
for month in (-1, 11, 23):
    outer.base_liability_pv(month, 1)
    outer.base_cashflows(month, 1)
    for i in ids:
        del valuation[month, i, 1, -1]
    for key in keys:
        outer.dv01(month, 1, key)
        outer.cs01(month, 1, key)
        for i in ids:
            del valuation[month, i, 1, key]
outer.annual_risk_report(1, 2)
outer.actual_cashflows(1)
outer.scenario_ids()
