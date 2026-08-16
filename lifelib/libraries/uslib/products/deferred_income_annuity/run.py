"""Run the DIA_US_S reference model and print its cash flow statement.

    python products/deferred_income_annuity/run.py       # anchor cell (point_id = 1)
    python products/deferred_income_annuity/run.py 5     # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "DIA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
lives = "{}{}".format(proj.sex(1), proj.age_at_entry(1))
if proj.is_joint():
    lives += " + {}{}".format(proj.sex(2), proj.age_at_entry(2))
prem = proj.premium_by_mth()
sched = ", ".join("{:,.0f} at month {}".format(prem[k], k) for k in sorted(prem))
start = proj.income_start_mth()

print("model point {}: {} - {} {} {} - premiums {}".format(
    point_id, proj.model_point()["policy_id"], proj.market_type(),
    proj.income_form(), lives, sched))
print("deferral DB = {}   income starts month {} (attained age {})   "
      "m = {} in {}   COLA = {:.0%}".format(
          proj.db_form(), start, proj.age(start, 1),
          proj.payment_freq(), proj.payment_timing(), proj.cola_rate()))
print("pricing factors = {}   CP(T) = {:,.0f}   B = {:,.2f}/yr = {:,.2f}/mth   "
      "guarantee = {:.4f} yrs ({} certain months)".format(
          proj.factor_basis(), proj.cum_premium_pp(start),
          proj.annual_income(start), proj.annual_income(start) / proj.payment_freq(),
          proj.guarantee_yrs(), proj.certain_mths_eff()))
if proj.is_qlac():
    flags = proj.qlac_flags()
    print("QLAC: room at issue {:,.0f}   compliance {}".format(
        proj.qlac_room(0), "OK" if not flags else "; ".join(flags)))
print()
print("annual display grid (the technical notes' worked-example table):")
print(proj.result_annual().head(25).round(2).to_string())
print()
print("monthly cash flows around the income start date:")
print(proj.result_cf().loc[start - 2:start + 3].round(2).to_string())

model.close()
