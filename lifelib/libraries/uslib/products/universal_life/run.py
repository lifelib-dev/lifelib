"""Run the UL_US_S reference model and print its account value roll-forward.

    python products/universal_life/run.py            # anchor cell (point_id = 1)
    python products/universal_life/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "UL_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} face {:,.0f} option {} {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.rate_class(), proj.sum_assured(), proj.db_option(), proj.qual_test()))
print("planned premium {:,.2f}/yr, load {:.0%}   credited {:.2%} (guaranteed {:.2%})   "
      "current COI {:.0%} of guaranteed max".format(
          proj.premium_pp_ann(), proj.load_prem_rate(),
          proj.crediting_rate_ann(1), proj.guar_rate_ann, proj.coi_curr_factor))
print("i_m = {:.7f}   NAAR factor = {:.7f}   surrender charge runs off by policy year {}"
      "   projection = {} policy months to attained age {}".format(
          proj.inv_return_mth(1), proj.naar_factor(), proj.lapse_shock_year(),
          proj.proj_len(), proj.age(proj.proj_len())))
print()
print("Account value roll-forward (per policy) - first 12 policy months")
print(proj.result_av().head(12).round(2).to_string())
print()
print("Liability cash flows - first 12 policy months")
print(proj.result_cf().head(12).round(2).to_string())

model.close()
