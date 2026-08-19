"""Run the IP_UK_S reference model and print its cash flow statement.

    python products/income_protection/run.py            # active-lives anchor cell
    python products/income_protection/run.py 2          # the claims-in-payment example

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "IP_UK_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} OC{} DP{}w, benefit {:,.0f}/month to age {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.occ_class(), proj.deferred_weeks(), proj.benefit_mth(), proj.expiry_age()))
print("status = {} (claim duration {} months)   recoveries {}   escalation = {}".format(
    proj.status(), proj.claim_duration_months(), proj.recovery_basis(),
    proj.escalation()))
print("premium = {:,.2f}/month   max benefit = {:,.2f}/month   "
      "inception(1) = {:.6f} p.a.   a_dis = {:.4f}".format(
          proj.premium_mth(), proj.benefit_max_pp(), proj.inception_rate(1),
          proj.annuity_dis()))
print()
print(proj.result_cf().head(12).round(2).to_string())

model.close()
