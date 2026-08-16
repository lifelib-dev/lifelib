"""Run the Term_US_A reference model and print its cash flow statement.

    python products/term_life/run.py            # anchor cell (point_id = 1)
    python products/term_life/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Term_US_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} {} sum assured {:,.0f}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.rate_class(), proj.plan(), proj.sum_assured()))
print("jump ratio = {:.4f}   shock lapse = {:.0%}   M(1) = {}   "
      "expiry = attained age 95 (policy year {})".format(
          proj.jump_ratio(), proj.shock_lapse_rate(),
          proj.plt_mort_factor_init(), proj.proj_len()))
print()
print(proj.result_cf().head(12).round(2).to_string())

model.close()
