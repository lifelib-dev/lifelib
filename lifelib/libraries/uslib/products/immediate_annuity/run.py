"""Run the SPIA_US_S reference model and print its cash flow statement.

    python products/immediate_annuity/run.py            # anchor cell (point_id = 1)
    python products/immediate_annuity/run.py 8          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "SPIA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
lives = "{}{}".format(proj.sex(1), proj.age_at_entry(1))
if proj.is_joint():
    lives += " + {}{}".format(proj.sex(2), proj.age_at_entry(2))
print("model point {}: {} - {} {} premium {:,.0f} income {:,.0f}/yr".format(
    point_id, proj.model_point()["policy_id"], proj.form(), lives,
    proj.premium_pp(), proj.annual_income(1)))
print("m = {} in {}   COLA = {:.0%}   survivor = {:.2%} on {} death   "
      "certain = {} mths".format(
          proj.payment_freq(), proj.payment_timing(), proj.cola_rate(),
          proj.survivor_pct(), proj.reduction_trigger(), proj.certain_mths_eff()))
print("mortality basis = {}   proj_len = {} mths (max of the age stop rule, {} mths, "
      "and the certain period)".format(
          proj.mort_basis(), proj.proj_len(), proj.horizon_mths()))
print()
print(proj.result_cf().head(15).round(2).to_string())

model.close()
