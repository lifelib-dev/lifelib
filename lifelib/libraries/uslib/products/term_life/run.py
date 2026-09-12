"""Run the Term_US_S reference model and print its cash flow statement.

    python products/term_life/run.py            # anchor cell (point_id = 1)
    python products/term_life/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Term_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} {} sum assured {:,.0f} ({} mode)".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.rate_class(), proj.plan(), proj.sum_assured(), proj.premium_mode()))
print("jump ratio = {:.4f}   shock lapse = {:.0%} at month {}   M(1) = {}   "
      "expiry = attained age 95 (proj_len = {} months, t = 0..{})".format(
          proj.jump_ratio(), proj.shock_lapse_rate(), 12 * proj.policy_term() - 1,
          proj.plt_mort_factor_init(), proj.proj_len(), proj.proj_len() - 1))
print()
print("first 12 rows, t = 0..11 (the months of policy year 1):")
print(proj.result_cf().head(12).round(2).to_string())
print()
print("summed into policy years, years 1-12 (the notes' second table):")
print(proj.result_cf_annual().head(12).round(2).to_string())

model.close()
