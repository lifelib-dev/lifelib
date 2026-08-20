"""Run the PA_UK_S reference model and print its cash flow statement.

    python products/pension_annuity/run.py            # the worked-example scenario
    python products/pension_annuity/run.py 2          # the same contract, expected basis

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "PA_UK_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
lives = "{}{}".format(proj.sex(1), proj.age_at_entry(1))
if proj.is_joint():
    lives += " with dependant {}{} at {:.0%}".format(
        proj.sex(2), proj.age_at_entry(2), proj.dependant_pct())
print("model point {}: {} - purchase price {:,.0f}, {}".format(
    point_id, proj.model_point()["policy_id"], proj.purchase_price(), lives))
print("income {:,.2f} p.a., {} payments in {}, escalation = {}   "
      "rating {:.2f}   basis = {}".format(
          proj.annual_income_init(), proj.payment_freq(), proj.payment_timing(),
          proj.escalation_type(), proj.rating_factor(1), proj.mort_basis()))
print("guarantee = {} months   value protection = {:.0%} on {}   overlap = {}".format(
    proj.guarantee_mths(), proj.vp_pct(), proj.vp_basis(), proj.overlap()))
print()
rows = [t for t in (3, 6, 9, 12, 13, 15, 17, 18, 21, 24) if t <= proj.proj_len()]
print(proj.result_cf().loc[rows].round(2).to_string())

model.close()
