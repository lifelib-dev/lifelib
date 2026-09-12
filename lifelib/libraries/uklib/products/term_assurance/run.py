"""Run the Term_UK_S reference model and print its cash flow statement.

    python products/term_assurance/run.py            # anchor cell (point_id = 1)
    python products/term_assurance/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Term_UK_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
cover = ("income {:,.0f}/month".format(proj.fib_income())
         if proj.shape() == "fib" else "cover {:,.0f}".format(proj.sum_assured()))
print("model point {}: {} - {}{} {} {} shape, {}-year term, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.smoker(), proj.shape(), proj.policy_term(), cover))
print("premium = {:,.2f}/month ({:,.2f} p.a.)   mode = {}   mortality basis = {}   "
      "indexation = {}   waiver = {}".format(
          proj.premium_mth_pp(), 12 * proj.premium_mth_pp(), proj.premium_mode(),
          proj.mort_basis(), proj.indexation(), proj.wop()))
print()
print("cash flows by month t, 0-based from issue (policy year = t // 12 + 1); "
      "frame t = {} .. {}, first 12 rows:".format(
          proj.proj_start(), proj.proj_len() - 1))
print(proj.result_cf().head(12).round(2).to_string())

model.close()
