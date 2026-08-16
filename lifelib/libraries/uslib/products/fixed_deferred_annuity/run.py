"""Run the MYGA_US_S reference model and print its cash flow statement.

    python products/fixed_deferred_annuity/run.py            # anchor cell (point_id = 1)
    python products/fixed_deferred_annuity/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "MYGA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} premium {:,.0f}, {}-year guarantee period".format(
    point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(), proj.tax_status(),
    proj.premium_pp(), proj.guar_period()))
print("declared rate = {:.2%}  GMIR = {:.2%}  GMSV rate = {:.2%}  "
      "renewal = {}  MVA = {} / {}".format(
          proj.declared_rate_initial(), proj.gmir(), proj.mgsv_rate(),
          proj.renewal_architecture(), proj.mva_family(), proj.mva_cap_rule()))
print("months 1..{} (to attained age {}); shock lapse at contract year {} "
      "= {:.2%} p.a.".format(
          proj.proj_len(), proj.age(proj.proj_len()) + 1,
          proj.guar_period() + 1,
          proj.lapse_rate(12 * proj.guar_period() + 1)))
print()
print("account value and Model #805 floor, first 12 months (per contract):")
print(proj.result_av().iloc[:13, :5].round(2).to_string())
print()
print("cash flows, first 12 months:")
print(proj.result_cf().head(13).round(2).to_string())

model.close()
