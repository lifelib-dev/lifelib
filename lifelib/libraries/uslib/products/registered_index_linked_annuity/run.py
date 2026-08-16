"""Run the RILA_US_S reference model and print its cash flows.

    python products/registered_index_linked_annuity/run.py       # anchor cell (point_id = 1)
    python products/registered_index_linked_annuity/run.py 2     # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "RILA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} premium {:,.0f}, one {}-year {} option, "
      "buffer {:.0%}".format(
          point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(),
          proj.premium_pp(), proj.term_years(), proj.crediting_type(),
          proj.buffer()))
print("interim value family = {} / {}   scenario = {}   "
      "months 1..{} (Maturity Date at attained age {})".format(
          proj.iv_family(), proj.amort_rule(), proj.scenario_id(),
          proj.proj_len(), proj.age_at_entry() + proj.policy_term()))
print("option budget beta = {:.4%} = {:,.2f}   fixed leg opens at {:,.2f} "
      "and accretes at {:.4%}, a {:.2%} spread".format(
          proj.opt_budget(0), proj.opt_budget(0) * proj.premium_pp(),
          proj.premium_pp() * (1 - proj.opt_budget(0)),
          proj.fixed_leg_yield(0), proj.nge_spread_implied(0)))
print()

term_ends = [t for t in range(1, proj.proj_len() + 1) if proj.is_term_end(t)]
rows = sorted(set([0, 12, 36] + term_ends[:2]))
rows = [t for t in rows if t <= proj.proj_len()]
print("interim value decomposition at issue, month 12, the term midpoint "
      "and the first term ends:")
print(proj.result_iv().loc[rows].round(2).to_string())
print()

print("cash flows, first 12 months:")
print(proj.result_cf().head(13).round(2).to_string())

model.close()
