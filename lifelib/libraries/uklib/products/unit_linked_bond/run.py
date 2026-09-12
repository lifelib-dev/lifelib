"""Run the ULB_UK_S reference model and print its unit fund and cash flow statements.

    python products/unit_linked_bond/run.py            # anchor cell (point_id = 1)
    python products/unit_linked_bond/run.py 2          # the accumulation cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "ULB_UK_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{}, premium {:,.0f} in {} segments".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.premium(), proj.n_segments()))
print("AMC {:.2%}  further costs {:.2%}  tax provision {:.0%}  uplift {:.3f}  "
      "gross return {:.1%}".format(
          proj.amc_rate(), proj.further_costs_rate(), proj.tax_provision_rate(),
          proj.db_uplift(), model.Projection.fund_return))
print("withdrawals = {} ({:,.2f}/month)   adviser charge {:.2%}   GMDB rider = {}".format(
    proj.wd_pattern(), proj.wd_pp(0), proj.oac_rate(), proj.gmdb_flag()))
exhausted = proj.fund_exhaust_mth() <= proj.horizon_mths()
print("projection: {} months, t = 0 .. {} ({}); fund {}".format(
    proj.proj_len(), proj.proj_len() - 1,
    "fund exhausted" if proj.proj_len() < proj.horizon_mths() else "limiting age",
    "drawn to nothing at time {} (end of month t = {})".format(
        proj.fund_exhaust_mth(), proj.fund_exhaust_mth() - 1)
    if exhausted else "never exhausted"))
print()
print("Unit fund (per policy), first three months t = 0, 1, 2:")
print(proj.result_uf().head(3).round(2).to_string())
print()
print("Cash flows, first three months t = 0, 1, 2:")
print(proj.result_cf().head(3).round(2).to_string())

model.close()
