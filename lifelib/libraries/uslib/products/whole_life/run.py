"""Run the WholeLife_US_A reference model and print its cash flow statement.

    python products/whole_life/run.py            # anchor cell (point_id = 1)
    python products/whole_life/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "WholeLife_US_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {} {}{} {} face {:,.0f} premium {:,.2f}".format(
    point_id, proj.model_point()["policy_id"], proj.product(), proj.sex(),
    proj.age_at_entry(), proj.risk_class(), proj.sum_assured(), proj.premium_pp(1)))
print("premium period {} ({} yrs)   dividend option {}   "
      "maturity at attained age 100 (policy year {})".format(
          proj.premium_period(), proj.policy_term(), proj.dividend_option(),
          proj.proj_len()))
print("i_g = {:.2%}   i_d = {:.2%}   i_L = {:.2%}   "
      "projection starts at policy year {}   MEC flag {}".format(
          proj.int_rate_guar, proj.int_rate_div, proj.int_rate_loan,
          proj.proj_start(), proj.mec_flag()))
print("net_cf: INCOME POSITIVE (library convention);   "
      "liability_cf = -net_cf: OUTGO POSITIVE (the technical notes' NetCF_t)")
print("pols_if(t) is the START-of-year count, the weight on that row's cash flows")
print()
print(proj.result_cf().head(12).round(2).to_string())

model.close()
