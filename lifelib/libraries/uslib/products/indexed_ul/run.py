"""Run the IUL_US_S reference model and print its account value roll-forward.

    python products/indexed_ul/run.py            # baseline cell (point_id = 1)
    python products/indexed_ul/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "IUL_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} face {:,.0f} option {} {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.rate_class(), proj.sum_assured(), proj.db_option(), proj.qual_test()))
print("planned premium {:,.2f}/yr {} mode, load {:.0%}   indexed allocation {:.0%}"
      "   fixed account {:.2%} (guaranteed {:.2%})".format(
          proj.premium_pp_ann(), proj.premium_mode(), proj.load_prem_rate(),
          proj.index_alloc_rate(), proj.fixed_rate_ann(1), proj.guar_rate_ann))
print("index account: cap {:.2%} (guaranteed {:.2%}), par {:.0%}, floor {:.0%}"
      "   level index return {:.2%}/yr   credited rate {:.2%}".format(
          proj.index_cap_at(1), proj.index_cap_guar, proj.index_par,
          proj.index_floor, proj.index_return_ann,
          proj.index_credit_rate(proj.index_return_ann)))
print("NAAR factor = {:.7f}   surrender charge runs off by policy year {}"
      "   projection = {} policy months to attained age {}".format(
          proj.naar_factor(), proj.lapse_shock_year(), proj.proj_len(),
          proj.age(proj.proj_len()) + 1))
print()
print("Account value roll-forward (per policy) - policy months 1-14")
print(proj.result_av().head(14).round(2).to_string())
print()
print("Indexed segment ladder - policy months 1-14")
print(proj.result_seg().head(14).round(2).to_string())
print()
print("Liability cash flows - policy months 1-14")
print(proj.result_cf().head(14).round(2).to_string())

model.close()
