"""Run the ULSG_US_S reference model and print its account roll-forward.

    python products/guaranteed_ul/run.py            # anchor cell (point_id = 1)
    python products/guaranteed_ul/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "ULSG_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} face {:,.0f} guarantee to age {} {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.rate_class(), proj.sum_assured(), proj.guarantee_age(),
    proj.premium_type()))
print("premium {:,.2f} mode {}   base load {:.0%} / shadow load {:.0%}   "
      "credited {:.2%} (guaranteed {:.2%}) / shadow {:.2%}".format(
          proj.premium_pp_ann(), proj.premium_mode(), proj.load_prem_rate(),
          proj.load_prem_rate_sg, proj.crediting_rate_ann(1),
          proj.guar_rate_ann, proj.sg_rate_ann))
print("current COI {:.0%} / shadow COI {:.0%} of guaranteed max   "
      "NAAR factors {:.7f} base / {:.7f} shadow".format(
          proj.coi_curr_factor, proj.coi_sg_factor,
          proj.naar_factor(), proj.sg_naar_factor()))
print("opening AV {:,.2f}   opening SG {:,.2f}   projection = {} policy months "
      "from policy month {} to attained age {}".format(
          proj.av_pp_init(), proj.sg_pp_init(), proj.proj_len(),
          proj.duration_mth_init() + 1, proj.age(proj.proj_len()) + 1))
print()

print("Account values (per policy) - first 12 projected months")
print(proj.result_av().head(12).round(2).to_string())
print()

print("Guarantee diagnostics - first 12 projected months")
print(proj.result_guar().head(12).round(2).to_string())
print()

print("Liability cash flows - first 12 projected months")
print(proj.result_cf().head(12).round(2).to_string())

model.close()
