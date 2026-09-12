"""Run the Dep_FR_S reference model and print its cash flow statement.

    python products/dependance/run.py            # the worked example's anchor cell
    python products/dependance/run.py 9          # a claim already in payment

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Dep_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} on {}, rente {:,.0f}/month "
      "({:.0%} partial)".format(
          point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(),
          proj.cover_type(), proj.trigger_grid(), proj.rente_total_mth(),
          proj.partial_ratio()))
print("status = {} (claim duration {} months)   capital {:,.0f}   "
      "premium {:,.2f}/month {}".format(
          proj.status(), proj.claim_duration_months(), proj.capital_amount(),
          proj.premium_mth(), proj.premium_mode()))
print("carence {}/{}/{} months by cause   franchise {} months   "
      "reduction from {} years   proj_len {} months (t = 0 .. {})".format(
          proj.carence_accident_months(), proj.carence_illness_months(),
          proj.carence_neuro_months(), proj.franchise_months(),
          proj.reduction_qualifying_years(), proj.proj_len(),
          proj.proj_len() - 1))
print("mort_rate({}) = {:.6f}   partielle {:.6f}   totale {:.6f}   "
      "sojourn in totale from 84 = {:.4f} years".format(
          proj.age(0), proj.mort_rate(0), proj.mort_rate_partial(0),
          proj.mort_rate_total(0), proj.sojourn_total(84)))
print("prev({}) = {:.6f}   i_P = {:.6f} p.a.   i_T = {:.6f} p.a.".format(
    proj.age(0), proj.prev_rate(0), proj.inc_rate_partial(0),
    proj.inc_rate_total(0)))
print()
print(proj.result_cf().head(16).round(4).to_string())

model.close()
