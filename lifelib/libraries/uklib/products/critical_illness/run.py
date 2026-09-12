"""Run the CI_UK_S reference model and print its cash flow statement.

    python products/critical_illness/run.py            # anchor cell (point_id = 1)
    python products/critical_illness/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "CI_UK_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} {} cover, {}-year term, sum assured {:,.0f}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.smoker(), proj.contract_type(), proj.policy_term(), proj.sum_assured()))
print("premium = {:,.2f}/month ({})   q_claim(0) = {:.6f} = i_ci {:.6f} + q_d {:.6f} "
      "x (1 - k)".format(
          proj.premium_mth_pp(), proj.premium_guarantee(), proj.claim_rate(0),
          proj.ci_rate(0), proj.mort_rate(0)))
print("additional payment {:,.0f}   children's cover {:,.0f}   life basis {}".format(
    proj.benefit_pp(0, "AP"), proj.benefit_pp(0, "CHILD"), proj.life_basis()))
print()
print("first policy year, t = 0 .. 11 of {} months (t is 0-based):".format(
    proj.proj_len()))
print(proj.result_cf().head(12).round(2).to_string())

model.close()
